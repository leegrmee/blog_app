from .article_repository import ArticleRepository, SearchParams, UpdateParams
from ..like.like_repository import LikeRepository


class ArticleService:
    def __init__(self):
        self.article_repository = ArticleRepository()
        self.like_repository = LikeRepository()

    async def find_many(self, user_id: int, skip: int, limit: int):
        articles = await self.article_repository.find_many(
            user_id=user_id, skip=skip, limit=limit
        )
        return articles

    async def find_by_id(self, article_id: int):
        article = await self.article_repository.find_by_id(article_id=article_id)
        if article is None:
            return None

        # Increment view count
        updated_article = await self.article_repository.increment_view_count(
            article_id=article_id
        )
        return updated_article

    async def create(
        self, user_id: int, title: str, content: str, category_ids: list[int]
    ):
        new_article = await self.article_repository.create(
            user_id=user_id,
            title=title,
            content=content,
            category_ids=category_ids,
        )
        return new_article

    async def delete(self, article_id: int, user_id: int):
        article = await self.article_repository.find_by_id(article_id=article_id)
        if article is None or article.user_id != user_id:
            return None

        deleted_article = await self.article_repository.delete(article_id=article_id)
        return deleted_article

    async def update(self, request: UpdateParams):
        article = await self.article_repository.find_by_id(
            article_id=request.article_id
        )
        if article is None or article.user_id != request.user_id:
            return None

        updated_article = await self.article_repository.update(params=request)
        return updated_article

    async def search(self, request: SearchParams):
        articles = await self.article_repository.search(params=request)
        return articles

    def get_category_ids(self, categories):
        """Extract category IDs from category objects."""
        return [cat.category_id for cat in categories] if categories else []
