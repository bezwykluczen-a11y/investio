from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr


class ComplaintCreate(BaseModel):
    last_name: str
    first_name: str
    company_name: str | None = None
    registration_number: str | None = None
    street_address: str | None = None
    postal_code: str | None = None
    city: str | None = None
    country: str | None = None
    email: EmailStr
    phone: str | None = None

    rep_last_name: str | None = None
    rep_first_name: str | None = None
    rep_entity_name: str | None = None
    rep_registration_number: str | None = None
    rep_street_address: str | None = None
    rep_postal_code: str | None = None
    rep_city: str | None = None
    rep_country: str | None = None
    rep_email: EmailStr | None = None
    rep_phone: str | None = None

    project_reference: str | None = None
    complaint_description: str
    incident_dates: str | None = None
    damage_description: str | None = None
    additional_remarks: str | None = None


class ComplaintOut(BaseModel):
    id: UUID
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
