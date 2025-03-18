import logging
from fastapi import UploadFile, File, HTTPException
from botocore.exceptions import BotoCoreError, NoCredentialsError

from resources.base_s3_service import BaseS3Service
from .file_repository import FileRepository
from .file_repository import FileData
from ..article.article_repository import ArticleRepository
from ..exceptions import NotFoundException, BadRequestException
from ..schemas.response import User, UserRole


class FileService(BaseS3Service):
    def __init__(self):
        super().__init__()
        self.file_repository = FileRepository()
        self.article_repository = ArticleRepository()

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
                # S3에 파일 업로드
                key = await self.upload_file(file, folder=f"articles/{article_id}")

                # 서명된 URL 생성
                signed_url = self.generate_signed_url(key)

                # 데이터베이스에 파일 정보 저장
                file_data = FileData(
                    user_id=user_id,
                    path=key,
                    filename=file.filename,
                    mimetype=file.content_type,
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
