import uuid
from pydantic import BaseModel, Field


class OrganizationCreate(BaseModel):
    name: str = Field(min_length=2, max_length=255)
    legal_name: str | None = None
    nip: str | None = Field(default=None, max_length=20)
    krs: str | None = Field(default=None, max_length=20)
    description: str | None = None


class OrganizationOut(BaseModel):
    id: uuid.UUID
    name: str
    slug: str
    legal_name: str | None
    is_verified: bool

    class Config:
        from_attributes = True
