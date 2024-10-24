from typing import List, Optional, datetime

from resources.article.article_repository import ArticleRepository
from resources.schemas.response import ArticleSchema


class ArticleService:
    def __init__(self):
        self.article_repository = ArticleRepository()

    def get_all_articles(
        self, user_id: int, skip: int, limit: int
    ) -> List[ArticleSchema]:
        return self.article_repository.get_all_articles(user_id, skip, limit)

    def get_article_by_id(self, article_id: int) -> Optional[ArticleSchema]:
        return self.article_repository.get_article_by_articleid(article_id)

    def search_articles(
        self,
        category_id: Optional[int] = None,
        user_id: Optional[int] = None,
        created_date: Optional[datetime] = None,
        updated_date: bool = False,
        skip: int = 0,
        limit: int = 10,
    ) -> List[ArticleSchema]:
        return self.article_repository.search_articles(
            category_id, user_id, created_date, updated_date, skip, limit
        )

    def create_article(self, user_id: int, title: str, content: str) -> ArticleSchema:
        return self.article_repository.create_article(user_id, title, content)

    def update_article(
        self, article_id: int, new_title: str, new_content: str
    ) -> ArticleSchema:
        return self.article_repository.update_article(
            article_id, new_title, new_content
        )

    def delete_article(self, article_id: int):
        return self.article_repository.delete_article(article_id)
