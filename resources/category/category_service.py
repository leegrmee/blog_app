from .category_repository import CategoryRepository
from resources.schemas.response import (
    CategoryInfo,
    CategoryToArticleResponse,
    ArticleToCategory,
)
from resources.exceptions import DatabaseException
import logging


class CategoryService:
    def __init__(self):
        self.category_repository = CategoryRepository()

    async def find_all(self):
        """Fetch all categories and their articles."""
        try:
            categories = await self.category_repository.find_all()
            # category.articles를 article 객체들의 리스트로 변환
            for category in categories:
                article_list = []
                for item in category.articles:
                    article = item.article
                    article.likes_count = len(article.likes) if article.likes else 0

                    del article.likes
                article_list.append(article)

                category.articles = article_list
            return categories

        except DatabaseException as e:
            logging.error(f"Database error in find_all: {e.detail}")
            raise e

    async def find_by_article_id(self, article_id: int):
        """Fetch categories associated with a specific article."""
        try:
            categories = await self.category_repository.find_by_article_id(
                article_id=article_id
            )

            if not categories:
                return None

            article_item = categories[0].articles[0].article
            article_item.likes_count = (
                len(article_item.likes) if article_item.likes else 0
            )
            del article_item.likes
            article = ArticleToCategory(
                **article_item.model_dump()
            )  # model_dump 로 딕셔너리 변환

            category_infos = []
            for category in categories:
                category_info = CategoryInfo(id=category.id, name=category.name)
                category_infos.append(category_info)

            response = CategoryToArticleResponse(
                article=article, categories=category_infos
            )
            return response

        except DatabaseException as e:
            logging.error(f"Database error in find_by_article_id: {e.detail}")
            raise e
