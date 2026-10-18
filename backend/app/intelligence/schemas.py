from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class ProcessJobOut(BaseModel):
    id: UUID
    document_id: UUID
    document_version_id: UUID
    status: str
    error_code: str | None = None
    error_message: str | None = None
    started_at: datetime | None = None
    finished_at: datetime | None = None
    created_at: datetime

    model_config = {"from_attributes": True}


class ExtractedFieldOut(BaseModel):
    id: UUID
    field_key: str
    raw_value: str | None
    normalized_value: str | None
    data_type: str
    confidence: str
    validation_result: str
    verification_status: str
    source_page: int | None
    source_text_snippet: str | None
    extraction_method: str
    extracted_at: datetime
    user_corrected_value: str | None
    document_id: UUID
    document_version_id: UUID

    model_config = {"from_attributes": True}


class ExtractionOut(BaseModel):
    id: UUID
    document_id: UUID
    document_version_id: UUID
    predicted_category: str
    category_certainty: str
    user_category: str | None
    effective_category: str
    extraction_method: str
    page_count: int | None
    fields: list[ExtractedFieldOut]
    job_status: str


class ClassificationUpdateIn(BaseModel):
    category: str = Field(min_length=3, max_length=64)


class FieldReviewIn(BaseModel):
    action: str = Field(pattern="^(confirm|correct|reject)$")
    value: str | None = None


class ProfileFieldOut(BaseModel):
    id: UUID
    field_key: str
    value: str | None
    data_type: str
    verification_state: str
    source_document_id: UUID | None
    source_document_version_id: UUID | None
    source_extracted_field_id: UUID | None
    original_extracted_value: str | None
    user_corrected: bool
    conflict_candidates_json: str | None
    updated_at: datetime

    model_config = {"from_attributes": True}


class ProfileOut(BaseModel):
    id: UUID
    user_id: UUID
    version: int
    updated_at: datetime
    fields: list[ProfileFieldOut]


class ProfileFieldUpdateIn(BaseModel):
    value: str = Field(min_length=1, max_length=500)
    verify: bool = True


class ConflictResolveIn(BaseModel):
    field_key: str
    value: str = Field(min_length=1, max_length=500)
    source_extracted_field_id: UUID | None = None
