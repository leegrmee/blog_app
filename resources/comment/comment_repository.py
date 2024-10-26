from typing import List, Optional
from config.Connection import prisma_connection
from resources.schemas.response import CommentResponse


class CommentRepository:
    def __init__(self):
        self.prisma = prisma_connection.prisma

    async def get_comments(
        self,
        comment_id: Optional[int] = None,
        article_id: Optional[int] = None,
        user_id: Optional[int] = None,
    ) -> List[CommentResponse]:

        filters = {}
        if comment_id:
            filters["id"] = comment_id
        if article_id:
            filters["article_id"] = article_id
        if user_id:
            filters["user_id"] = user_id

        comments = await self.prisma.comment.find_many(
            where=filters, include={"user": True, "article": True}
        )
        return [CommentResponse.model_validate(comment) for comment in comments]

    async def create_comment(
        self, user_id: int, article_id: int, content: str
    ) -> CommentResponse:
        new_comment = await self.prisma.comment.create(
            data={"user_id": user_id, "article_id": article_id, "content": content}
        )
        return CommentResponse.model_validate(new_comment)

    async def update_comment(
        self, user_id: int, comment_id: int, content: str
    ) -> CommentResponse:
        updated_comment = await self.prisma.comment.update(
            where={"id": comment_id, "user_id": user_id}, data={"content": content}
        )
        return CommentResponse.model_validate(updated_comment)

    async def delete_comment(self, user_id: int, comment_id: int) -> None:
        await self.prisma.comment.delete(where={"id": comment_id, "user_id": user_id})
