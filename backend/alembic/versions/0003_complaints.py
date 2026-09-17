"""add complaints table

Revision ID: 0003_complaints
Revises: 0002_user_settings
Create Date: 2026-09-17

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0003_complaints"
down_revision = "0002_user_settings"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "complaints",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("last_name", sa.String(255), nullable=False),
        sa.Column("first_name", sa.String(255), nullable=False),
        sa.Column("company_name", sa.String(255), nullable=True),
        sa.Column("registration_number", sa.String(255), nullable=True),
        sa.Column("street_address", sa.String(500), nullable=True),
        sa.Column("postal_code", sa.String(20), nullable=True),
        sa.Column("city", sa.String(255), nullable=True),
        sa.Column("country", sa.String(100), nullable=True),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column("phone", sa.String(50), nullable=True),
        sa.Column("rep_last_name", sa.String(255), nullable=True),
        sa.Column("rep_first_name", sa.String(255), nullable=True),
        sa.Column("rep_entity_name", sa.String(255), nullable=True),
        sa.Column("rep_registration_number", sa.String(255), nullable=True),
        sa.Column("rep_street_address", sa.String(500), nullable=True),
        sa.Column("rep_postal_code", sa.String(20), nullable=True),
        sa.Column("rep_city", sa.String(255), nullable=True),
        sa.Column("rep_country", sa.String(100), nullable=True),
        sa.Column("rep_email", sa.String(255), nullable=True),
        sa.Column("rep_phone", sa.String(50), nullable=True),
        sa.Column("project_reference", sa.Text(), nullable=True),
        sa.Column("complaint_description", sa.Text(), nullable=False),
        sa.Column("incident_dates", sa.String(255), nullable=True),
        sa.Column("damage_description", sa.Text(), nullable=True),
        sa.Column("additional_remarks", sa.Text(), nullable=True),
        sa.Column("status", sa.String(30), server_default="new", nullable=False),
    )


def downgrade() -> None:
    op.drop_table("complaints")
