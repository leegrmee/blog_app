from dataclasses import dataclass
from config.Connection import prisma_connection
from datetime import datetime
from dataclasses import field


@dataclass
class FileData:
    user_id: int
    path: str  # s3 key저장
    filename: str
    mimetype: str
    article_id: int
    upload_time: datetime = field(default_factory=datetime.datetime)


class FileRepository:
    def __init__(self):
        self.prisma = prisma_connection.prisma

    async def upload(self, file: FileData):
        # upload file to database/ file path = s3 key
        created_file = await self.prisma.file.create(
            data={
                "path": file.path,
                "filename": file.filename,
                "mimetype": file.mimetype,
                "article_id": file.article_id,
                "user_id": file.user_id,
                "upload_time": file.upload_time,
                "file_size": file.file_size,
            }
        )
        return created_file.id

    async def get_file(self, id: int) -> FileData:
        file = await self.prisma.file.find_unique(where={"id": id})
        if file:
            return FileData(
                user_id=file.user_id,
                path=file.path,
                filename=file.filename,
                mimetype=file.mimetype,
                article_id=file.article_id,
            )

        return None

    async def delete(self, id: int):
        await self.prisma.file.delete(where={"id": id})
