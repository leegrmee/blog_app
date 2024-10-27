from typing import List, Optional
from config.Connection import prisma_connection
from resources.schemas.response import CommentResponse


class CommentRepository:
    def __init__(self):
        self.prisma = prisma_connection.prisma

    async def get_comments(
        self,
        id: Optional[int] = None,
        articleId: Optional[int] = None,
        userId: Optional[int] = None,
    ) -> List[CommentResponse]:
        filters = {}
        if id:
            filters["id"] = id
        if articleId:
            filters["articleId"] = articleId
        if userId:
            filters["userId"] = userId

        comments = await self.prisma.comment.find_many(
            where=filters, include={"user": True, "article": True}
        )
        return [CommentResponse.model_validate(comment) for comment in comments]

    async def create_comment(
        self, userId: int, articleId: int, content: str
    ) -> CommentResponse:
        new_comment = await self.prisma.comment.create(
            data={"userId": userId, "articleId": articleId, "content": content}
        )
        return CommentResponse.model_validate(new_comment)

    async def update_comment(
        self, userId: int, id: int, content: str
    ) -> CommentResponse:
        updated_comment = await self.prisma.comment.update(
            where={"id": id, "userId": userId}, data={"content": content}
        )
        return CommentResponse.model_validate(updated_comment)

    async def delete_comment(self, userId: int, id: int) -> None:
        await self.prisma.comment.delete(where={"id": id, "userId": userId})
