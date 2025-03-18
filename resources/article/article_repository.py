from datetime import date, datetime, timedelta, timezone
from dataclasses import dataclass
from typing import List, Dict, Any, Optional

from resources.base_repository import BaseRepository
from resources.exceptions import NotFoundException


@dataclass
class UpdateParams:
    user_id: int
    article_id: int
    title: str | None = None
    content: str | None = None
    categories: list[int] | None = None


@dataclass
class SearchParams:
    """
    검색 파라미터 클래스입니다.
    Pydantic 모델과 유사하지만 레이어 분리를 위해 내부 표현으로 사용합니다.
    """

    category_id: int | None = None
    user_id: int | None = None
    created_date: date | None = None
    updated_date: date | None = None
    skip: int = 0
    limit: int = 10


class ArticleRepository(BaseRepository):
    def __init__(self):
        super().__init__("article")

    async def find_many(self, skip: int, limit: int):
        """
        여러 게시글을 조회합니다.
        """
        return await super().find_many(
            skip=skip,
            take=limit,
            order={"created_at": "desc"},
            include={
                "user": True,
                "categories": {"include": {"category": True}},
                "likes": True,
                "files": True,
            },
        )

    async def find_by_id(self, article_id: int):
        """
        ID로 게시글을 조회합니다.
        """
        article = await super().find_unique(
            where={"id": article_id},
            include={
                "user": True,
                "categories": {"include": {"category": True}},
                "likes": True,
                "files": True,
            },
        )

        if not article:
            raise NotFoundException(name=f"Article with id {article_id}")
        return article

    async def increment_view_count(self, article_id: int):
        """
        게시글 조회수를 증가시킵니다.
        """
        return await super().update(
            where={"id": article_id},
            data={"views": {"increment": 1}},
            include={
                "user": True,
                "categories": {"include": {"category": True}},
                "likes": True,
            },
        )

    async def increment_likes_count(self, article_id: int):
        """
        게시글 좋아요 수를 증가시킵니다.
        """
        return await super().update(
            where={"id": article_id},
            data={"likes_count": {"increment": 1}},
        )

    async def decrement_likes_count(self, article_id: int):
        """
        게시글 좋아요 수를 감소시킵니다.
        """
        return await super().update(
            where={"id": article_id},
            data={"likes_count": {"decrement": 1}},
        )

    async def set_likes_count(self, article_id: int, count: int):
        """
        게시글 좋아요 수를 설정합니다.
        """
        await super().update(where={"id": article_id}, data={"likes_count": count})

    async def search(self, params: SearchParams):
        """
        검색 조건에 맞는 게시글을 조회합니다.
        """
        filters = {}
        if params.category_id is not None:
            filters["categories"] = {"some": {"category_id": params.category_id}}
        if params.user_id is not None:
            filters["user_id"] = params.user_id

        if params.created_date is not None:
            start_datetime = datetime.combine(
                params.created_date, datetime.min.time()
            ).replace(tzinfo=timezone.utc)
            end_datetime = start_datetime + timedelta(days=1)
            filters["created_at"] = {
                "gte": start_datetime,
                "lt": end_datetime,
            }

        if params.updated_date is not None:
            start_datetime = datetime.combine(
                params.updated_date, datetime.min.time()
            ).replace(tzinfo=timezone.utc)
            end_datetime = start_datetime + timedelta(days=1)
            filters["updated_at"] = {
                "gte": start_datetime,
                "lt": end_datetime,
            }

        return await super().find_many(
            where=filters,
            skip=params.skip,
            take=params.limit,
            order={"created_at": "desc"},
            include={
                "user": True,
                "categories": {"include": {"category": True}},
                "likes": True,
                "files": True,
            },
        )

    async def create(
        self, user_id: int, title: str, content: str, category_ids: list[int]
    ):
        """
        새 게시글을 생성합니다.
        """
        async with self.prisma.tx() as transaction:
            article = await transaction.article.create(
                data={
                    "user_id": user_id,
                    "title": title,
                    "content": content,
                    "categories": {
                        "create": [
                            {"category": {"connect": {"id": cat_id}}}
                            for cat_id in category_ids
                        ],
                    },
                },
                include={
                    "user": True,
                    "categories": {"include": {"category": True}},
                    "likes": True,
                },
            )
        return article

    async def delete(self, article_id: int):
        """
        게시글을 삭제합니다.
        """
        article = await super().find_unique(where={"id": article_id})
        if not article:
            raise NotFoundException(name=f"Article with id {article_id}")
        await super().delete(where={"id": article_id})
        return True

    async def update(self, params: UpdateParams):
        """
        게시글을 업데이트합니다.
        """
        article = await super().find_unique(where={"id": params.article_id})
        if not article:
            raise NotFoundException(name=f"Article with id {params.article_id}")

        update_data = {}
        if params.title is not None:
            update_data["title"] = params.title
        if params.content is not None:
            update_data["content"] = params.content
        # 카테고리 업뎃은 전부 다 다시 설정해야함
        if params.categories is not None:
            update_data["categories"] = {
                "deleteMany": {},
                "create": [
                    {"category": {"connect": {"id": cat_id}}}
                    for cat_id in params.categories
                ],
            }

        updated_article = await super().update(
            where={"id": article.id},
            data=update_data,
            include={
                "user": True,
                "categories": {"include": {"category": True}},
                "likes": True,
                "files": True,
            },
        )
        return updated_article
