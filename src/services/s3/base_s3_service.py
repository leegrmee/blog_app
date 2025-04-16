import os
import uuid
import boto3
from botocore.exceptions import BotoCoreError, NoCredentialsError
from botocore.config import Config
from fastapi import UploadFile, HTTPException
import logging
from typing import List

from src.core.config.settings import settings


class BaseS3Service:
    """
    S3 파일 저장소 작업을 위한 기본 클래스입니다.
    """

    def __init__(self):
        config = Config(signature_version="s3v4")
        self.s3_client = boto3.client(
            "s3",
            region_name=settings.AWS_S3_REGION,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            config=config,
        )
        self.bucket_name = settings.AWS_S3_BUCKET_NAME
        self.base_url = (
            f"https://{self.bucket_name}.s3.{settings.AWS_S3_REGION}.amazonaws.com/"
        )

    def generate_unique_filename(self, original_filename: str) -> str:
        """
        고유한 파일 이름을 생성합니다.
        """
        ext = os.path.splitext(original_filename)[1] if original_filename else ""
        return f"{uuid.uuid4()}{ext}"

    async def upload_file(self, file: UploadFile, folder: str = "") -> str:
        """
        파일을 S3에 업로드합니다.
        """
        try:
            unique_filename = self.generate_unique_filename(file.filename)
            key = f"{folder}/{unique_filename}" if folder else unique_filename

            # 파일 내용 읽기
            contents = await file.read()

            # S3에 업로드
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=key,
                Body=contents,
                ContentType=file.content_type,
            )

            # 파일 포인터 위치 초기화
            await file.seek(0)

            return key
        except (BotoCoreError, NoCredentialsError) as e:
            logging.error(f"S3 upload error: {str(e)}")
            raise HTTPException(status_code=500, detail=f"S3 upload failed: {str(e)}")

    async def upload_files(
        self, files: List[UploadFile], folder: str = ""
    ) -> List[str]:
        """
        여러 파일을 S3에 업로드합니다.
        """
        if not files:
            return []

        uploaded_keys = []
        for file in files:
            key = await self.upload_file(file, folder)
            uploaded_keys.append(key)

        return uploaded_keys

    def generate_signed_url(self, key: str, expires_in: int = 3600) -> str:
        """
        S3 객체에 대한 signed URL을 생성합니다.
        """
        try:
            signed_url = self.s3_client.generate_presigned_url(
                "get_object",
                Params={
                    "Bucket": self.bucket_name,
                    "Key": key,
                },
                ExpiresIn=expires_in,
                HttpMethod="GET",
            )
            return signed_url
        except Exception as e:
            logging.error(f"Error generating signed URL for key {key}: {e}")
            raise HTTPException(status_code=500, detail="Failed to generate signed URL")

    def delete_file(self, key: str) -> bool:
        """
        S3에서 파일을 삭제합니다.
        """
        try:
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=key)
            return True
        except Exception as e:
            logging.error(f"Error deleting file with key {key}: {e}")
            raise HTTPException(
                status_code=500, detail=f"Failed to delete file: {str(e)}"
            )

    def get_file_url(self, key: str) -> str:
        """
        S3 파일의 URL을 반환합니다.
        """
        return f"{self.base_url}{key}"
