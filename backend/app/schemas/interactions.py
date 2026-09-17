import uuid
from pydantic import BaseModel, Field


class InterestDeclarationCreate(BaseModel):
    amount_range: str = Field(max_length=50)
    contact_preference: str = Field(max_length=50)
    comment: str | None = None
    consent_marketing: bool = False
    consent_risk_disclaimer_accepted: bool

    class Config:
        json_schema_extra = {
            "description": (
                "Deklaracja zainteresowania nie jest zobowiazaniem finansowym "
                "ani inwestycja. consent_risk_disclaimer_accepted musi byc True."
            )
        }


class InterestDeclarationOut(BaseModel):
    id: uuid.UUID
    project_id: uuid.UUID
    amount_range: str
    contact_preference: str

    class Config:
        from_attributes = True


class ProjectQuestionCreate(BaseModel):
    question: str = Field(min_length=5, max_length=2000)


class ProjectQuestionAnswer(BaseModel):
    answer: str = Field(min_length=1, max_length=4000)


class ProjectQuestionOut(BaseModel):
    id: uuid.UUID
    project_id: uuid.UUID
    question: str
    answer: str | None
    status: str

    class Config:
        from_attributes = True
