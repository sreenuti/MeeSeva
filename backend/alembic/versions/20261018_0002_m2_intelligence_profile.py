"""M2 document intelligence and citizen profile

Revision ID: 20261018_0002
Revises: 20261018_0001
Create Date: 2026-10-18
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "20261018_0002"
down_revision: Union[str, None] = "20261018_0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "document_processing_jobs",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("document_id", sa.Uuid(), nullable=False),
        sa.Column("document_version_id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("error_code", sa.String(length=64), nullable=True),
        sa.Column("error_message", sa.String(length=255), nullable=True),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("finished_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["document_id"], ["documents.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["document_version_id"], ["document_versions.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("document_version_id", name="uq_processing_job_version"),
    )
    op.create_index("ix_document_processing_jobs_document_id", "document_processing_jobs", ["document_id"])
    op.create_index("ix_document_processing_jobs_user_id", "document_processing_jobs", ["user_id"])
    op.create_index("ix_document_processing_jobs_status", "document_processing_jobs", ["status"])

    op.create_table(
        "document_extractions",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("job_id", sa.Uuid(), nullable=False),
        sa.Column("document_id", sa.Uuid(), nullable=False),
        sa.Column("document_version_id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("predicted_category", sa.String(length=64), nullable=False),
        sa.Column("category_certainty", sa.String(length=32), nullable=False),
        sa.Column("user_category", sa.String(length=64), nullable=True),
        sa.Column("extraction_method", sa.String(length=64), nullable=False),
        sa.Column("page_count", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["job_id"], ["document_processing_jobs.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("job_id"),
    )
    op.create_index("ix_document_extractions_document_id", "document_extractions", ["document_id"])
    op.create_index("ix_document_extractions_document_version_id", "document_extractions", ["document_version_id"])
    op.create_index("ix_document_extractions_user_id", "document_extractions", ["user_id"])

    op.create_table(
        "extracted_fields",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("extraction_id", sa.Uuid(), nullable=False),
        sa.Column("document_id", sa.Uuid(), nullable=False),
        sa.Column("document_version_id", sa.Uuid(), nullable=False),
        sa.Column("field_key", sa.String(length=64), nullable=False),
        sa.Column("raw_value", sa.Text(), nullable=True),
        sa.Column("normalized_value", sa.Text(), nullable=True),
        sa.Column("data_type", sa.String(length=32), nullable=False),
        sa.Column("confidence", sa.String(length=32), nullable=False),
        sa.Column("validation_result", sa.String(length=32), nullable=False),
        sa.Column("verification_status", sa.String(length=32), nullable=False),
        sa.Column("source_page", sa.Integer(), nullable=True),
        sa.Column("source_text_snippet", sa.String(length=240), nullable=True),
        sa.Column("extraction_method", sa.String(length=64), nullable=False),
        sa.Column("extracted_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("user_corrected_value", sa.Text(), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["extraction_id"], ["document_extractions.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_extracted_fields_extraction_id", "extracted_fields", ["extraction_id"])
    op.create_index("ix_extracted_fields_document_id", "extracted_fields", ["document_id"])
    op.create_index("ix_extracted_fields_document_version_id", "extracted_fields", ["document_version_id"])

    op.create_table(
        "citizen_profiles",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id", name="uq_citizen_profile_user"),
    )

    op.create_table(
        "profile_fields",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("profile_id", sa.Uuid(), nullable=False),
        sa.Column("field_key", sa.String(length=64), nullable=False),
        sa.Column("value", sa.Text(), nullable=True),
        sa.Column("data_type", sa.String(length=32), nullable=False),
        sa.Column("verification_state", sa.String(length=32), nullable=False),
        sa.Column("source_document_id", sa.Uuid(), nullable=True),
        sa.Column("source_document_version_id", sa.Uuid(), nullable=True),
        sa.Column("source_extracted_field_id", sa.Uuid(), nullable=True),
        sa.Column("original_extracted_value", sa.Text(), nullable=True),
        sa.Column("user_corrected", sa.Boolean(), nullable=False),
        sa.Column("conflict_candidates_json", sa.Text(), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["profile_id"], ["citizen_profiles.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("profile_id", "field_key", name="uq_profile_field_key"),
    )
    op.create_index("ix_profile_fields_profile_id", "profile_fields", ["profile_id"])


def downgrade() -> None:
    op.drop_index("ix_profile_fields_profile_id", table_name="profile_fields")
    op.drop_table("profile_fields")
    op.drop_table("citizen_profiles")
    op.drop_index("ix_extracted_fields_document_version_id", table_name="extracted_fields")
    op.drop_index("ix_extracted_fields_document_id", table_name="extracted_fields")
    op.drop_index("ix_extracted_fields_extraction_id", table_name="extracted_fields")
    op.drop_table("extracted_fields")
    op.drop_index("ix_document_extractions_user_id", table_name="document_extractions")
    op.drop_index("ix_document_extractions_document_version_id", table_name="document_extractions")
    op.drop_index("ix_document_extractions_document_id", table_name="document_extractions")
    op.drop_table("document_extractions")
    op.drop_index("ix_document_processing_jobs_status", table_name="document_processing_jobs")
    op.drop_index("ix_document_processing_jobs_user_id", table_name="document_processing_jobs")
    op.drop_index("ix_document_processing_jobs_document_id", table_name="document_processing_jobs")
    op.drop_table("document_processing_jobs")
