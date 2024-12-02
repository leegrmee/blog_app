import os
import uuid
import boto3
from botocore.exceptions import BotoCoreError, NoCredentialsError
from fastapi import UploadFile, File, HTTPException
import logging

from config.settings import settings
from .file_repository import FileRepository
from .file_repository import FileData
from ..article.article_repository import ArticleRepository
from ..exceptions import NotFoundException, BadRequestException
from ..schemas.response import User, UserRole


class FileService:
    def __init__(self):
        self.file_repository = FileRepository()
        self.article_repository = ArticleRepository()
        self.s3_client = boto3.client(
            "s3",
            region_name=settings.AWS_S3_REGION,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )
        self.bucket_name = settings.AWS_S3_BUCKET_NAME
        self.url = (
            f"https://{self.bucket_name}.s3.{settings.AWS_S3_REGION}.amazonaws.com/"
        )

    async def upload(
        self,
        article_id: int,
        user_id: int,
        files: list[UploadFile] = File(None),
    ) -> list[str]:
        # upload file to database
        article = await self.article_repository.find_by_id(article_id)
        if not article:
            raise NotFoundException(name="Article")

        if article.user_id != user_id:
            raise HTTPException(
                status_code=403, detail="You are not the author of this article"
            )

        if not files:
            raise BadRequestException(detail="No files provided")

        file_urls = []
        for file in files:
            _, file_extension = os.path.splitext(file.filename)
            unique_filename = f"{uuid.uuid4()}{file_extension}"

            try:
                self.s3_client.upload_fileobj(
                    file.file,
                    self.bucket_name,
                    unique_filename,
                    ExtraArgs={
                        "ContentType": file.content_type,
                    },
                )
                file_url = f"{self.url}{unique_filename}"

                file_data = FileData(
                    user_id=user_id,
                    path=unique_filename,
                    filename=file.filename,
                    mimetype=file.content_type,
                    article_id=article_id,
                )
                file_id = await self.file_repository.upload(file_data)
                logging.info("Uploaded file with id:%s", file_id)
                file_urls.append(file_url)

                # # 파일 저장 (비동기로 처리)
                # async with aiofiles_open(file_path, "wb") as buffer:
                #     content = await file.read()
                #     await buffer.write(content)

            except (BotoCoreError, NoCredentialsError) as e:
                logging.error(f"Error uploading file {file.filename}: {e}")
                continue  # 에러 발생 시 해당 파일 건너뛰기

        return file_urls

    async def get_path(self, id: int) -> str:
        file = await self.file_repository.get_file(id)

        if file:
            return f"{self.url}{file.path}"

        raise NotFoundException(name="File")

    async def delete(self, id: int, current_user: User):
        file = await self.file_repository.get_file(id)

        if not file:
            raise NotFoundException(name="File")

        if file.user_id != current_user.id and current_user.role not in [
            UserRole.MODERATOR,
            UserRole.ADMIN,
        ]:
            raise HTTPException(
                status_code=403, detail="Insufficient permissions to delete the article"
            )

        try:
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=file.path)
            await self.file_repository.delete(id)

        except (BotoCoreError, NoCredentialsError) as e:
            logging.error(f"Error deleting file {id} from S3: {e}")
            raise HTTPException(
                status_code=500, detail="Failed to delete the file from S3"
            )

    async def get_file_info(self, id: int):
        file = await self.file_repository.get_file(id)
        if not file:
            raise NotFoundException(name="File")
        # file_stat = os.stat(file.path)
        return {**file.__dict__}
