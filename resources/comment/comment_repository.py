from dataclasses import dataclass
from typing import TypedDict
from config.Connection import prisma_connection


@dataclass
class CommentData(TypedDict):
    user_id: int
    article_id: int
    content: str


@dataclass
class CommentFilters(TypedDict, total=False):
    article_id: int | None = None
    user_id: int | None = None


@dataclass
class UpdateCommentData(TypedDict):
    user_id: int
    id: int
    new_content: str


class CommentRepository:
    def __init__(self):
        self.prisma = prisma_connection.prisma

    async def find_many(self, skip: int = 0, limit: int = 10):
        return await self.prisma.comment.find_many(skip=skip, take=limit)

    async def find_by_id(self, comment_id: int):
        return await self.prisma.comment.find_unique(where={"id": comment_id})

    async def find_by_filters(self, filters: CommentFilters):
        where_clause = {}
        if filters.get("article_id"):
            where_clause["article_id"] = filters["article_id"]
        if filters.get("user_id"):
            where_clause["user_id"] = filters["user_id"]

        return await self.prisma.comment.find_many(where=where_clause)

    async def create(self, data: CommentData):
        return await self.prisma.comment.create(
            data={
                "user_id": data["user_id"],
                "article_id": data["article_id"],
                "content": data["content"],
            }
        )

    async def update(self, data: UpdateCommentData):
        return await self.prisma.comment.update(
            where={"id": data["id"]},
            data={"content": data["new_content"]},
        )

    async def delete(self, comment_id: int):
        return await self.prisma.comment.delete(where={"id": comment_id})
