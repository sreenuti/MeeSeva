from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, Field


class DocumentOut(BaseModel):
    id: UUID
    display_name: str
    doc_type: str
    status: str
    expires_on: date | None
    mime_type: str | None = None
    byte_size: int | None = None
    scan_status: str | None = None
    created_at: datetime
    downloadable: bool = False

    model_config = {"from_attributes": True}


class DocumentListOut(BaseModel):
    items: list[DocumentOut]
    total: int


class DocumentUpdateIn(BaseModel):
    display_name: str | None = Field(default=None, min_length=1, max_length=255)
    doc_type: str | None = Field(default=None, min_length=1, max_length=64)
    expires_on: date | None = None


class DownloadOut(BaseModel):
    document_id: UUID
    mode: str
    url: str | None = None
    expires_in: int | None = None
    filename: str
    content_type: str
