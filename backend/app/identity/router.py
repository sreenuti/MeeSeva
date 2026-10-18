from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.audit.service import record_audit_event
from app.config import Settings, get_settings
from app.db import get_db
from app.identity.deps import AuthContext, get_current_user
from app.identity.jwt_validator import mint_dev_token
from app.identity.schemas import ConsentIn, ConsentOut, DevTokenRequest, UserOut
from app.models.consent import ConsentRecord

router = APIRouter(tags=["identity"])


@router.get("/me", response_model=UserOut)
def get_me(auth: Annotated[AuthContext, Depends(get_current_user)]):
    return auth.user


@router.post("/consents", response_model=list[ConsentOut])
def record_consents(
    body: ConsentIn,
    auth: Annotated[AuthContext, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
    settings: Annotated[Settings, Depends(get_settings)],
):
    allowed = {"vault_storage", "application_preparation", "notifications"}
    created: list[ConsentRecord] = []
    for purpose in body.purposes:
        if purpose not in allowed:
            raise HTTPException(status_code=400, detail=f"Unknown consent purpose: {purpose}")
        row = ConsentRecord(
            user_id=auth.user.id,
            purpose=purpose,
            policy_version=settings.consent_policy_version,
            granted=body.granted,
            channel="web",
        )
        db.add(row)
        created.append(row)
    record_audit_event(
        db,
        action="consent.recorded",
        actor_user_id=auth.user.id,
        metadata={"purposes": body.purposes, "granted": body.granted},
        ip=auth.ip,
    )
    db.commit()
    for row in created:
        db.refresh(row)
    return created


@router.get("/consents", response_model=list[ConsentOut])
def list_consents(
    auth: Annotated[AuthContext, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    return (
        db.query(ConsentRecord)
        .filter(ConsentRecord.user_id == auth.user.id, ConsentRecord.revoked_at.is_(None))
        .order_by(ConsentRecord.granted_at.desc())
        .all()
    )


@router.post("/dev/token")
def issue_dev_token(
    body: DevTokenRequest,
    settings: Annotated[Settings, Depends(get_settings)],
):
    if settings.environment not in ("development", "test") or not settings.auth_dev_mode:
        raise HTTPException(status_code=404, detail="Not found")
    token = mint_dev_token(settings, subject=body.subject, email=str(body.email) if body.email else None)
    return {
        "access_token": token,
        "token_type": "bearer",
        "expires_in": 3600,
        "warning": "Development-only token. Disabled in staging/production.",
    }
