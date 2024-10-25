from .category_repository import CategoryRepository
from typing import List


class CategoryService:
    def __init__(self):
        self.category_repository = CategoryRepository()

    async def get_categories(self):
        return await self.category_repository.get_all_categories()

    async def get_category(self, category_id: int):
        return await self.category_repository.get_category_by_id(category_id)

    async def get_categories_of_article(self, article_id: int):
        categories = await self.category_repository.get_categories_of_article(article_id)
        return [cat.category for cat in categories]

    async def update_article_categories(
        self, article_id: int, category_ids: List[int]
    ):
        await self.category_repository.update_article_categories(article_id, category_ids)
        
        return await self.get_categories_of_article(article_id)

    async def get_articles_by_category(self, category_id: int):
        return await self.category_repository.get_articles_by_category(category_id)

     """사용자가 선택한 카테고리 및 카테고리별 작성한 게시글 조회"""
    async def get_user_categories_and_articles(self, user_id: int):
        categories = await self.category_repository.get_user_categories_with_articles(user_id)
        result = []
        for category in categories:
                category_data = {
                    "id": category.id,
                    "name": category.name,
                    "articles": [article.article for article in category.articles],
                }
                result.append(category_data)
        return result
