import uuid
from pydantic import BaseModel, EmailStr, Field

from app.models.enums import UserRole


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    full_name: str = Field(min_length=2, max_length=255)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: uuid.UUID
    email: EmailStr
    full_name: str
    role: UserRole
    is_active: bool

    class Config:
        from_attributes = True


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserProfileOut(BaseModel):
    id: uuid.UUID
    email: EmailStr
    full_name: str
    role: UserRole
    is_active: bool
    notify_email_project_updates: bool
    notify_email_new_projects: bool
    notify_email_marketing: bool

    class Config:
        from_attributes = True


class ProfileUpdatePayload(BaseModel):
    full_name: str = Field(min_length=2, max_length=255)


class PasswordChangePayload(BaseModel):
    current_password: str
    new_password: str = Field(min_length=8, max_length=128)


class NotificationPreferencesPayload(BaseModel):
    notify_email_project_updates: bool
    notify_email_new_projects: bool
    notify_email_marketing: bool
