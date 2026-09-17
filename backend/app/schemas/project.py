import uuid
from decimal import Decimal
from pydantic import BaseModel, Field

from app.models.enums import ProjectCategory, ProjectStatus


class ProjectCreate(BaseModel):
    title: str = Field(min_length=3, max_length=255)
    short_description: str = Field(min_length=10, max_length=500)
    full_description: str | None = None
    category: ProjectCategory
    voivodeship: str | None = None
    location_general: str | None = None
    estimated_budget: Decimal | None = None
    cover_image_url: str | None = None
    planned_start_date: str | None = None
    planned_end_date: str | None = None
    main_risks: str | None = None


class ProjectUpdatePayload(BaseModel):
    title: str | None = None
    short_description: str | None = None
    full_description: str | None = None
    category: ProjectCategory | None = None
    voivodeship: str | None = None
    location_general: str | None = None
    estimated_budget: Decimal | None = None
    cover_image_url: str | None = None
    planned_start_date: str | None = None
    planned_end_date: str | None = None
    main_risks: str | None = None


class ProjectOut(BaseModel):
    id: uuid.UUID
    organization_id: uuid.UUID
    title: str
    slug: str
    short_description: str
    category: ProjectCategory
    status: ProjectStatus
    voivodeship: str | None
    location_general: str | None
    estimated_budget: Decimal | None
    cover_image_url: str | None = None

    class Config:
        from_attributes = True


class ProjectDetailOut(ProjectOut):
    full_description: str | None
    main_risks: str | None
    planned_start_date: str | None
    planned_end_date: str | None


class StatusChangeRequest(BaseModel):
    new_status: ProjectStatus
    comment: str | None = None
