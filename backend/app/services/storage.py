import hashlib
import uuid
from urllib.parse import urlsplit, urlunsplit

import boto3
from botocore.exceptions import ClientError

from app.core.config import get_settings

ALLOWED_IMAGE_TYPES = {
    "image/jpeg": "jpg",
    "image/png": "png",
    "image/webp": "webp",
}


def get_s3_client():
    settings = get_settings()
    return boto3.client(
        "s3",
        endpoint_url=settings.storage_endpoint_url,
        aws_access_key_id=settings.storage_access_key,
        aws_secret_access_key=settings.storage_secret_key,
    )


def ensure_bucket_exists(bucket: str) -> None:
    client = get_s3_client()
    try:
        client.head_bucket(Bucket=bucket)
    except ClientError:
        client.create_bucket(Bucket=bucket)


def build_storage_key(project_id: uuid.UUID, extension: str) -> str:
    return f"projects/{project_id}/images/{uuid.uuid4().hex}.{extension}"


def upload_bytes(bucket: str, key: str, data: bytes, content_type: str) -> None:
    client = get_s3_client()
    client.put_object(Bucket=bucket, Key=key, Body=data, ContentType=content_type)


def delete_object(bucket: str, key: str) -> None:
    client = get_s3_client()
    client.delete_object(Bucket=bucket, Key=key)


def presigned_get_url(bucket: str, key: str, expires_in: int = 3600) -> str:
    client = get_s3_client()
    internal_url = client.generate_presigned_url(
        "get_object",
        Params={"Bucket": bucket, "Key": key},
        ExpiresIn=expires_in,
    )
    settings = get_settings()
    public_base = getattr(settings, "storage_public_base_url", None)
    if not public_base:
        return internal_url

    parts = urlsplit(internal_url)
    public_parts = urlsplit(public_base.rstrip("/") + "/")
    new_path = public_parts.path.rstrip("/") + parts.path
    return urlunsplit((public_parts.scheme, public_parts.netloc, new_path, parts.query, ""))


def sha256_of(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()
