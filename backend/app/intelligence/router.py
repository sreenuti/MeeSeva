from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy.orm import Session

from app.config import Settings, get_settings
from app.db import SessionLocal, get_db
from app.identity.deps import AuthContext, get_current_user
from app.intelligence.pipeline import IntelligencePipeline
from app.intelligence.profile_service import ProfileService
from app.intelligence.schemas import (
    ClassificationUpdateIn,
    ConflictResolveIn,
    ExtractionOut,
    ExtractedFieldOut,
    FieldReviewIn,
    ProcessJobOut,
    ProfileFieldOut,
    ProfileFieldUpdateIn,
    ProfileOut,
)
from app.vault.storage import build_storage

router = APIRouter(tags=["intelligence"])


def get_pipeline(
    db: Annotated[Session, Depends(get_db)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> IntelligencePipeline:
    return IntelligencePipeline(db, build_storage(settings), settings)


def get_profile_service(db: Annotated[Session, Depends(get_db)]) -> ProfileService:
    return ProfileService(db)


def _run_job(job_id: UUID) -> None:
    settings = get_settings()
    db = SessionLocal()
    try:
        pipeline = IntelligencePipeline(db, build_storage(settings), settings)
        pipeline.process_job(job_id)
    finally:
        db.close()


@router.post("/documents/{document_id}/process", response_model=ProcessJobOut)
def start_processing(
    document_id: UUID,
    background_tasks: BackgroundTasks,
    auth: Annotated[AuthContext, Depends(get_current_user)],
    pipeline: Annotated[IntelligencePipeline, Depends(get_pipeline)],
    settings: Annotated[Settings, Depends(get_settings)],
):
    job = pipeline.enqueue(user_id=auth.user.id, document_id=document_id, ip=auth.ip)
    if job.status == "queued":
        if settings.environment == "test":
            # Deterministic for tests: process inline
            job = pipeline.process_job(job.id)
        else:
            background_tasks.add_task(_run_job, job.id)
    return job


@router.get("/documents/{document_id}/process", response_model=ProcessJobOut)
def get_processing_status(
    document_id: UUID,
    auth: Annotated[AuthContext, Depends(get_current_user)],
    pipeline: Annotated[IntelligencePipeline, Depends(get_pipeline)],
):
    return pipeline.get_job_for_owner(auth.user.id, document_id, ip=auth.ip)


@router.get("/documents/{document_id}/extraction", response_model=ExtractionOut)
def get_extraction(
    document_id: UUID,
    auth: Annotated[AuthContext, Depends(get_current_user)],
    pipeline: Annotated[IntelligencePipeline, Depends(get_pipeline)],
):
    job = pipeline.get_job_for_owner(auth.user.id, document_id, ip=auth.ip)
    extraction = pipeline.get_extraction_for_owner(auth.user.id, document_id, ip=auth.ip)
    effective = extraction.user_category or extraction.predicted_category
    return ExtractionOut(
        id=extraction.id,
        document_id=extraction.document_id,
        document_version_id=extraction.document_version_id,
        predicted_category=extraction.predicted_category,
        category_certainty=extraction.category_certainty,
        user_category=extraction.user_category,
        effective_category=effective,
        extraction_method=extraction.extraction_method,
        page_count=extraction.page_count,
        fields=[ExtractedFieldOut.model_validate(f) for f in extraction.fields],
        job_status=job.status,
    )


@router.patch("/documents/{document_id}/classification", response_model=ExtractionOut)
def update_classification(
    document_id: UUID,
    body: ClassificationUpdateIn,
    auth: Annotated[AuthContext, Depends(get_current_user)],
    pipeline: Annotated[IntelligencePipeline, Depends(get_pipeline)],
):
    pipeline.update_classification(
        user_id=auth.user.id, document_id=document_id, category=body.category, ip=auth.ip
    )
    return get_extraction(document_id, auth, pipeline)


@router.post("/extracted-fields/{field_id}/review", response_model=ExtractedFieldOut)
def review_field(
    field_id: UUID,
    body: FieldReviewIn,
    auth: Annotated[AuthContext, Depends(get_current_user)],
    profiles: Annotated[ProfileService, Depends(get_profile_service)],
):
    field = profiles.review_extracted_field(
        user_id=auth.user.id,
        field_id=field_id,
        action=body.action,
        value=body.value,
        ip=auth.ip,
    )
    return field


@router.get("/profile", response_model=ProfileOut)
def get_profile(
    auth: Annotated[AuthContext, Depends(get_current_user)],
    profiles: Annotated[ProfileService, Depends(get_profile_service)],
):
    profile = profiles.get_profile(auth.user.id)
    return ProfileOut(
        id=profile.id,
        user_id=profile.user_id,
        version=profile.version,
        updated_at=profile.updated_at,
        fields=[ProfileFieldOut.model_validate(f) for f in profile.fields],
    )


@router.patch("/profile/fields/{field_key}", response_model=ProfileFieldOut)
def update_profile_field(
    field_key: str,
    body: ProfileFieldUpdateIn,
    auth: Annotated[AuthContext, Depends(get_current_user)],
    profiles: Annotated[ProfileService, Depends(get_profile_service)],
):
    return profiles.update_profile_field(
        user_id=auth.user.id,
        field_key=field_key,
        value=body.value,
        verify=body.verify,
        ip=auth.ip,
    )


@router.get("/profile/conflicts", response_model=list[ProfileFieldOut])
def list_conflicts(
    auth: Annotated[AuthContext, Depends(get_current_user)],
    profiles: Annotated[ProfileService, Depends(get_profile_service)],
):
    return profiles.list_conflicts(auth.user.id)


@router.post("/profile/conflicts/resolve", response_model=ProfileFieldOut)
def resolve_conflict(
    body: ConflictResolveIn,
    auth: Annotated[AuthContext, Depends(get_current_user)],
    profiles: Annotated[ProfileService, Depends(get_profile_service)],
):
    return profiles.resolve_conflict(
        user_id=auth.user.id,
        field_key=body.field_key,
        value=body.value,
        source_extracted_field_id=body.source_extracted_field_id,
        ip=auth.ip,
    )
