import uuid

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import require_roles
from app.core.config import get_settings
from app.db.session import get_db
from app.models.documents import ProjectDocument
from app.models.enums import DocumentStatus, UserRole
from app.models.project import Project
from app.models.user import User
from app.schemas.documents import ProjectImageOut
from app.services.audit import log_audit_event
from app.services.storage import (
    ALLOWED_IMAGE_TYPES,
    build_storage_key,
    delete_object,
    ensure_bucket_exists,
    presigned_get_url,
    sha256_of,
    upload_bytes,
)

router = APIRouter(prefix="/projects", tags=["project-images"])


@router.post("/{project_id}/images", response_model=ProjectImageOut, status_code=201)
async def upload_project_image(
    project_id: uuid.UUID,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.MODERATOR, UserRole.ADMIN)),
):
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Projekt nie znaleziony")

    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Niedozwolony typ pliku. Dozwolone: {', '.join(ALLOWED_IMAGE_TYPES)}",
        )

    settings = get_settings()
    data = await file.read()
    size_mb = len(data) / (1024 * 1024)
    if size_mb > settings.max_upload_mb:
        raise HTTPException(
            status_code=400,
            detail=f"Plik przekracza maksymalny rozmiar {settings.max_upload_mb} MB",
        )
    if len(data) == 0:
        raise HTTPException(status_code=400, detail="Plik jest pusty")

    extension = ALLOWED_IMAGE_TYPES[file.content_type]
    storage_key = build_storage_key(project_id, extension)

    ensure_bucket_exists(settings.storage_bucket)
    upload_bytes(settings.storage_bucket, storage_key, data, file.content_type)

    document = ProjectDocument(
        project_id=project_id,
        file_name=file.filename or f"image.{extension}",
        storage_key=storage_key,
        checksum_sha256=sha256_of(data),
        content_type=file.content_type,
        size_bytes=len(data),
        is_public=True,
        status=DocumentStatus.APPROVED,
        uploaded_by_id=current_user.id,
    )
    db.add(document)
    db.commit()
    db.refresh(document)

    log_audit_event(
        db, current_user.id, "project_document", str(document.id), "uploaded",
        comment=f"project_id={project_id}",
    )

    result = ProjectImageOut.model_validate(document)
    result.url = presigned_get_url(settings.storage_bucket, storage_key)
    return result


@router.get("/{project_id}/images", response_model=list[ProjectImageOut])
def list_project_images(
    project_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Projekt nie znaleziony")

    stmt = (
        select(ProjectDocument)
        .where(ProjectDocument.project_id == project_id)
        .where(ProjectDocument.is_public.is_(True))
        .where(ProjectDocument.status == DocumentStatus.APPROVED)
        .order_by(ProjectDocument.created_at.asc())
    )
    documents = list(db.scalars(stmt))

    settings = get_settings()
    results = []
    for doc in documents:
        item = ProjectImageOut.model_validate(doc)
        item.url = presigned_get_url(settings.storage_bucket, doc.storage_key)
        results.append(item)
    return results


@router.delete("/{project_id}/images/{image_id}", status_code=204)
def delete_project_image(
    project_id: uuid.UUID,
    image_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.MODERATOR, UserRole.ADMIN)),
):
    document = db.get(ProjectDocument, image_id)
    if not document or document.project_id != project_id:
        raise HTTPException(status_code=404, detail="Zdjecie nie znalezione")

    settings = get_settings()
    delete_object(settings.storage_bucket, document.storage_key)
    db.delete(document)
    db.commit()

    log_audit_event(
        db, current_user.id, "project_document", str(image_id), "deleted",
        comment=f"project_id={project_id}",
    )
