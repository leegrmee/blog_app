from datetime import datetime
from config.Connection import prisma_connection
from dataclasses import dataclass


@dataclass
class UpdateParams:
    user_id: int
    article_id: int
    title: str | None
    content: str | None
    categories: list[int] | None


@dataclass
class SearchParams:
    category_id: int | None
    user_id: int
    created_date: datetime | None
    updated_date: datetime | None
    skip: int = 0
    limit: int = 10


class ArticleRepository:
    def __init__(self):
        self.prisma = prisma_connection.prisma

    async def find_many(self, user_id: int, skip: int, limit: int):
        return await self.prisma.article.find_many(
            where={"user_id": user_id},
            skip=skip,
            take=limit,
            order={"created_at": "desc"},
            include={"user": True, "categories": {"include": {"category": True}}},
        )

    async def find_by_id(self, article_id: int):
        return await self.prisma.article.find_unique(
            where={"id": article_id},
            include={"user": True, "categories": {"include": {"category": True}}},
        )

    async def increment_view_count(self, article_id: int):
        return await self.prisma.article.update(
            where={"id": article_id},
            data={"views": {"increment": 1}},
            include={"user": True},
        )

    async def search(self, params: SearchParams):
        filters = {}
        if params.category_id is not None:
            filters["categories"] = {"some": {"category_id": params.category_id}}
        if params.user_id is not None:
            filters["user_id"] = params.user_id
        if params.created_date is not None:
            filters["created_at"] = params.created_date
        if params.updated_date is not None:
            filters["updated_at"] = params.updated_date

        return await self.prisma.article.find_many(
            where=filters,
            skip=params.skip,
            take=params.limit,
            include={"user": True, "categories": True},
        )

    async def create(
        self, user_id: int, title: str, content: str, category_ids: list[int]
    ):
        return await self.prisma.article.create(
            data={
                "user_id": user_id,
                "title": title,
                "content": content,
                "categories": {
                    "create": [
                        {"category": {"connect": {"id": cat_id}}}
                        for cat_id in category_ids
                    ]
                },
            },
            include={"user": True, "categories": {"include": {"category": True}}},
        )

    async def add_categories(self, article_id: int, category_ids: list[int]):
        return await self.prisma.category_to_article.create(
            data={
                [
                    {"category_id": cat_id, "article_id": article_id}
                    for cat_id in category_ids
                ]
            },
        )

    async def delete(self, article_id: int):
        article = await self.prisma.article.find_unique(where={"id": article_id})
        if not article:
            return None
        return await self.prisma.article.delete(where={"id": article_id})

    async def update(self, params: UpdateParams):
        article = await self.prisma.article.find_unique(where={"id": params.article_id})
        if not article:
            return None

        update_data = {}
        if params.title is not None:
            update_data["title"] = params.title
        if params.content is not None:
            update_data["content"] = params.content
        if params.categories is not None:
            update_data["categories"] = {
                "deleteMany": {},
                "create": [
                    {"category": {"connect": {"id": cat_id}}}
                    for cat_id in params.categories
                ],
            }

        updated_article = await self.prisma.article.update(
            where={"id": article.id},
            data=update_data,
            include={"user": True, "categories": {"include": {"category": True}}},
        )

        return updated_article
