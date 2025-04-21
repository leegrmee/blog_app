import logging
from fastapi import UploadFile, File, HTTPException
from botocore.exceptions import BotoCoreError, NoCredentialsError
from typing import List

from src.services.s3.base_s3_service import BaseS3Service
from src.api.v1.files.file_repository import FileRepository, FileData
from src.api.v1.articles.article_repository import ArticleRepository
from src.core.exceptions.base import NotFoundException, BadRequestException
from src.schemas.response import User, UserRole, FileType, FileResponse


class FileService(BaseS3Service):
    def __init__(self):
        super().__init__()
        self.file_repository = FileRepository()
        self.article_repository = ArticleRepository()
        self.max_file_size = 10 * 1024 * 1024  # 10MB
        self.allowed_file_types = {
            "image": ["image/jpeg", "image/png", "image/gif", "image/jpg"],
            "document": ["application/pdf", "application/msword"],
        }

    def _get_file_type(self, mimetype: str) -> FileType:
        for file_type, mime_types in self.allowed_file_types.items():
            if mimetype in mime_types:
                return file_type
        return FileType.OTHER

    def _validate_file(self, file: UploadFile) -> bool:
        if file.size > self.max_file_size:
            raise BadRequestException(detail="File size exceeds the maximum limit")

        # Check if the content type is in any of the allowed mime types
        is_allowed = any(
            file.content_type in mime_types
            for mime_types in self.allowed_file_types.values()
        )
        if not is_allowed:
            raise BadRequestException(detail="Invalid file type")
        return True

    async def upload(
        self,
        article_id: int,
        user_id: int,
        files: list[UploadFile] = File(None),
    ) -> list[str]:
        """
        파일을 S3에 업로드하고 데이터베이스에 정보를 저장합니다.
        """
        # 게시글 확인
        article = await self.article_repository.find_by_id(article_id)
        if not article:
            raise NotFoundException(name="Article")

        # 권한 확인
        if article.user_id != user_id:
            raise HTTPException(
                status_code=403, detail="You are not the author of this article"
            )

        if not files:
            raise BadRequestException(detail="No files provided")

        signed_urls = []
        for file in files:
            try:
                # validation
                self._validate_file(file)

                # S3에 파일 업로드
                key = await self.upload_file(file, folder=f"articles/{article_id}")

                # 서명된 URL 생성
                signed_url = self.generate_signed_url(key)

                # 파일 타입 결정
                file_type = self._get_file_type(file.content_type)

                # 데이터베이스에 파일 정보 저장
                file_data = FileData(
                    user_id=user_id,
                    path=key,
                    filename=file.filename,
                    mimetype=file_type,
                    article_id=article_id,
                    size=file.size,
                )
                await self.file_repository.upload(file_data)
                logging.info("Uploaded file with key: %s", key)
                signed_urls.append(signed_url)

            except (BotoCoreError, NoCredentialsError) as e:
                logging.error(f"Error uploading file {file.filename}: {e}")
                continue  # 에러 발생 시 해당 파일 건너뛰기

        return signed_urls

    async def get_article_files(self, article_id: int) -> List[FileResponse]:
        """
        게시글에 속한 모든 파일을 반환합니다.
        """
        files = await self.file_repository.find_many(article_id)
        result = []
        for file in files:
            file_type = self._get_file_type(file.mimetype)
            file_url = self.generate_signed_url(file.path)
            result.append(
                FileResponse(
                    id=file.id,
                    filename=file.filename,
                    mimetype=file.mimetype,
                    size=file.size,
                    type=file_type,
                    url=file_url,
                    upload_time=file.created_at,
                )
            )
        return result

    async def get_url(self, id: int) -> str:
        """
        파일의 서명된 URL을 반환합니다.
        """
        file = await self.file_repository.get_file(id)

        if file:
            signed_url = self.generate_signed_url(file.path)
            return signed_url

        raise NotFoundException(name="File")

    async def delete(self, id: int, current_user: User):
        """
        파일을 S3와 데이터베이스에서 삭제합니다.
        """
        file = await self.file_repository.get_file(id)

        if not file:
            raise NotFoundException(name="File")

        # 권한 확인
        if file.user_id != current_user.id and current_user.role not in [
            UserRole.MODERATOR,
            UserRole.ADMIN,
        ]:
            raise HTTPException(
                status_code=403, detail="Insufficient permissions to delete file"
            )

        try:
            # S3에서 파일 삭제
            self.delete_file(file.path)
            # 데이터베이스에서 파일 정보 삭제
            await self.file_repository.delete(id)

        except Exception as e:
            logging.error(f"Error deleting file {id} from S3: {e}")
            raise HTTPException(
                status_code=500, detail="Failed to delete the file from S3"
            )
