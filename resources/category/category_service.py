from .category_repository import CategoryRepository
from typing import List
from resources.schemas.response import CategoryResponse, ArticleResponse


class CategoryService:
    def __init__(self):
        self.category_repository = CategoryRepository()

    async def get_categories(self) -> List[CategoryResponse]:
        """모든 카테고리 조회"""
        return await self.category_repository.get_all_categories()

    async def get_category(self, category_id: int) -> CategoryResponse | None:
        """특정 카테고리 조회"""
        return await self.category_repository.get_category_by_id(id=category_id)

    async def get_categories_of_article(
        self, article_id: int
    ) -> List[CategoryResponse]:
        """특정 게시글의 카테고리 조회"""
        return await self.category_repository.get_categories_of_article(
            articleId=article_id
        )

    async def get_articles_by_category(self, category_id: int) -> List[ArticleResponse]:
        """특정 카테고리의 게시글 조회"""
        return await self.category_repository.get_articles_by_category(
            categoryId=category_id
        )

    async def get_user_categories_and_articles(
        self, user_id: int
    ) -> List[CategoryResponse]:
        """사용자가 선택한 카테고리 및 카테고리별 작성한 게시글 조회"""
        return await self.category_repository.get_user_categories_with_articles(
            userId=user_id
        )
