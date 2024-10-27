from config.Connection import prisma_connection
from typing import List, Dict, Any
from resources.schemas.response import CategoryResponse, ArticleResponse


class CategoryRepository:
    def __init__(self):
        self.prisma = prisma_connection.prisma

    # 모든 카테고리 조회
    async def get_all_categories(self) -> List[CategoryResponse]:
        categories = await self.prisma.category.find_many()
        return [CategoryResponse.model_validate(cat) for cat in categories]

    # 특정 ID의 카테고리 조회
    async def get_category_by_id(self, id: int) -> CategoryResponse | None:
        category = await self.prisma.category.find_unique(where={"id": id})
        return CategoryResponse.model_validate(category) if category else None

    # 특정 게시글의 카테고리 조회
    async def get_categories_of_article(self, articleId: int) -> List[CategoryResponse]:
        categories = await self.prisma.categorytoarticle.find_many(
            where={"articleId": articleId}, include={"category": True}
        )
        return [CategoryResponse.model_validate(cat.category) for cat in categories]

    # 게시글의 카테고리 업데이트
    async def update_article_categories(
        self, articleId: int, categoryIds: List[int]
    ) -> None:
        await self.prisma.categorytoarticle.delete_many(where={"articleId": articleId})
        new_connections = [
            {"articleId": articleId, "categoryId": catId} for catId in categoryIds
        ]
        await self.prisma.categorytoarticle.create_many(data=new_connections)

    # 카테고리 별 게시물
    async def get_articles_by_category(self, categoryId: int) -> List[ArticleResponse]:
        articles = await self.prisma.article.find_many(
            where={"categories": {"some": {"categoryId": categoryId}}},
            include={"user": True},
        )
        return [ArticleResponse.model_validate(article) for article in articles]

    async def get_user_categories_with_articles(
        self, userId: int
    ) -> List[CategoryResponse]:
        categories = await self.prisma.category.find_many(
            where={"articles": {"some": {"article": {"userId": userId}}}},
            include={
                "articles": {
                    "include": {"article": True},
                    "where": {"article": {"userId": userId}},
                }
            },
        )
        return [CategoryResponse.model_validate(category) for category in categories]
