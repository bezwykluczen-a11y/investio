from celery import Celery

from app.core.config import get_settings

settings = get_settings()

celery_app = Celery("portal", broker=settings.redis_url, backend=settings.redis_url)
celery_app.conf.update(task_serializer="json", accept_content=["json"], result_serializer="json")


@celery_app.task
def scan_uploaded_document(document_id: str) -> str:
    """Placeholder: antywirus/skan pliku po uploadzie."""
    return f"scanned:{document_id}"
