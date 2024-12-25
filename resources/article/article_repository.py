from datetime import date, datetime, timedelta, timezone
from config.Connection import prisma_connection
from dataclasses import dataclass
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
    """While SearchParams is similar to ArticleSearch, transforming the Pydantic model into a dataclass (or any other internal representation) can be useful for:
    Decoupling Layers: Keeping the repository layer independent from Pydantic (and FastAPI) specifics.
    Data Transformation: Preparing data in a format that's optimal for the repository's operations.
    """

    category_id: int | None = None
    user_id: int | None = None
    created_date: date | None = None
    updated_date: date | None = None
    skip: int = 0
    limit: int = 10


class ArticleRepository:
    def __init__(self):
        self._prisma = prisma_connection.prisma

    async def find_many(self, skip: int, limit: int):
        return await self._prisma.article.find_many(
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
        article = await self._prisma.article.find_unique(
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
        return await self._prisma.article.update(
            where={"id": article_id},
            data={"views": {"increment": 1}},
            include={
                "user": True,
                "categories": {"include": {"category": True}},
                "likes": True,
            },
        )

    async def increment_likes_count(self, article_id: int):
        return await self._prisma.article.update(
            where={"id": article_id},
            data={"likes_count": {"increment": 1}},
        )

    async def decrement_likes_count(self, article_id: int):
        return await self._prisma.article.update(
            where={"id": article_id},
            data={"likes_count": {"decrement": 1}},
        )

    async def set_likes_count(self, article_id: int, count: int):
        await self._prisma.article.update(
            where={"id": article_id}, data={"likes_count": count}
        )

    async def search(self, params: SearchParams):
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

        return await self._prisma.article.find_many(
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
        async with self._prisma.tx() as transaction:
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
        article = await self._prisma.article.find_unique(where={"id": article_id})
        if not article:
            raise NotFoundException(name=f"Article with id {article_id}")
        await self._prisma.article.delete(where={"id": article_id})
        return True

    async def update(self, params: UpdateParams):
        article = await self._prisma.article.find_unique(
            where={"id": params.article_id}
        )
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

        updated_article = await self._prisma.article.update(
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
