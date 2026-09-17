from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_roles
from app.db.session import get_db
from app.models.enums import UserRole
from app.models.organization import Organization, OrganizationMember
from app.models.user import User
from app.schemas.organization import OrganizationCreate, OrganizationOut
from app.services.slug import unique_slug

router = APIRouter(prefix="/organizations", tags=["organizations"])


@router.post("", response_model=OrganizationOut, status_code=201)
def create_organization(
    payload: OrganizationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.MODERATOR, UserRole.ADMIN)),
):
    slug = unique_slug(db, Organization, payload.name)
    org = Organization(
        name=payload.name,
        slug=slug,
        legal_name=payload.legal_name,
        nip=payload.nip,
        krs=payload.krs,
        description=payload.description,
    )
    db.add(org)
    db.flush()
    membership = OrganizationMember(organization_id=org.id, user_id=current_user.id, role_in_org="owner")
    db.add(membership)
    db.commit()
    db.refresh(org)
    return org


@router.get("/{slug}", response_model=OrganizationOut)
def get_organization(slug: str, db: Session = Depends(get_db)):
    org = db.scalar(select(Organization).where(Organization.slug == slug))
    if not org:
        raise HTTPException(status_code=404, detail="Organizacja nie znaleziona")
    return org


@router.get("/me/list", response_model=list[OrganizationOut])
def list_my_organizations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    stmt = (
        select(Organization)
        .join(OrganizationMember, OrganizationMember.organization_id == Organization.id)
        .where(OrganizationMember.user_id == current_user.id)
    )
    return list(db.scalars(stmt))
