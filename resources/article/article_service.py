from .article_repository import ArticleRepository, SearchParams, UpdateParams
from ..like.like_repository import LikeRepository
from resources.schemas.response import ArticleResponse


class ArticleService:
    def __init__(self):
        self.article_repository = ArticleRepository()
        self.like_repository = LikeRepository()

    async def find_many(self, user_id: int, skip: int, limit: int):
        articles = await self.article_repository.find_many(
            user_id=user_id, skip=skip, limit=limit
        )
        return [self._process_article(article) for article in articles]

    async def find_by_id(self, article_id: int):
        article = await self.article_repository.find_by_id(article_id=article_id)
        if article:
            return self._process_article(article)

        # Increment view count
        await self.article_repository.increment_view_count(article_id=article_id)

    async def create(
        self, user_id: int, title: str, content: str, category_ids: list[int]
    ):
        article = await self.article_repository.create(
            user_id=user_id,
            title=title,
            content=content,
            category_ids=category_ids,
        )
        return self._process_article(article)

    async def update(self, params: UpdateParams):
        article = await self.article_repository.update(params)
        if article:
            return self._process_article(article)
        return None

    async def delete(self, article_id: int, user_id: int):
        article = await self.article_repository.find_by_id(article_id=article_id)
        if article and article.user_id == user_id:
            return await self.article_repository.delete(article_id=article_id)
        return None

    async def search(self, params: SearchParams):
        articles = await self.article_repository.search(params)
        return [self._process_article(article) for article in articles]

    def _process_article(self, article):
        """Process article data"""
        # Calculate likes_count
        article.likes_count = len(article.likes) if article.likes else 0

        # Extract category IDs
        categories = [item.category.id for item in article.categories]

        # Remove unnecessary data
        del article.likes
        del article.categories

        # Return processed article
        return ArticleResponse(
            id=article.id,
            user_id=article.user_id,
            title=article.title,
            content=article.content,
            views=article.views,
            created_at=article.created_at,
            updated_at=article.updated_at,
            categories=categories,
            likes_count=article.likes_count,
        )
