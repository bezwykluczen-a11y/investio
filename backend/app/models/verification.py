from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base
from app.models.base_mixins import TimestampMixin, UUIDPrimaryKeyMixin


class VerificationCase(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "verification_cases"

    project_id: Mapped[UUID] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    assigned_to_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=True)
    completeness_score: Mapped[int] = mapped_column(default=0, nullable=False)
    notes: Mapped[str] = mapped_column(Text, nullable=True)
    is_closed: Mapped[bool] = mapped_column(default=False, nullable=False)

    project = relationship("Project", back_populates="verification_cases")


class AuditEvent(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "audit_events"

    actor_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=True)
    entity_type: Mapped[str] = mapped_column(String(100), nullable=False)
    entity_id: Mapped[str] = mapped_column(String(64), nullable=False)
    action: Mapped[str] = mapped_column(String(100), nullable=False)
    from_status: Mapped[str] = mapped_column(String(50), nullable=True)
    to_status: Mapped[str] = mapped_column(String(50), nullable=True)
    comment: Mapped[str] = mapped_column(Text, nullable=True)
