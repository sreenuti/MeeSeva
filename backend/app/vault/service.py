from __future__ import annotations

import hashlib
import uuid
from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.audit.service import record_audit_event
from app.config import Settings
from app.models.document import Document, DocumentVersion
from app.vault.scanner import MalwareScanner
from app.vault.storage import ObjectStorage
from app.vault.validation import ValidatedUpload


def _opaque_key(user_id: uuid.UUID) -> str:
    return f"vault/{user_id}/{uuid.uuid4().hex}"


def _to_out(doc: Document, version: DocumentVersion | None) -> dict:
    scan = version.scan_status if version else None
    downloadable = bool(version and scan == "clean" and doc.status == "active" and doc.deleted_at is None)
    return {
        "id": doc.id,
        "display_name": doc.display_name,
        "doc_type": doc.doc_type,
        "status": doc.status,
        "expires_on": doc.expires_on,
        "mime_type": version.mime_type if version else None,
        "byte_size": version.byte_size if version else None,
        "scan_status": scan,
        "created_at": doc.created_at,
        "downloadable": downloadable,
    }


class VaultService:
    def __init__(self, db: Session, storage: ObjectStorage, scanner: MalwareScanner, settings: Settings):
        self.db = db
        self.storage = storage
        self.scanner = scanner
        self.settings = settings

    def list_documents(self, user_id: uuid.UUID) -> list[dict]:
        docs = (
            self.db.query(Document)
            .filter(Document.user_id == user_id, Document.deleted_at.is_(None))
            .order_by(Document.created_at.desc())
            .all()
        )
        items = []
        for doc in docs:
            version = self._current_version(doc)
            items.append(_to_out(doc, version))
        return items

    def get_owned_document(self, user_id: uuid.UUID, document_id: uuid.UUID, *, ip: str | None) -> Document:
        doc = (
            self.db.query(Document)
            .filter(Document.id == document_id, Document.deleted_at.is_(None))
            .one_or_none()
        )
        if doc is None or doc.user_id != user_id:
            record_audit_event(
                self.db,
                action="document.access_denied",
                actor_user_id=user_id,
                entity_type="document",
                entity_id=str(document_id),
                metadata={"reason": "not_found_or_not_owner"},
                ip=ip,
            )
            self.db.commit()
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
        return doc

    def upload(
        self,
        *,
        user_id: uuid.UUID,
        validated: ValidatedUpload,
        doc_type: str,
        display_name: str | None,
        ip: str | None,
    ) -> dict:
        storage_key = _opaque_key(user_id)
        content_hash = hashlib.sha256(validated.content).hexdigest()

        try:
            self.storage.put_bytes(storage_key, validated.content, validated.mime_type)
        except Exception as exc:
            record_audit_event(
                self.db,
                action="document.upload_failed",
                actor_user_id=user_id,
                metadata={"reason": "storage_put_failed", "error_type": exc.__class__.__name__},
                ip=ip,
            )
            self.db.commit()
            raise HTTPException(status_code=500, detail="Storage failure") from exc

        scan = self.scanner.scan(validated.content, filename=validated.original_filename)
        # Fail-closed: failed scans are not downloadable
        if scan.status == "failed" and self.settings.fail_closed_on_scan_error:
            effective_status = "failed"
        else:
            effective_status = scan.status

        try:
            doc = Document(
                user_id=user_id,
                doc_type=doc_type or "unclassified",
                display_name=display_name or validated.original_filename,
                status="active" if effective_status != "infected" else "quarantined",
            )
            self.db.add(doc)
            self.db.flush()

            version = DocumentVersion(
                document_id=doc.id,
                storage_key=storage_key,
                content_hash=content_hash,
                mime_type=validated.mime_type,
                byte_size=validated.size,
                original_filename=validated.original_filename,
                scan_status=effective_status,
                scan_detail=scan.detail,
            )
            self.db.add(version)
            self.db.flush()
            doc.current_version_id = version.id

            record_audit_event(
                self.db,
                action="document.uploaded",
                actor_user_id=user_id,
                entity_type="document",
                entity_id=str(doc.id),
                metadata={
                    "mime_type": validated.mime_type,
                    "byte_size": validated.size,
                    "scan_status": effective_status,
                    "content_hash": content_hash,
                },
                ip=ip,
            )
            self.db.commit()
            self.db.refresh(doc)
            return _to_out(doc, version)
        except Exception:
            # Upload failure cleanup: remove orphaned object
            try:
                self.storage.delete(storage_key)
            except Exception:
                pass
            self.db.rollback()
            raise

    def update_metadata(
        self, *, user_id: uuid.UUID, document_id: uuid.UUID, updates: dict, ip: str | None
    ) -> dict:
        doc = self.get_owned_document(user_id, document_id, ip=ip)
        if updates.get("display_name"):
            doc.display_name = updates["display_name"]
        if updates.get("doc_type"):
            doc.doc_type = updates["doc_type"]
        if "expires_on" in updates:
            doc.expires_on = updates["expires_on"]
        self.db.commit()
        self.db.refresh(doc)
        return _to_out(doc, self._current_version(doc))

    def soft_delete(self, *, user_id: uuid.UUID, document_id: uuid.UUID, ip: str | None) -> None:
        doc = self.get_owned_document(user_id, document_id, ip=ip)
        doc.deleted_at = datetime.now(timezone.utc)
        doc.status = "deleted"
        record_audit_event(
            self.db,
            action="document.deleted",
            actor_user_id=user_id,
            entity_type="document",
            entity_id=str(doc.id),
            ip=ip,
        )
        self.db.commit()

    def prepare_download(
        self, *, user_id: uuid.UUID, document_id: uuid.UUID, ip: str | None
    ) -> tuple[Document, DocumentVersion, bytes | None, str | None]:
        doc = self.get_owned_document(user_id, document_id, ip=ip)
        version = self._current_version(doc)
        if version is None:
            raise HTTPException(status_code=404, detail="Document version missing")

        if version.scan_status != "clean":
            record_audit_event(
                self.db,
                action="document.download_denied",
                actor_user_id=user_id,
                entity_type="document",
                entity_id=str(doc.id),
                metadata={"reason": "scan_not_clean", "scan_status": version.scan_status},
                ip=ip,
            )
            self.db.commit()
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Document is quarantined or not yet cleared by malware scan",
            )

        record_audit_event(
            self.db,
            action="document.downloaded",
            actor_user_id=user_id,
            entity_type="document",
            entity_id=str(doc.id),
            metadata={"version_id": str(version.id)},
            ip=ip,
        )
        self.db.commit()

        if self.settings.storage_backend == "local":
            data = self.storage.get_bytes(version.storage_key)
            return doc, version, data, None

        url = self.storage.presigned_get_url(
            version.storage_key,
            expires_in=self.settings.download_url_ttl_seconds,
            filename=version.original_filename,
            content_type=version.mime_type,
        )
        return doc, version, None, url

    def _current_version(self, doc: Document) -> DocumentVersion | None:
        if doc.current_version_id:
            return self.db.query(DocumentVersion).filter(DocumentVersion.id == doc.current_version_id).one_or_none()
        return (
            self.db.query(DocumentVersion)
            .filter(DocumentVersion.document_id == doc.id)
            .order_by(DocumentVersion.created_at.desc())
            .first()
        )
