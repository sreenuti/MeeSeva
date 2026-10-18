from __future__ import annotations

import hashlib
import json
import uuid
from typing import Any

from sqlalchemy.orm import Session

from app.models.audit import AuditEvent


def _hash_ip(ip: str | None) -> str | None:
    if not ip:
        return None
    return hashlib.sha256(ip.encode("utf-8")).hexdigest()


def record_audit_event(
    db: Session,
    *,
    action: str,
    actor_user_id: uuid.UUID | None = None,
    entity_type: str | None = None,
    entity_id: str | None = None,
    metadata: dict[str, Any] | None = None,
    ip: str | None = None,
) -> AuditEvent:
    # Never accept document contents or tokens in metadata.
    safe_meta = None
    if metadata:
        blocked = {"content", "token", "access_token", "authorization", "password", "file_bytes"}
        cleaned = {k: v for k, v in metadata.items() if k.lower() not in blocked}
        safe_meta = json.dumps(cleaned, default=str)

    event = AuditEvent(
        actor_user_id=actor_user_id,
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        metadata_json=safe_meta,
        ip_hash=_hash_ip(ip),
    )
    db.add(event)
    db.flush()
    return event
