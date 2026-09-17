import uuid
from sqlalchemy.orm import Session

from app.models.verification import AuditEvent


def log_audit_event(
    db: Session,
    actor_id: uuid.UUID | None,
    entity_type: str,
    entity_id: str,
    action: str,
    from_status: str | None = None,
    to_status: str | None = None,
    comment: str | None = None,
) -> AuditEvent:
    event = AuditEvent(
        actor_id=actor_id,
        entity_type=entity_type,
        entity_id=str(entity_id),
        action=action,
        from_status=from_status,
        to_status=to_status,
        comment=comment,
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event
