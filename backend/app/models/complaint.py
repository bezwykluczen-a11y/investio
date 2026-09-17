import uuid

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base
from app.models.base_mixins import TimestampMixin, UUIDPrimaryKeyMixin


class Complaint(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "complaints"

    last_name: Mapped[str] = mapped_column(String(255), nullable=False)
    first_name: Mapped[str] = mapped_column(String(255), nullable=False)
    company_name: Mapped[str] = mapped_column(String(255), nullable=True)
    registration_number: Mapped[str] = mapped_column(String(255), nullable=True)
    street_address: Mapped[str] = mapped_column(String(500), nullable=True)
    postal_code: Mapped[str] = mapped_column(String(20), nullable=True)
    city: Mapped[str] = mapped_column(String(255), nullable=True)
    country: Mapped[str] = mapped_column(String(100), nullable=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[str] = mapped_column(String(50), nullable=True)

    rep_last_name: Mapped[str] = mapped_column(String(255), nullable=True)
    rep_first_name: Mapped[str] = mapped_column(String(255), nullable=True)
    rep_entity_name: Mapped[str] = mapped_column(String(255), nullable=True)
    rep_registration_number: Mapped[str] = mapped_column(String(255), nullable=True)
    rep_street_address: Mapped[str] = mapped_column(String(500), nullable=True)
    rep_postal_code: Mapped[str] = mapped_column(String(20), nullable=True)
    rep_city: Mapped[str] = mapped_column(String(255), nullable=True)
    rep_country: Mapped[str] = mapped_column(String(100), nullable=True)
    rep_email: Mapped[str] = mapped_column(String(255), nullable=True)
    rep_phone: Mapped[str] = mapped_column(String(50), nullable=True)

    project_reference: Mapped[str] = mapped_column(Text, nullable=True)
    complaint_description: Mapped[str] = mapped_column(Text, nullable=False)
    incident_dates: Mapped[str] = mapped_column(String(255), nullable=True)
    damage_description: Mapped[str] = mapped_column(Text, nullable=True)
    additional_remarks: Mapped[str] = mapped_column(Text, nullable=True)

    status: Mapped[str] = mapped_column(String(30), default="new", server_default="new", nullable=False)
