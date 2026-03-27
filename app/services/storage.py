import os
import shutil
import boto3
from typing import Optional, Protocol
from fastapi import UploadFile
from app.core.config import settings

class StorageService(Protocol):
    async def upload(self, file: UploadFile, filename: str) -> str:
        ...

    def delete(self, path: str):
        ...

    def get_url(self, path: str) -> str:
        ...

class LocalStorageService:
    def __init__(self, base_path: str):
        self.base_path = base_path
        if not os.path.exists(base_path):
            os.makedirs(base_path)

    async def upload(self, file: UploadFile, filename: str) -> str:
        file_path = os.path.join(self.base_path, filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return file_path

    def delete(self, path: str):
        if os.path.exists(path):
            os.remove(path)

    def get_url(self, path: str) -> str:
        # In a real app, this would return a URL served by the backend or Nginx
        return f"/media/{os.path.basename(path)}"

class S3StorageService:
    def __init__(self):
        self.s3 = boto3.client(
            "s3",
            endpoint_url=settings.S3_ENDPOINT,
            aws_access_key_id=settings.S3_ACCESS_KEY,
            aws_secret_access_key=settings.S3_SECRET_KEY,
        )
        self.bucket = settings.S3_BUCKET

    async def upload(self, file: UploadFile, filename: str) -> str:
        self.s3.upload_fileobj(file.file, self.bucket, filename)
        return filename

    def delete(self, path: str):
        self.s3.delete_object(Bucket=self.bucket, Key=path)

    def get_url(self, path: str) -> str:
        return f"{settings.S3_ENDPOINT}/{self.bucket}/{path}"

def get_storage_service() -> StorageService:
    if settings.STORAGE_TYPE == "s3":
        return S3StorageService()
    return LocalStorageService(settings.MEDIA_LOCAL_PATH)
