from sqlalchemy import ForeignKey, Numeric, String, Text, Enum as SQLAlchemyEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base
from app.models.base_mixins import TimestampMixin, UUIDPrimaryKeyMixin
from app.models.enums import ProjectCategory, ProjectStatus


class Project(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "projects"

    organization_id: Mapped[UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    short_description: Mapped[str] = mapped_column(String(500), nullable=False)
    full_description: Mapped[str] = mapped_column(Text, nullable=True)
    category: Mapped[ProjectCategory] = mapped_column(
        SQLAlchemyEnum(ProjectCategory, values_callable=lambda x: [e.value for e in x]),
        nullable=False,
    )
    status: Mapped[ProjectStatus] = mapped_column(
        SQLAlchemyEnum(ProjectStatus, values_callable=lambda x: [e.value for e in x]),
        default=ProjectStatus.DRAFT,
        nullable=False,
    )
    voivodeship: Mapped[str] = mapped_column(String(100), nullable=True)
    location_general: Mapped[str] = mapped_column(String(255), nullable=True)
    estimated_budget: Mapped[float] = mapped_column(Numeric(14, 2), nullable=True)
    planned_start_date: Mapped[str] = mapped_column(String(20), nullable=True)
    planned_end_date: Mapped[str] = mapped_column(String(20), nullable=True)
    main_risks: Mapped[str] = mapped_column(Text, nullable=True)
    published_at: Mapped[str] = mapped_column(String(40), nullable=True)

    organization = relationship("Organization", back_populates="projects")
    documents = relationship("ProjectDocument", back_populates="project", cascade="all, delete-orphan")
    updates = relationship("ProjectUpdate", back_populates="project", cascade="all, delete-orphan")
    questions = relationship("ProjectQuestion", back_populates="project", cascade="all, delete-orphan")
    interest_declarations = relationship("InterestDeclaration", back_populates="project", cascade="all, delete-orphan")
    watchlist_items = relationship("Watchlist", back_populates="project", cascade="all, delete-orphan")
    verification_cases = relationship("VerificationCase", back_populates="project", cascade="all, delete-orphan")

    @property
    def cover_image_url(self) -> str | None:
        from app.models.enums import DocumentStatus
        from app.services.storage import presigned_get_url
        from app.core.config import get_settings

        candidates = [
            d for d in self.documents
            if d.is_public and d.status == DocumentStatus.APPROVED
        ]
        if not candidates:
            return None
        doc = sorted(candidates, key=lambda d: d.created_at)[0]
        settings = get_settings()
        return presigned_get_url(settings.storage_bucket, doc.storage_key)
