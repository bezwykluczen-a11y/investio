import enum


class UserRole(str, enum.Enum):
    USER = "user"
    ORGANIZER = "organizer"
    ANALYST = "analyst"
    MODERATOR = "moderator"
    ADMIN = "admin"


class ProjectStatus(str, enum.Enum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    IN_REVIEW = "in_review"
    NEEDS_CHANGES = "needs_changes"
    VERIFIED = "verified"
    PUBLISHED = "published"
    PAUSED = "paused"
    COMPLETED = "completed"
    REJECTED = "rejected"


class ProjectCategory(str, enum.Enum):
    HOUSING = "housing"
    ENERGY_BIOGAS = "energy_biogas"
    LOCAL_INFRASTRUCTURE = "local_infrastructure"
    SPORTS_RECREATION = "sports_recreation"
    INDUSTRIAL = "industrial"
    MUNICIPAL = "municipal"
    OTHER = "other"


class DocumentStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class QuestionStatus(str, enum.Enum):
    OPEN = "open"
    ANSWERED = "answered"
    HIDDEN = "hidden"
