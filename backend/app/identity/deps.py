from __future__ import annotations

from dataclasses import dataclass
from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.audit.service import record_audit_event
from app.config import Settings, get_settings
from app.db import get_db
from app.identity.jwt_validator import build_validator
from app.models.user import User

_bearer = HTTPBearer(auto_error=False)
_validator = None


def get_validator(settings: Settings = Depends(get_settings)):
    global _validator
    if _validator is None:
        _validator = build_validator(settings)
    return _validator


@dataclass
class AuthContext:
    user: User
    claims: dict
    ip: str | None


def _client_ip(request: Request) -> str | None:
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    if request.client:
        return request.client.host
    return None


def get_current_user(
    request: Request,
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(_bearer)],
    db: Annotated[Session, Depends(get_db)],
    settings: Annotated[Settings, Depends(get_settings)],
    validator=Depends(get_validator),
) -> AuthContext:
    if credentials is None or credentials.scheme.lower() != "bearer":
        record_audit_event(db, action="auth.unauthenticated", ip=_client_ip(request))
        db.commit()
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")

    claims = validator.validate(credentials.credentials)
    subject = claims.get("sub")
    if not subject:
        raise HTTPException(status_code=401, detail="Token missing subject")

    user = db.query(User).filter(User.idp_subject == subject, User.deleted_at.is_(None)).one_or_none()
    if user is None:
        user = User(
            idp_subject=subject,
            email=claims.get("email"),
            status="active",
            locale="en",
        )
        db.add(user)
        db.flush()
        record_audit_event(
            db,
            action="auth.user_provisioned",
            actor_user_id=user.id,
            entity_type="user",
            entity_id=str(user.id),
            ip=_client_ip(request),
        )
        db.commit()
        db.refresh(user)

    return AuthContext(user=user, claims=claims, ip=_client_ip(request))


def require_user_id_from_auth(auth: AuthContext) -> UUID:
    """Ownership must always come from the verified token-mapped user, never the client."""
    return auth.user.id
