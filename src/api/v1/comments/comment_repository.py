from dataclasses import dataclass
from typing import TypedDict

from src.core.database.base_repo import BaseRepository


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


class CommentRepository(BaseRepository):
    def __init__(self):
        super().__init__("comment")

    async def find_many(self, skip: int = 0, limit: int = 10):
        """
        여러 댓글을 조회합니다.
        """
        return await super().find_many(skip=skip, take=limit)

    async def find_by_id(self, comment_id: int):
        """
        ID로 댓글을 조회합니다.
        """
        return await super().find_unique(where={"id": comment_id})

    async def find_by_filters(self, filters: CommentFilters):
        """
        필터 조건에 맞는 댓글을 조회합니다.
        """
        where_clause = {}
        if filters.get("article_id"):
            where_clause["article_id"] = filters["article_id"]
        if filters.get("user_id"):
            where_clause["user_id"] = filters["user_id"]

        return await super().find_many(where=where_clause)

    async def create(self, data: CommentData):
        """
        새 댓글을 생성합니다.
        """
        return await super().create(
            data={
                "user_id": data["user_id"],
                "article_id": data["article_id"],
                "content": data["content"],
            }
        )

    async def update(self, data: UpdateCommentData):
        """
        댓글을 업데이트합니다.
        """
        return await super().update(
            where={"id": data["id"]},
            data={"content": data["new_content"]},
        )

    async def delete(self, comment_id: int):
        """
        댓글을 삭제합니다.
        """
        return await super().delete(where={"id": comment_id})
