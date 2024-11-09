import os
import uuid
from fastapi import UploadFile, File, HTTPException
from aiofiles import open as aiofiles_open

from .file_repository import FileRepository
from .file_repository import FileData
from ..article.article_repository import ArticleRepository
from ..exceptions import ResourceNotFoundException
from ..schemas.response import User, UserRole

UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)


class FileService:
    def __init__(self):
        self.file_repository = FileRepository()
        self.article_repository = ArticleRepository()

    async def upload(
        self,
        article_id: int,
        user_id: int,
        files: list[UploadFile] = File(None),
    ) -> list[str]:
        # upload file to database

        article = await self.article_repository.find_by_id(article_id)
        if not article:
            raise ResourceNotFoundException(detail="Article not found")

        if article.user_id != user_id:
            raise HTTPException(
                status_code=403, detail="You are not the author of this article"
            )

        if not files:
            raise ResourceNotFoundException(detail="No files provided")

        file_urls = []
        for file in files:
            _, file_extension = os.path.splitext(file.filename)
            unique_filename = f"{uuid.uuid4()}{file_extension}"
            file_path = os.path.join(UPLOAD_DIR, unique_filename)

            try:
                # 파일 저장 (비동기로 처리)
                async with aiofiles_open(file_path, "wb") as buffer:
                    content = await file.read()
                    await buffer.write(content)

            except Exception as e:
                print(e)
                continue  # 에러 발생 시 해당 파일 건너뛰기

            file_data = FileData(
                user_id=user_id,
                path=file_path,
                filename=unique_filename,
                mimetype=file.content_type,
                article_id=article_id,
            )
            file_id = await self.file_repository.upload(file_data)
            file_url = f"/files/{file_id}"
            file_urls.append(file_url)

        return file_urls

    async def get_path(self, id: int) -> str:
        file = await self.file_repository.get_file(id)

        if file:
            return file.path

        raise ResourceNotFoundException(detail="File not found")

    async def delete(self, id: int, current_user: User):
        file = await self.file_repository.get_file(id)

        if not file:
            raise ResourceNotFoundException(detail="File not found")

        if file.user_id != current_user.id and current_user.role not in [
            UserRole.MODERATOR,
            UserRole.ADMIN,
        ]:
            raise HTTPException(
                status_code=403, detail="Insufficient permissions to delete the article"
            )

        await self.file_repository.delete(id)

    async def get_file_info(self, id: int):
        file = await self.file_repository.get_file(id)
        if not file:
            raise ResourceNotFoundException(detail="File not found")
        # file_stat = os.stat(file.path)
        return {**file.__dict__}
