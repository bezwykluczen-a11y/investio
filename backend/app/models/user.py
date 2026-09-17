from sqlalchemy import Boolean, Enum as SQLAlchemyEnum, String
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

    notify_email_project_updates: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    notify_email_new_projects: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    notify_email_marketing: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    memberships = relationship("OrganizationMember", back_populates="user", cascade="all, delete-orphan")
    watchlist_items = relationship("Watchlist", back_populates="user", cascade="all, delete-orphan")
    interest_declarations = relationship("InterestDeclaration", back_populates="user", cascade="all, delete-orphan")
