from typing import TypedDict
from config.Connection import prisma_connection
from dataclasses import dataclass


@dataclass
class CommentData(TypedDict):
    user_id: int
    article_id: int
    content: str


@dataclass
class CommentFilters(TypedDict, total=False):
    article_id: int | None
    user_id: int | None


class CommentRepository:
    def __init__(self):
        self.prisma = prisma_connection.prisma

    async def find_by_id(self, comment_id: int):
        return await self.prisma.comment.find_unique(
            where={"id": comment_id}, include={"user": True, "article": True}
        )

    async def find_by_filters(self, filters: CommentFilters):
        where_clause = {}
        if filters.get("article_id"):
            where_clause["articleId"] = filters["article_id"]
        if filters.get("user_id"):
            where_clause["userId"] = filters["user_id"]

        comments = await self.prisma.comment.find_many(
            where=where_clause, include={"user": True, "article": True}
        )
        return comments

    async def create(self, data: CommentData):
        return await self.prisma.comment.create(
            data={
                "userId": data["user_id"],
                "articleId": data["article_id"],
                "content": data["content"],
            }
        )

    async def update(self, data: CommentData):
        return await self.prisma.comment.update(
            where={"id": data["comment_id"], "userId": data["user_id"]},
            data={"content": data["content"]},
        )

    async def delete(self, user_id: int, comment_id: int):
        return await self.prisma.comment.delete(
            where={"id": comment_id, "userId": user_id}
        )
