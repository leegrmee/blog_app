from typing import Optional
from datetime import datetime
from ..schemas.response import ArticleResponse
from config.Connection import prisma_connection


class ArticleRepository:
    def __init__(self):
        self.prisma = prisma_connection.connect()

    async def get_all_articles(
        self, user_id: int, skip: int, limit: int
    ) -> list[ArticleResponse]:

        articles = await self.prisma.article.find_many(
            where={"user_id": user_id},
            skip=skip,
            take=limit,
            order={"created_at": "desc"},
        )
        return [ArticleResponse.model_validate(article) for article in articles]

    async def get_article_by_articleid(self, article_id: int) -> ArticleResponse | None:

        article = await self.prisma.article.find_unique(
            where={"id": article_id}, include={"user": True}
        )
        if article:
            return ArticleResponse.model_validate(article)

    async def increment_views(self, article_id: int) -> ArticleResponse | None:
        updated_article = await self.prisma.article.update(
            where={"id": article_id},
            data={
                "views": {"increment": 1}
            },  # {"increment": 1}= UPDATE Article SET views = views + 1 WHERE id = :article_id
            include={"user": True},
        )
        if updated_article:
            return ArticleResponse.model_validate(updated_article)

    async def search_articles(
        self,
        category_id: Optional[int] = None,
        user_id: Optional[int] = None,
        created_date: Optional[datetime] = None,
        updated_date: Optional[datetime] = None,
        skip: int = 0,
        limit: int = 10,
    ) -> list[ArticleResponse]:

        # Construct the filter conditions
        filters = {}
        if category_id is not None:
            filters["category_id"] = category_id
        if user_id is not None:
            filters["user_id"] = user_id
        if created_date is not None:
            filters["created_date"] = created_date
        if updated_date:
            filters["updated_date"] = updated_date

        # Use find_many with the constructed filters
        articles = await self.prisma.article.find_many(
            where=filters, skip=skip, take=limit
        )
        return [ArticleResponse.model_validate(article) for article in articles]

    async def create_article(
        self, user_id: int, title: str, content: str
    ) -> ArticleResponse:

        new_article = await self.prisma.article.create(
            data={
                "user_id": user_id,
                "title": title,
                "content": content,
            }
        )
        return ArticleResponse.model_validate(new_article)

    async def delete_article(self, article_id: int):
        article = await self.prisma.article.find_unique(where={"id": article_id})
        if not article:
            return None
        return await self.prisma.article.delete(where={"id": article_id})

    async def update_article(
        self, article_id: int, new_title: str, new_content: str
    ) -> ArticleResponse:

        article = await self.prisma.article.find_unique(where={"id": article_id})

        update_data = {}
        if new_title is not None:
            update_data["title"] = new_title
        if new_content is not None:
            update_data["content"] = new_content
        updated_article = await self.prisma.article.update(
            where={"id": article.id}, data=update_data
        )
        return ArticleResponse.model_validate(updated_article)
