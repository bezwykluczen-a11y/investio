from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import require_roles
from app.db.session import get_db
from app.models.enums import ProjectStatus, UserRole
from app.models.project import Project
from app.models.verification import AuditEvent
from app.schemas.project import ProjectOut

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/projects", response_model=list[ProjectOut])
def list_all_projects(
    status_filter: ProjectStatus | None = None,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(UserRole.ANALYST, UserRole.MODERATOR, UserRole.ADMIN)),
):
    stmt = select(Project)
    if status_filter:
        stmt = stmt.where(Project.status == status_filter)
    return list(db.scalars(stmt))


@router.get("/audit-events")
def list_audit_events(
    entity_type: str | None = None,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(UserRole.ADMIN)),
):
    stmt = select(AuditEvent).order_by(AuditEvent.created_at.desc()).limit(limit)
    if entity_type:
        stmt = stmt.where(AuditEvent.entity_type == entity_type)
    events = list(db.scalars(stmt))
    return [
        {
            "id": str(e.id),
            "actor_id": str(e.actor_id) if e.actor_id else None,
            "entity_type": e.entity_type,
            "entity_id": e.entity_id,
            "action": e.action,
            "from_status": e.from_status,
            "to_status": e.to_status,
            "comment": e.comment,
            "created_at": e.created_at.isoformat(),
        }
        for e in events
    ]
