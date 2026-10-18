from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from urllib.parse import quote

import boto3
from botocore.client import Config

from app.config import Settings


class ObjectStorage(ABC):
    @abstractmethod
    def put_bytes(self, key: str, data: bytes, content_type: str) -> None: ...

    @abstractmethod
    def get_bytes(self, key: str) -> bytes: ...

    @abstractmethod
    def delete(self, key: str) -> None: ...

    @abstractmethod
    def presigned_get_url(self, key: str, *, expires_in: int, filename: str, content_type: str) -> str: ...


class LocalObjectStorage(ObjectStorage):
    """Private local storage for development. Not a public web root."""

    def __init__(self, root: str):
        self.root = Path(root).resolve()
        self.root.mkdir(parents=True, exist_ok=True)

    def _path(self, key: str) -> Path:
        # Opaque keys only; reject path traversal.
        if ".." in key or key.startswith(("/", "\\")):
            raise ValueError("Invalid storage key")
        path = (self.root / key).resolve()
        if not str(path).startswith(str(self.root)):
            raise ValueError("Invalid storage key")
        return path

    def put_bytes(self, key: str, data: bytes, content_type: str) -> None:
        path = self._path(key)
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix(path.suffix + ".tmp")
        tmp.write_bytes(data)
        tmp.replace(path)
        meta = path.with_suffix(path.suffix + ".meta")
        meta.write_text(content_type, encoding="utf-8")

    def get_bytes(self, key: str) -> bytes:
        return self._path(key).read_bytes()

    def delete(self, key: str) -> None:
        path = self._path(key)
        if path.exists():
            path.unlink()
        meta = path.with_suffix(path.suffix + ".meta")
        if meta.exists():
            meta.unlink()

    def presigned_get_url(self, key: str, *, expires_in: int, filename: str, content_type: str) -> str:
        # Local backend returns an API-relative tokenized download path placeholder;
        # callers should stream via authenticated API when using local storage.
        return f"local://{quote(key)}?ttl={expires_in}&filename={quote(filename)}"


class S3ObjectStorage(ObjectStorage):
    def __init__(self, settings: Settings):
        kwargs = {
            "service_name": "s3",
            "region_name": settings.s3_region or None,
            "config": Config(signature_version="s3v4"),
        }
        if settings.s3_endpoint_url:
            kwargs["endpoint_url"] = settings.s3_endpoint_url
        self.client = boto3.client(**kwargs)
        self.bucket = settings.s3_bucket
        self.kms_key_id = settings.s3_kms_key_id

    def put_bytes(self, key: str, data: bytes, content_type: str) -> None:
        extra = {"ContentType": content_type, "ACL": "private"}
        if self.kms_key_id:
            extra["ServerSideEncryption"] = "aws:kms"
            extra["SSEKMSKeyId"] = self.kms_key_id
        else:
            extra["ServerSideEncryption"] = "AES256"
        self.client.put_object(Bucket=self.bucket, Key=key, Body=data, **extra)

    def get_bytes(self, key: str) -> bytes:
        obj = self.client.get_object(Bucket=self.bucket, Key=key)
        return obj["Body"].read()

    def delete(self, key: str) -> None:
        self.client.delete_object(Bucket=self.bucket, Key=key)

    def presigned_get_url(self, key: str, *, expires_in: int, filename: str, content_type: str) -> str:
        return self.client.generate_presigned_url(
            "get_object",
            Params={
                "Bucket": self.bucket,
                "Key": key,
                "ResponseContentDisposition": f'attachment; filename="{filename}"',
                "ResponseContentType": content_type,
            },
            ExpiresIn=expires_in,
        )


def build_storage(settings: Settings) -> ObjectStorage:
    if settings.storage_backend == "s3":
        if not settings.s3_bucket:
            raise RuntimeError("S3_BUCKET is required when STORAGE_BACKEND=s3")
        return S3ObjectStorage(settings)
    return LocalObjectStorage(settings.local_storage_path)
