from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.audit.service import record_audit_event
from app.intelligence.extract import normalize_for_compare
from app.models.document import Document
from app.models.intelligence import (
    CitizenProfile,
    ExtractedField,
    ProfileField,
)


class ProfileService:
    def __init__(self, db: Session):
        self.db = db

    def get_or_create_profile(self, user_id: uuid.UUID) -> CitizenProfile:
        profile = self.db.query(CitizenProfile).filter(CitizenProfile.user_id == user_id).one_or_none()
        if profile:
            return profile
        profile = CitizenProfile(user_id=user_id, version=1)
        self.db.add(profile)
        self.db.commit()
        self.db.refresh(profile)
        return profile

    def get_profile(self, user_id: uuid.UUID) -> CitizenProfile:
        return self.get_or_create_profile(user_id)

    def list_conflicts(self, user_id: uuid.UUID) -> list[ProfileField]:
        profile = self.get_or_create_profile(user_id)
        return [f for f in profile.fields if f.verification_state == "conflict"]

    def review_extracted_field(
        self,
        *,
        user_id: uuid.UUID,
        field_id: uuid.UUID,
        action: str,
        value: str | None,
        ip: str | None,
    ) -> ExtractedField:
        field = (
            self.db.query(ExtractedField)
            .filter(ExtractedField.id == field_id)
            .one_or_none()
        )
        if field is None:
            raise HTTPException(status_code=404, detail="Field not found")
        doc = (
            self.db.query(Document)
            .filter(Document.id == field.document_id, Document.deleted_at.is_(None))
            .one_or_none()
        )
        if doc is None or doc.user_id != user_id:
            record_audit_event(
                self.db,
                action="profile.access_denied",
                actor_user_id=user_id,
                entity_type="extracted_field",
                entity_id=str(field_id),
                ip=ip,
            )
            self.db.commit()
            raise HTTPException(status_code=404, detail="Field not found")

        if action == "reject":
            field.verification_status = "rejected"
            record_audit_event(
                self.db,
                action="intelligence.field_rejected",
                actor_user_id=user_id,
                entity_type="extracted_field",
                entity_id=str(field.id),
                ip=ip,
            )
            self.db.commit()
            self.db.refresh(field)
            return field

        if action not in {"confirm", "correct"}:
            raise HTTPException(status_code=400, detail="Invalid action")

        chosen = value if action == "correct" else (field.normalized_value or field.raw_value)
        if not chosen or not str(chosen).strip():
            raise HTTPException(status_code=400, detail="A value is required")

        if action == "correct":
            field.user_corrected_value = str(chosen).strip()
            field.verification_status = "user_corrected"
            field.normalized_value = str(chosen).strip()
        else:
            field.verification_status = "user_verified"

        self._upsert_profile_from_field(
            user_id=user_id,
            field=field,
            value=str(chosen).strip(),
            user_corrected=(action == "correct"),
            ip=ip,
        )
        record_audit_event(
            self.db,
            action="intelligence.field_verified" if action == "confirm" else "intelligence.field_corrected",
            actor_user_id=user_id,
            entity_type="extracted_field",
            entity_id=str(field.id),
            metadata={"field_key": field.field_key},
            ip=ip,
        )
        self.db.commit()
        self.db.refresh(field)
        return field

    def resolve_conflict(
        self,
        *,
        user_id: uuid.UUID,
        field_key: str,
        value: str,
        source_extracted_field_id: uuid.UUID | None,
        ip: str | None,
    ) -> ProfileField:
        profile = self.get_or_create_profile(user_id)
        pf = (
            self.db.query(ProfileField)
            .filter(ProfileField.profile_id == profile.id, ProfileField.field_key == field_key)
            .one_or_none()
        )
        if pf is None or pf.verification_state != "conflict":
            raise HTTPException(status_code=404, detail="No unresolved conflict for this field")

        chosen = value.strip()
        if not chosen:
            raise HTTPException(status_code=400, detail="A value is required")

        pf.value = chosen
        pf.verification_state = "verified"
        pf.user_corrected = True
        pf.conflict_candidates_json = None
        pf.updated_at = datetime.now(timezone.utc)
        if source_extracted_field_id:
            ef = (
                self.db.query(ExtractedField)
                .filter(ExtractedField.id == source_extracted_field_id)
                .one_or_none()
            )
            if ef and self._owns_extracted(user_id, ef):
                pf.source_extracted_field_id = ef.id
                pf.source_document_id = ef.document_id
                pf.source_document_version_id = ef.document_version_id
                if pf.original_extracted_value is None:
                    pf.original_extracted_value = ef.normalized_value or ef.raw_value

        profile.version += 1
        record_audit_event(
            self.db,
            action="profile.conflict_resolved",
            actor_user_id=user_id,
            entity_type="profile_field",
            entity_id=str(pf.id),
            metadata={"field_key": field_key},
            ip=ip,
        )
        self.db.commit()
        self.db.refresh(pf)
        return pf

    def update_profile_field(
        self,
        *,
        user_id: uuid.UUID,
        field_key: str,
        value: str,
        verify: bool,
        ip: str | None,
    ) -> ProfileField:
        profile = self.get_or_create_profile(user_id)
        pf = (
            self.db.query(ProfileField)
            .filter(ProfileField.profile_id == profile.id, ProfileField.field_key == field_key)
            .one_or_none()
        )
        if pf is None:
            pf = ProfileField(
                profile_id=profile.id,
                field_key=field_key,
                data_type="string",
                verification_state="unverified",
            )
            self.db.add(pf)
        if pf.original_extracted_value is None and pf.value:
            pf.original_extracted_value = pf.value
        pf.value = value.strip()
        pf.user_corrected = True
        pf.verification_state = "verified" if verify else "unverified"
        pf.updated_at = datetime.now(timezone.utc)
        profile.version += 1
        record_audit_event(
            self.db,
            action="profile.field_updated",
            actor_user_id=user_id,
            entity_type="profile_field",
            entity_id=str(pf.id) if pf.id else field_key,
            metadata={"field_key": field_key, "verified": verify},
            ip=ip,
        )
        self.db.commit()
        self.db.refresh(pf)
        return pf

    def _upsert_profile_from_field(
        self,
        *,
        user_id: uuid.UUID,
        field: ExtractedField,
        value: str,
        user_corrected: bool,
        ip: str | None,
    ) -> None:
        profile = self.get_or_create_profile(user_id)
        pf = (
            self.db.query(ProfileField)
            .filter(ProfileField.profile_id == profile.id, ProfileField.field_key == field.field_key)
            .one_or_none()
        )
        incoming_norm = normalize_for_compare(field.field_key, value)

        if pf is None:
            self.db.add(
                ProfileField(
                    profile_id=profile.id,
                    field_key=field.field_key,
                    value=value,
                    data_type=field.data_type,
                    verification_state="verified",
                    source_document_id=field.document_id,
                    source_document_version_id=field.document_version_id,
                    source_extracted_field_id=field.id,
                    original_extracted_value=field.normalized_value or field.raw_value,
                    user_corrected=user_corrected,
                )
            )
            profile.version += 1
            return

        existing_norm = normalize_for_compare(field.field_key, pf.value)
        if pf.verification_state == "verified" and existing_norm and incoming_norm and existing_norm != incoming_norm:
            # Conflict: do not silently overwrite verified values
            candidates = []
            if pf.conflict_candidates_json:
                try:
                    candidates = json.loads(pf.conflict_candidates_json)
                except json.JSONDecodeError:
                    candidates = []
            candidates.append(
                {
                    "value": pf.value,
                    "source_document_id": str(pf.source_document_id) if pf.source_document_id else None,
                    "source_extracted_field_id": str(pf.source_extracted_field_id)
                    if pf.source_extracted_field_id
                    else None,
                    "label": "current_verified",
                }
            )
            candidates.append(
                {
                    "value": value,
                    "source_document_id": str(field.document_id),
                    "source_extracted_field_id": str(field.id),
                    "label": "incoming",
                }
            )
            pf.verification_state = "conflict"
            pf.conflict_candidates_json = json.dumps(candidates)
            pf.updated_at = datetime.now(timezone.utc)
            profile.version += 1
            record_audit_event(
                self.db,
                action="profile.conflict_detected",
                actor_user_id=user_id,
                entity_type="profile_field",
                entity_id=str(pf.id),
                metadata={"field_key": field.field_key},
                ip=ip,
            )
            return

        if pf.verification_state == "verified" and existing_norm == incoming_norm:
            # Equivalent after normalization — keep verified, refresh provenance optionally
            return

        # Unverified / needs_review can be updated with explicit user confirmation
        if pf.original_extracted_value is None:
            pf.original_extracted_value = field.normalized_value or field.raw_value
        pf.value = value
        pf.verification_state = "verified"
        pf.user_corrected = user_corrected
        pf.source_document_id = field.document_id
        pf.source_document_version_id = field.document_version_id
        pf.source_extracted_field_id = field.id
        pf.updated_at = datetime.now(timezone.utc)
        profile.version += 1

    def _owns_extracted(self, user_id: uuid.UUID, field: ExtractedField) -> bool:
        doc = self.db.query(Document).filter(Document.id == field.document_id).one_or_none()
        return bool(doc and doc.user_id == user_id and doc.deleted_at is None)
