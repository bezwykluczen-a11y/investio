from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.enums import ProjectStatus
from app.models.interactions import InterestDeclaration, ProjectQuestion, Watchlist
from app.models.project import Project
from app.models.user import User
from app.schemas.interactions import (
    InterestDeclarationCreate,
    InterestDeclarationOut,
    ProjectQuestionCreate,
    ProjectQuestionOut,
)

router = APIRouter(prefix="/projects", tags=["interactions"])


def _get_published_project(db: Session, project_id) -> Project:
    project = db.get(Project, project_id)
    if not project or project.status != ProjectStatus.PUBLISHED:
        raise HTTPException(status_code=404, detail="Projekt nie znaleziony")
    return project


@router.post("/{project_id}/interest", response_model=InterestDeclarationOut, status_code=201)
def declare_interest(
    project_id,
    payload: InterestDeclarationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    project = _get_published_project(db, project_id)
    if not payload.consent_risk_disclaimer_accepted:
        raise HTTPException(
            status_code=400,
            detail="Wymagane jest potwierdzenie zapoznania sie z informacja o ryzyku",
        )
    declaration = InterestDeclaration(
        project_id=project.id,
        user_id=current_user.id,
        amount_range=payload.amount_range,
        contact_preference=payload.contact_preference,
        comment=payload.comment,
        consent_marketing=payload.consent_marketing,
        consent_risk_disclaimer_accepted=payload.consent_risk_disclaimer_accepted,
    )
    db.add(declaration)
    db.commit()
    db.refresh(declaration)
    return declaration


@router.post("/{project_id}/watchlist", status_code=201)
def add_to_watchlist(
    project_id,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    project = _get_published_project(db, project_id)
    existing = db.scalar(
        select(Watchlist).where(Watchlist.project_id == project.id, Watchlist.user_id == current_user.id)
    )
    if existing:
        return {"status": "already_watching"}
    db.add(Watchlist(project_id=project.id, user_id=current_user.id))
    db.commit()
    return {"status": "added"}


@router.delete("/{project_id}/watchlist", status_code=200)
def remove_from_watchlist(
    project_id,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    existing = db.scalar(
        select(Watchlist).where(Watchlist.project_id == project_id, Watchlist.user_id == current_user.id)
    )
    if existing:
        db.delete(existing)
        db.commit()
    return {"status": "removed"}


@router.post("/{project_id}/questions", response_model=ProjectQuestionOut, status_code=201)
def ask_question(
    project_id,
    payload: ProjectQuestionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    project = _get_published_project(db, project_id)
    question = ProjectQuestion(project_id=project.id, author_id=current_user.id, question=payload.question)
    db.add(question)
    db.commit()
    db.refresh(question)
    return question


@router.get("/{project_id}/questions", response_model=list[ProjectQuestionOut])
def list_questions(project_id, db: Session = Depends(get_db)):
    stmt = select(ProjectQuestion).where(ProjectQuestion.project_id == project_id)
    return list(db.scalars(stmt))
