from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, File, Form, UploadFile
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.config import Settings, get_settings
from app.db import get_db
from app.identity.deps import AuthContext, get_current_user
from app.vault.scanner import build_scanner
from app.vault.schemas import DocumentListOut, DocumentOut, DocumentUpdateIn, DownloadOut
from app.vault.service import VaultService
from app.vault.storage import build_storage
from app.vault.validation import validate_upload

router = APIRouter(prefix="/documents", tags=["vault"])


def get_vault_service(
    db: Annotated[Session, Depends(get_db)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> VaultService:
    return VaultService(db, build_storage(settings), build_scanner(settings), settings)


@router.get("", response_model=DocumentListOut)
def list_documents(
    auth: Annotated[AuthContext, Depends(get_current_user)],
    vault: Annotated[VaultService, Depends(get_vault_service)],
):
    items = vault.list_documents(auth.user.id)
    return DocumentListOut(items=items, total=len(items))


@router.post("", response_model=DocumentOut, status_code=201)
async def upload_document(
    auth: Annotated[AuthContext, Depends(get_current_user)],
    vault: Annotated[VaultService, Depends(get_vault_service)],
    settings: Annotated[Settings, Depends(get_settings)],
    file: UploadFile = File(...),
    doc_type: str = Form("unclassified"),
    display_name: str | None = Form(None),
):
    content = await file.read()
    validated = validate_upload(
        filename=file.filename or "document",
        content=content,
        declared_content_type=file.content_type,
        settings=settings,
    )
    return vault.upload(
        user_id=auth.user.id,
        validated=validated,
        doc_type=doc_type,
        display_name=display_name,
        ip=auth.ip,
    )


@router.get("/{document_id}", response_model=DocumentOut)
def get_document(
    document_id: UUID,
    auth: Annotated[AuthContext, Depends(get_current_user)],
    vault: Annotated[VaultService, Depends(get_vault_service)],
):
    doc = vault.get_owned_document(auth.user.id, document_id, ip=auth.ip)
    version = vault._current_version(doc)
    from app.vault.service import _to_out

    return _to_out(doc, version)


@router.patch("/{document_id}", response_model=DocumentOut)
def update_document(
    document_id: UUID,
    body: DocumentUpdateIn,
    auth: Annotated[AuthContext, Depends(get_current_user)],
    vault: Annotated[VaultService, Depends(get_vault_service)],
):
    updates = body.model_dump(exclude_unset=True)
    return vault.update_metadata(user_id=auth.user.id, document_id=document_id, updates=updates, ip=auth.ip)


@router.delete("/{document_id}", status_code=204)
def delete_document(
    document_id: UUID,
    auth: Annotated[AuthContext, Depends(get_current_user)],
    vault: Annotated[VaultService, Depends(get_vault_service)],
):
    vault.soft_delete(user_id=auth.user.id, document_id=document_id, ip=auth.ip)
    return Response(status_code=204)


@router.get("/{document_id}/download")
def download_document(
    document_id: UUID,
    auth: Annotated[AuthContext, Depends(get_current_user)],
    vault: Annotated[VaultService, Depends(get_vault_service)],
    settings: Annotated[Settings, Depends(get_settings)],
):
    doc, version, data, url = vault.prepare_download(
        user_id=auth.user.id, document_id=document_id, ip=auth.ip
    )
    if data is not None:
        return Response(
            content=data,
            media_type=version.mime_type,
            headers={
                "Content-Disposition": f'attachment; filename="{version.original_filename}"',
                "X-Content-Type-Options": "nosniff",
                "Cache-Control": "no-store",
            },
        )
    return DownloadOut(
        document_id=doc.id,
        mode="presigned",
        url=url,
        expires_in=settings.download_url_ttl_seconds,
        filename=version.original_filename,
        content_type=version.mime_type,
    )
