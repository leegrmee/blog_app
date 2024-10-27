from typing import Optional
from datetime import datetime
from ..schemas.response import ArticleResponse
from config.Connection import prisma_connection


class ArticleRepository:
    def __init__(self):
        self.prisma = prisma_connection.prisma

    async def get_all_articles(
        self, user_id: int, skip: int, limit: int
    ) -> list[ArticleResponse]:
        articles = await self.prisma.article.find_many(
            where={"userId": user_id},
            skip=skip,
            take=limit,
            order={"createdAt": "desc"},
            include={"user": True},
        )
        return [ArticleResponse.model_validate(article) for article in articles]

    async def get_article_by_articleid(self, articleId: int) -> ArticleResponse | None:

        article = await self.prisma.article.find_unique(
            where={"id": articleId}, include={"user": True}
        )
        if article:
            return ArticleResponse.model_validate(article)

    async def increment_views(self, articleId: int) -> ArticleResponse | None:
        updated_article = await self.prisma.article.update(
            where={"id": articleId},
            data={
                "views": {"increment": 1}
            },  # {"increment": 1}= UPDATE Article SET views = views + 1 WHERE id = :article_id
            include={"user": True},
        )
        if updated_article:
            return ArticleResponse.model_validate(updated_article)

    async def search_articles(
        self,
        categoryId: Optional[int] = None,
        userId: Optional[int] = None,
        createdAt: Optional[datetime] = None,
        updatedAt: Optional[datetime] = None,
        skip: int = 0,
        limit: int = 10,
    ) -> list[ArticleResponse]:
        filters = {}
        if categoryId is not None:
            filters["categories"] = {"some": {"categoryId": categoryId}}
        if userId is not None:
            filters["userId"] = userId
        if createdAt is not None:
            filters["createdAt"] = createdAt
        if updatedAt:
            filters["updatedAt"] = updatedAt

        articles = await self.prisma.article.find_many(
            where=filters,
            skip=skip,
            take=limit,
            include={"user": True, "categories": True},
        )
        return [ArticleResponse.model_validate(article) for article in articles]

    async def create_article(
        self, userId: int, title: str, content: str
    ) -> ArticleResponse:

        new_article = await self.prisma.article.create(
            data={
                "user": {"connect": {"id": userId}},
                "title": title,
                "content": content,
            }
        )
        return ArticleResponse.model_validate(new_article)

    async def delete_article(self, articleId: int):
        article = await self.prisma.article.find_unique(where={"id": articleId})
        if not article:
            return None
        return await self.prisma.article.delete(where={"id": articleId})

    async def update_article(
        self, articleId: int, new_title: str, new_content: str
    ) -> ArticleResponse:

        article = await self.prisma.article.find_unique(where={"id": articleId})

        update_data = {}
        if new_title is not None:
            update_data["title"] = new_title
        if new_content is not None:
            update_data["content"] = new_content
        updated_article = await self.prisma.article.update(
            where={"id": article.id}, data=update_data
        )
        return ArticleResponse.model_validate(updated_article)
