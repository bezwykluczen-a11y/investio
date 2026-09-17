#!/usr/bin/env python3
"""
Naprawia blad enumow: SQLAlchemy wysyla do PostgreSQL nazwy pol
enuma (USER, ADMIN, DRAFT) zamiast wartosci (user, admin, draft),
co powoduje "invalid input value for enum userrole: USER".

Rozwiazanie: dodajemy values_callable=lambda x: [e.value for e in x]
do kazdej kolumny enum w modelach, aby SQLAlchemy mapowal enumy
na wartosci (male litery), ktore istnieja w typach PostgreSQL.

Uzycie: uruchom WEWNATRZ folderu mvp-portal-projektow:

    cd mvp-portal-projektow
    python3 fix_enum_values.py
    docker compose up -d api

Po zastosowaniu:
    otworz http://localhost:8000/docs i przetestuj POST /api/v1/auth/register
"""
import os

FILES: dict[str, str] = {}

FILES["backend/app/models/user.py"] = '''from sqlalchemy import Boolean, Enum as SQLAlchemyEnum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base
from app.models.base_mixins import TimestampMixin, UUIDPrimaryKeyMixin
from app.models.enums import UserRole


class User(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(
        SQLAlchemyEnum(UserRole, values_callable=lambda x: [e.value for e in x]),
        default=UserRole.USER,
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_mfa_enabled: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    memberships = relationship("OrganizationMember", back_populates="user", cascade="all, delete-orphan")
    watchlist_items = relationship("Watchlist", back_populates="user", cascade="all, delete-orphan")
    interest_declarations = relationship("InterestDeclaration", back_populates="user", cascade="all, delete-orphan")
'''

FILES["backend/app/models/project.py"] = '''from sqlalchemy import ForeignKey, Numeric, String, Text, Enum as SQLAlchemyEnum
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
'''

FILES["backend/app/models/documents.py"] = '''from sqlalchemy import ForeignKey, String, Enum as SQLAlchemyEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base
from app.models.base_mixins import TimestampMixin, UUIDPrimaryKeyMixin
from app.models.enums import DocumentStatus


class ProjectDocument(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "project_documents"

    project_id: Mapped[UUID] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    file_name: Mapped[str] = mapped_column(String(255), nullable=False)
    storage_key: Mapped[str] = mapped_column(String(500), nullable=False)
    checksum_sha256: Mapped[str] = mapped_column(String(64), nullable=False)
    content_type: Mapped[str] = mapped_column(String(100), nullable=False)
    size_bytes: Mapped[int] = mapped_column(nullable=False)
    is_public: Mapped[bool] = mapped_column(default=False, nullable=False)
    status: Mapped[DocumentStatus] = mapped_column(
        SQLAlchemyEnum(DocumentStatus, values_callable=lambda x: [e.value for e in x]),
        default=DocumentStatus.PENDING,
        nullable=False,
    )
    version: Mapped[int] = mapped_column(default=1, nullable=False)
    uploaded_by_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False)

    project = relationship("Project", back_populates="documents")


class ProjectUpdate(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "project_updates"

    project_id: Mapped[UUID] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    body: Mapped[str] = mapped_column(nullable=False)
    author_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False)

    project = relationship("Project", back_populates="updates")
'''

FILES["backend/app/models/interactions.py"] = '''from sqlalchemy import ForeignKey, String, Text, Enum as SQLAlchemyEnum
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
'''


def main() -> None:
    if not os.path.exists("docker-compose.yml"):
        print("UWAGA: nie widze docker-compose.yml w tym katalogu.")
        print("Upewnij sie, ze uruchamiasz skrypt wewnatrz folderu mvp-portal-projektow.")
        return

    for rel_path, content in FILES.items():
        with open(rel_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  napisano: {rel_path}")

    print("\\nNastepne kroki:")
    print("  docker compose up -d api")
    print("  (backend jest montowany jako wolumen, wiec zmiana jest widoczna")
    print("   od razu po restarcie kontenera - bez rebuilda obrazu)")
    print("\\nPo restarcie:")
    print("  otworz http://localhost:8000/docs")
    print("  przetestuj POST /api/v1/auth/register")


if __name__ == "__main__":
    main()
