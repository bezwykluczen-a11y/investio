"""add user profile and notification preference columns

Revision ID: 0002_user_settings
Revises: 0001_initial
Create Date: 2026-08-29

"""
from alembic import op
import sqlalchemy as sa

revision = "0002_user_settings"
down_revision = "0001_initial"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column("notify_email_project_updates", sa.Boolean(), nullable=False, server_default=sa.true()),
    )
    op.add_column(
        "users",
        sa.Column("notify_email_new_projects", sa.Boolean(), nullable=False, server_default=sa.true()),
    )
    op.add_column(
        "users",
        sa.Column("notify_email_marketing", sa.Boolean(), nullable=False, server_default=sa.false()),
    )


def downgrade() -> None:
    op.drop_column("users", "notify_email_marketing")
    op.drop_column("users", "notify_email_new_projects")
    op.drop_column("users", "notify_email_project_updates")
