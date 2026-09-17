import uuid
from slugify import slugify
from sqlalchemy import select
from sqlalchemy.orm import Session


def unique_slug(db: Session, model, base_text: str, slug_field: str = "slug") -> str:
    base_slug = slugify(base_text)[:200] or str(uuid.uuid4())[:8]
    candidate = base_slug
    counter = 1
    field = getattr(model, slug_field)
    while db.scalar(select(model).where(field == candidate)) is not None:
        counter += 1
        candidate = f"{base_slug}-{counter}"
    return candidate
