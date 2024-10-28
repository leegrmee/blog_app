from config.Connection import prisma_connection
from resources.schemas.response import CategoryResponse, ArticleResponse


class CategoryRepository:
    def __init__(self):
        self.prisma = prisma_connection.prisma

    # 모든 카테고리 조회
    async def get_all_categories(self) -> list[CategoryResponse]:
        categories = await self.prisma.category.find_many(
            include={"articles": {"include": {"article": True}}}
        )

        result = [
            CategoryResponse(
                id=cat.id,
                name=cat.name,
                articles=[
                    ArticleResponse.model_validate(cat_to_article.article)
                    for cat_to_article in cat.articles
                ],
            )
            for cat in categories
        ]
        return result

    # 특정 ID의 카테고리 조회
    async def get_category_by_id(self, id: int) -> CategoryResponse | None:
        category = await self.prisma.category.find_unique(
            where={"id": id}, include={"articles": {"include": {"article": True}}}
        )
        if category:
            return CategoryResponse(
                id=category.id,
                name=category.name,
                articles=[
                    ArticleResponse.model_validate(cat_to_article.article)
                    for cat_to_article in category.articles
                ],
            )

        else:
            return None

    # 특정 게시글의 카테고리 조회
    async def get_categories_of_article(self, articleId: int) -> list[CategoryResponse]:
        categories = await self.prisma.categorytoarticle.find_many(
            where={"articleId": articleId}, include={"category": True}
        )
        return [CategoryResponse.model_validate(cat.category) for cat in categories]

    # 게시글의 카테고리 업데이트
    async def update_article_categories(
        self, articleId: int, categoryIds: list[int]
    ) -> None:
        await self.prisma.categorytoarticle.delete_many(where={"articleId": articleId})
        new_connections = [
            {"articleId": articleId, "categoryId": catId} for catId in categoryIds
        ]
        await self.prisma.categorytoarticle.create_many(data=new_connections)

    # 카테고리 별 게시물
    async def get_articles_by_category(self, categoryId: int) -> list[ArticleResponse]:
        articles = await self.prisma.article.find_many(
            where={"categories": {"some": {"categoryId": categoryId}}},
            include={"user": True},
        )
        return [ArticleResponse.model_validate(article) for article in articles]

    async def get_user_categories_with_articles(
        self, userId: int
    ) -> list[CategoryResponse]:
        categories = await self.prisma.category.find_many(
            where={"articles": {"some": {"article": {"userId": userId}}}},
            include={
                "articles": {
                    "include": {"article": True},
                    "where": {"article": {"userId": userId}},
                }
            },
        )

        result = [
            CategoryResponse(
                id=category.id,
                name=category.name,
                articles=[
                    ArticleResponse.model_validate(cat_to_article.article)
                    for cat_to_article in category.articles
                ],
            )
            for category in categories
        ]
        return result

    # 게시글에서 특정 카테고리 제거
    async def remove_category_from_article(self, articleId: int, categoryId: int):
        await self.prisma.categorytoarticle.delete(
            where={
                "articleId_categoryId": {
                    "articleId": articleId,
                    "categoryId": categoryId,
                }
            }
        )

        # Prisma에서는 복합 키(@@id([articleId, categoryId]))로 정의된 경우, delete 메서드에서 where 조건을 { "field1_field2": {"field1": value1, "field2": value2} } 형태로 지정
