from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.security import hash_password, verify_password
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import (
    NotificationPreferencesPayload,
    PasswordChangePayload,
    ProfileUpdatePayload,
    UserProfileOut,
)

router = APIRouter(prefix="/me", tags=["me"])


@router.get("", response_model=UserProfileOut)
def get_my_profile(current_user: User = Depends(get_current_user)):
    return current_user


@router.patch("/profile", response_model=UserProfileOut)
def update_my_profile(
    payload: ProfileUpdatePayload,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    current_user.full_name = payload.full_name
    db.commit()
    db.refresh(current_user)
    return current_user


@router.patch("/password", status_code=204)
def change_my_password(
    payload: PasswordChangePayload,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not verify_password(payload.current_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="Obecne haslo jest nieprawidlowe")
    if payload.current_password == payload.new_password:
        raise HTTPException(status_code=400, detail="Nowe haslo musi byc inne od obecnego")
    current_user.hashed_password = hash_password(payload.new_password)
    db.commit()


@router.patch("/notifications", response_model=UserProfileOut)
def update_my_notifications(
    payload: NotificationPreferencesPayload,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    current_user.notify_email_project_updates = payload.notify_email_project_updates
    current_user.notify_email_new_projects = payload.notify_email_new_projects
    current_user.notify_email_marketing = payload.notify_email_marketing
    db.commit()
    db.refresh(current_user)
    return current_user
