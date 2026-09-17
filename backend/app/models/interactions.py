from sqlalchemy import ForeignKey, String, Text, Enum as SQLAlchemyEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base
from app.models.base_mixins import TimestampMixin, UUIDPrimaryKeyMixin
from app.models.enums import QuestionStatus


class ProjectQuestion(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "project_questions"

    project_id: Mapped[UUID] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    author_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    question: Mapped[str] = mapped_column(Text, nullable=False)
    answer: Mapped[str] = mapped_column(Text, nullable=True)
    status: Mapped[QuestionStatus] = mapped_column(
        SQLAlchemyEnum(QuestionStatus, values_callable=lambda x: [e.value for e in x]),
        default=QuestionStatus.OPEN,
        nullable=False,
    )

    project = relationship("Project", back_populates="questions")


class InterestDeclaration(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Deklaracja zainteresowania - NIE jest zobowiazaniem finansowym."""
    __tablename__ = "interest_declarations"

    project_id: Mapped[UUID] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    amount_range: Mapped[str] = mapped_column(String(50), nullable=False)
    contact_preference: Mapped[str] = mapped_column(String(50), nullable=False)
    comment: Mapped[str] = mapped_column(Text, nullable=True)
    consent_marketing: Mapped[bool] = mapped_column(default=False, nullable=False)
    consent_risk_disclaimer_accepted: Mapped[bool] = mapped_column(default=False, nullable=False)

    project = relationship("Project", back_populates="interest_declarations")
    user = relationship("User", back_populates="interest_declarations")


class Watchlist(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "watchlists"

    project_id: Mapped[UUID] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    project = relationship("Project", back_populates="watchlist_items")
    user = relationship("User", back_populates="watchlist_items")
