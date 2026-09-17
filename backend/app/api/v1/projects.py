from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_roles
from app.db.session import get_db
from app.models.enums import ProjectCategory, ProjectStatus, UserRole
from app.models.organization import Organization, OrganizationMember
from app.models.project import Project
from app.models.user import User
from app.schemas.project import (
    ProjectCreate,
    ProjectDetailOut,
    ProjectOut,
    ProjectUpdatePayload,
    StatusChangeRequest,
)
from app.services.audit import log_audit_event
from app.services.slug import unique_slug

router = APIRouter(prefix="/projects", tags=["projects"])

ALLOWED_TRANSITIONS: dict[ProjectStatus, set[ProjectStatus]] = {
    ProjectStatus.DRAFT: {ProjectStatus.SUBMITTED},
    ProjectStatus.SUBMITTED: {ProjectStatus.IN_REVIEW, ProjectStatus.NEEDS_CHANGES},
    ProjectStatus.IN_REVIEW: {ProjectStatus.VERIFIED, ProjectStatus.NEEDS_CHANGES, ProjectStatus.REJECTED},
    ProjectStatus.NEEDS_CHANGES: {ProjectStatus.SUBMITTED},
    ProjectStatus.VERIFIED: {ProjectStatus.PUBLISHED, ProjectStatus.NEEDS_CHANGES},
    ProjectStatus.PUBLISHED: {ProjectStatus.PAUSED, ProjectStatus.COMPLETED},
    ProjectStatus.PAUSED: {ProjectStatus.PUBLISHED, ProjectStatus.COMPLETED},
    ProjectStatus.COMPLETED: set(),
    ProjectStatus.REJECTED: set(),
}


@router.get("", response_model=list[ProjectOut])
def list_public_projects(
    category: ProjectCategory | None = Query(default=None),
    voivodeship: str | None = Query(default=None),
    db: Session = Depends(get_db),
):
    stmt = select(Project).where(Project.status == ProjectStatus.PUBLISHED)
    if category:
        stmt = stmt.where(Project.category == category)
    if voivodeship:
        stmt = stmt.where(Project.voivodeship == voivodeship)
    return list(db.scalars(stmt))


@router.get("/{slug}", response_model=ProjectDetailOut)
def get_project_by_slug(slug: str, db: Session = Depends(get_db)):
    project = db.scalar(select(Project).where(Project.slug == slug))
    if not project or project.status != ProjectStatus.PUBLISHED:
        raise HTTPException(status_code=404, detail="Projekt nie znaleziony")
    return project


@router.post("/organizations/{organization_id}", response_model=ProjectDetailOut, status_code=201)
def create_project(
    organization_id,
    payload: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.MODERATOR, UserRole.ADMIN)),
):
    org = db.get(Organization, organization_id)
    if not org:
        raise HTTPException(status_code=404, detail="Organizacja nie znaleziona")

    slug = unique_slug(db, Project, payload.title)

    initial_status = ProjectStatus.PUBLISHED
    published_at = datetime.now(timezone.utc).isoformat()

    project = Project(
        organization_id=organization_id,
        title=payload.title,
        slug=slug,
        short_description=payload.short_description,
        full_description=payload.full_description,
        category=payload.category,
        voivodeship=payload.voivodeship,
        location_general=payload.location_general,
        estimated_budget=payload.estimated_budget,
        planned_start_date=payload.planned_start_date,
        planned_end_date=payload.planned_end_date,
        main_risks=payload.main_risks,
        status=initial_status,
        published_at=published_at,
    )
    db.add(project)
    db.commit()
    db.refresh(project)
    log_audit_event(
        db, current_user.id, "project", str(project.id), "created_published",
        to_status=initial_status.value,
    )
    return project


@router.patch("/{project_id}", response_model=ProjectDetailOut)
def update_project(
    project_id,
    payload: ProjectUpdatePayload,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.MODERATOR, UserRole.ADMIN)),
):
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Projekt nie znaleziony")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(project, field, value)
    db.commit()
    db.refresh(project)
    return project


@router.delete("/{project_id}", status_code=204)
def delete_project(
    project_id,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.MODERATOR, UserRole.ADMIN)),
):
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Projekt nie znaleziony")
    db.delete(project)
    db.commit()
    log_audit_event(db, current_user.id, "project", str(project_id), "deleted")


@router.post("/{project_id}/submit", response_model=ProjectDetailOut)
def submit_project(
    project_id,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.MODERATOR, UserRole.ADMIN)),
):
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Projekt nie znaleziony")

    if ProjectStatus.SUBMITTED not in ALLOWED_TRANSITIONS.get(project.status, set()):
        raise HTTPException(status_code=400, detail="Nie mozna zglosic projektu z obecnego statusu")

    old_status = project.status
    project.status = ProjectStatus.SUBMITTED
    db.commit()
    log_audit_event(
        db, current_user.id, "project", str(project.id), "status_change",
        from_status=old_status.value, to_status=project.status.value,
    )
    db.refresh(project)
    return project


@router.post("/{project_id}/status", response_model=ProjectDetailOut)
def change_project_status(
    project_id,
    payload: StatusChangeRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.MODERATOR, UserRole.ADMIN)),
):
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Projekt nie znaleziony")

    allowed = ALLOWED_TRANSITIONS.get(project.status, set())
    if payload.new_status not in allowed:
        raise HTTPException(
            status_code=400,
            detail=f"Niedozwolone przejscie statusu z {project.status.value} do {payload.new_status.value}",
        )

    old_status = project.status
    project.status = payload.new_status
    db.commit()
    log_audit_event(
        db, current_user.id, "project", str(project.id), "status_change",
        from_status=old_status.value, to_status=payload.new_status.value, comment=payload.comment,
    )
    db.refresh(project)
    return project
