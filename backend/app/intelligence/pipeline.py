from __future__ import annotations

import uuid
from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.audit.service import record_audit_event
from app.config import Settings
from app.intelligence.classify import classify_document
from app.intelligence.extract import extract_fields
from app.intelligence.ocr.local import build_ocr_provider
from app.models.document import Document, DocumentVersion
from app.models.intelligence import DocumentExtraction, DocumentProcessingJob, ExtractedField
from app.vault.storage import ObjectStorage


ACTIVE_JOB_STATUSES = {"queued", "processing"}
TERMINAL_OK = {"completed", "awaiting_user_review"}


class IntelligencePipeline:
    def __init__(self, db: Session, storage: ObjectStorage, settings: Settings):
        self.db = db
        self.storage = storage
        self.settings = settings
        self.ocr = build_ocr_provider(settings.ocr_provider)

    def enqueue(
        self, *, user_id: uuid.UUID, document_id: uuid.UUID, ip: str | None
    ) -> DocumentProcessingJob:
        doc, version = self._require_processable(user_id, document_id, ip=ip)

        existing = (
            self.db.query(DocumentProcessingJob)
            .filter(DocumentProcessingJob.document_version_id == version.id)
            .one_or_none()
        )
        if existing:
            if existing.status in ACTIVE_JOB_STATUSES or existing.status in TERMINAL_OK:
                return existing
            # Allow restart from failed/unsupported
            existing.status = "queued"
            existing.error_code = None
            existing.error_message = None
            existing.started_at = None
            existing.finished_at = None
            if existing.extraction:
                for field in list(existing.extraction.fields):
                    self.db.delete(field)
                self.db.delete(existing.extraction)
                self.db.flush()
            record_audit_event(
                self.db,
                action="intelligence.requeued",
                actor_user_id=user_id,
                entity_type="document",
                entity_id=str(document_id),
                metadata={"job_id": str(existing.id)},
                ip=ip,
            )
            self.db.commit()
            self.db.refresh(existing)
            return existing

        job = DocumentProcessingJob(
            document_id=doc.id,
            document_version_id=version.id,
            user_id=user_id,
            status="queued",
        )
        self.db.add(job)
        record_audit_event(
            self.db,
            action="intelligence.queued",
            actor_user_id=user_id,
            entity_type="document",
            entity_id=str(document_id),
            metadata={"version_id": str(version.id)},
            ip=ip,
        )
        self.db.commit()
        self.db.refresh(job)
        return job

    def process_job(self, job_id: uuid.UUID) -> DocumentProcessingJob:
        job = self.db.query(DocumentProcessingJob).filter(DocumentProcessingJob.id == job_id).one_or_none()
        if job is None:
            return job  # type: ignore[return-value]
        if job.status in TERMINAL_OK:
            return job
        if job.status == "processing":
            return job

        job.status = "processing"
        job.started_at = datetime.now(timezone.utc)
        self.db.commit()

        try:
            doc = self.db.query(Document).filter(Document.id == job.document_id).one()
            version = self.db.query(DocumentVersion).filter(DocumentVersion.id == job.document_version_id).one()

            if doc.deleted_at is not None or doc.user_id != job.user_id:
                return self._fail(job, "document_unavailable", "Document is not available for processing")
            if version.scan_status != "clean":
                return self._fail(job, "security_gate", "Document has not passed security clearance")

            content = self.storage.get_bytes(version.storage_key)
            ocr = self.ocr.extract(
                content,
                mime_type=version.mime_type,
                max_pages=self.settings.ocr_max_pages,
                timeout_seconds=self.settings.ocr_timeout_seconds,
            )

            if "malformed_pdf" in ocr.errors or "malformed_image" in ocr.errors:
                return self._fail(job, "malformed_file", "We could not read this file safely", status_value="failed")

            if not ocr.has_text:
                # Image without tesseract or empty PDF
                if "tesseract_unavailable" in ocr.errors or "unsupported_mime" in ocr.errors:
                    return self._fail(
                        job,
                        "unsupported",
                        "This file type could not be read with the local text extractor",
                        status_value="unsupported",
                    )
                return self._fail(
                    job,
                    "no_text",
                    "We could not find readable text in this document",
                    status_value="failed",
                )

            classification = classify_document(ocr.full_text)
            pages = [(p.page_number, p.text) for p in ocr.pages]
            fields = extract_fields(ocr.full_text, classification.category, pages=pages)

            extraction = DocumentExtraction(
                job_id=job.id,
                document_id=job.document_id,
                document_version_id=job.document_version_id,
                user_id=job.user_id,
                predicted_category=classification.category,
                category_certainty=classification.certainty,
                extraction_method="local_rules_v1",
                page_count=ocr.page_count,
            )
            self.db.add(extraction)
            self.db.flush()

            for cand in fields:
                self.db.add(
                    ExtractedField(
                        extraction_id=extraction.id,
                        document_id=job.document_id,
                        document_version_id=job.document_version_id,
                        field_key=cand.field_key,
                        raw_value=cand.raw_value,
                        normalized_value=cand.normalized_value,
                        data_type=cand.data_type,
                        confidence=cand.confidence,
                        validation_result=cand.validation_result,
                        verification_status="extracted_unverified",
                        source_page=cand.source_page,
                        source_text_snippet=cand.source_text_snippet,
                        extraction_method="local_rules_v1",
                    )
                )

            # Update document type label for UX (does not change ownership/security)
            if classification.category != "unknown":
                doc.doc_type = classification.category

            job.status = "awaiting_user_review"
            job.finished_at = datetime.now(timezone.utc)
            job.error_code = None
            job.error_message = None
            record_audit_event(
                self.db,
                action="intelligence.completed",
                actor_user_id=job.user_id,
                entity_type="document",
                entity_id=str(job.document_id),
                metadata={
                    "job_id": str(job.id),
                    "category": classification.category,
                    "field_count": len(fields),
                },
            )
            self.db.commit()
            self.db.refresh(job)
            return job
        except Exception:
            self.db.rollback()
            job = self.db.query(DocumentProcessingJob).filter(DocumentProcessingJob.id == job_id).one()
            return self._fail(job, "processing_error", "Processing failed", status_value="failed")

    def get_job_for_owner(self, user_id: uuid.UUID, document_id: uuid.UUID, *, ip: str | None) -> DocumentProcessingJob:
        self._require_owned_document(user_id, document_id, ip=ip)
        job = (
            self.db.query(DocumentProcessingJob)
            .filter(
                DocumentProcessingJob.document_id == document_id,
                DocumentProcessingJob.user_id == user_id,
            )
            .order_by(DocumentProcessingJob.created_at.desc())
            .first()
        )
        if job is None:
            raise HTTPException(status_code=404, detail="No processing job found")
        return job

    def get_extraction_for_owner(self, user_id: uuid.UUID, document_id: uuid.UUID, *, ip: str | None):
        job = self.get_job_for_owner(user_id, document_id, ip=ip)
        if job.extraction is None:
            raise HTTPException(status_code=404, detail="Extraction results not available")
        return job.extraction

    def update_classification(
        self, *, user_id: uuid.UUID, document_id: uuid.UUID, category: str, ip: str | None
    ):
        if category not in {"identity_proof", "address_proof", "income_proof", "unknown"}:
            raise HTTPException(status_code=400, detail="Invalid category")
        extraction = self.get_extraction_for_owner(user_id, document_id, ip=ip)
        extraction.user_category = category
        doc = self.db.query(Document).filter(Document.id == document_id).one()
        doc.doc_type = category
        record_audit_event(
            self.db,
            action="intelligence.classification_corrected",
            actor_user_id=user_id,
            entity_type="document",
            entity_id=str(document_id),
            metadata={"category": category},
            ip=ip,
        )
        self.db.commit()
        self.db.refresh(extraction)
        return extraction

    def _require_processable(
        self, user_id: uuid.UUID, document_id: uuid.UUID, *, ip: str | None
    ) -> tuple[Document, DocumentVersion]:
        doc = self._require_owned_document(user_id, document_id, ip=ip)
        version = self._current_version(doc)
        if version is None:
            raise HTTPException(status_code=404, detail="Document version missing")
        if version.scan_status != "clean":
            record_audit_event(
                self.db,
                action="intelligence.denied_security_gate",
                actor_user_id=user_id,
                entity_type="document",
                entity_id=str(document_id),
                metadata={"scan_status": version.scan_status},
                ip=ip,
            )
            self.db.commit()
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Document must pass security clearance before processing",
            )
        if doc.status == "quarantined":
            raise HTTPException(status_code=403, detail="Quarantined documents cannot be processed")
        return doc, version

    def _require_owned_document(self, user_id: uuid.UUID, document_id: uuid.UUID, *, ip: str | None) -> Document:
        doc = (
            self.db.query(Document)
            .filter(Document.id == document_id, Document.deleted_at.is_(None))
            .one_or_none()
        )
        if doc is None or doc.user_id != user_id:
            record_audit_event(
                self.db,
                action="intelligence.access_denied",
                actor_user_id=user_id,
                entity_type="document",
                entity_id=str(document_id),
                metadata={"reason": "not_found_or_not_owner"},
                ip=ip,
            )
            self.db.commit()
            raise HTTPException(status_code=404, detail="Document not found")
        return doc

    def _current_version(self, doc: Document) -> DocumentVersion | None:
        if doc.current_version_id:
            return (
                self.db.query(DocumentVersion)
                .filter(DocumentVersion.id == doc.current_version_id)
                .one_or_none()
            )
        return (
            self.db.query(DocumentVersion)
            .filter(DocumentVersion.document_id == doc.id)
            .order_by(DocumentVersion.created_at.desc())
            .first()
        )

    def _fail(
        self,
        job: DocumentProcessingJob,
        code: str,
        message: str,
        *,
        status_value: str = "failed",
    ) -> DocumentProcessingJob:
        job.status = status_value
        job.error_code = code
        # Never put document contents into error messages
        job.error_message = message[:255]
        job.finished_at = datetime.now(timezone.utc)
        record_audit_event(
            self.db,
            action="intelligence.failed",
            actor_user_id=job.user_id,
            entity_type="document",
            entity_id=str(job.document_id),
            metadata={"job_id": str(job.id), "error_code": code},
        )
        self.db.commit()
        self.db.refresh(job)
        return job
