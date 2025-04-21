from dataclasses import dataclass
from typing import List
from pydantic import ConfigDict

from src.core.database.base_repo import BaseRepository


@dataclass
class FileData:
    user_id: int
    path: str  # s3 key저장
    filename: str
    mimetype: str
    article_id: int
    size: int = 0

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class FileRepository(BaseRepository):
    def __init__(self):
        super().__init__("file")

    async def upload(self, file: FileData):
        """
        파일 정보를 데이터베이스에 저장합니다.
        """
        created_file = await super().create(
            data={
                "path": file.path,
                "filename": file.filename,
                "mimetype": file.mimetype,
                "article_id": file.article_id,
                "user_id": file.user_id,
                "size": file.size,
            }
        )
        return created_file.id

    async def get_file(self, id: int) -> FileData:
        """
        ID로 파일 정보를 조회합니다.
        """
        file = await super().find_unique(where={"id": id})
        if file:
            return FileData(
                user_id=file.user_id,
                path=file.path,
                filename=file.filename,
                mimetype=file.mimetype,
                article_id=file.article_id,
                size=file.size,
            )

        return None

    async def find_many(self, article_id: int) -> List[FileData]:
        """
        게시글에 속한 모든 파일을 조회합니다.
        """
        files = await super().find_many(where={"article_id": article_id})
        return [FileData.model_config(file) for file in files]

    async def delete(self, id: int):
        """
        파일 정보를 삭제합니다.
        """
        await super().delete(where={"id": id})
