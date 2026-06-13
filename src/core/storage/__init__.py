"""MinIO S3-compatible storage client (adapter pattern)."""
from io import BytesIO
from typing import Optional, BinaryIO
from minio import Minio

from src.config import MINIO_ENDPOINT, MINIO_ACCESS_KEY, MINIO_SECRET_KEY, MINIO_BUCKET


class StorageClient:
    def __init__(
        self,
        endpoint: str = MINIO_ENDPOINT,
        access_key: str = MINIO_ACCESS_KEY,
        secret_key: str = MINIO_SECRET_KEY,
        bucket: str = MINIO_BUCKET,
    ):
        self._client = Minio(
            endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=False,
        )
        self._bucket = bucket

    async def ensure_bucket(self):
        if not self._client.bucket_exists(self._bucket):
            self._client.make_bucket(self._bucket)

    def upload(self, object_name: str, data: bytes | BinaryIO, content_type: str = "application/octet-stream") -> str:
        if isinstance(data, bytes):
            data = BytesIO(data)
        self._client.put_object(
            self._bucket, object_name, data, length=-1,
            part_size=10 * 1024 * 1024, content_type=content_type,
        )
        return f"{self._bucket}/{object_name}"

    def get_url(self, object_name: str) -> str:
        return self._client.presigned_get_object(self._bucket, object_name)

    def delete(self, object_name: str):
        self._client.remove_object(self._bucket, object_name)


storage = StorageClient()
