import uuid

from pydantic import BaseModel

from app.models.enums import DocumentStatus


class ProjectImageOut(BaseModel):
    id: uuid.UUID
    project_id: uuid.UUID
    file_name: str
    content_type: str
    size_bytes: int
    is_public: bool
    status: DocumentStatus
    url: str | None = None

    class Config:
        from_attributes = True
