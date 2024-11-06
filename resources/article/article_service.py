from fastapi import UploadFile
from resources.schemas.response import ArticleResponse
from resources.files.file_service import FileService
from .article_repository import ArticleRepository, SearchParams, UpdateParams
from ..like.like_repository import LikeRepository


class ArticleService:
    def __init__(self):
        self.article_repository = ArticleRepository()
        self.like_repository = LikeRepository()
        self.file_service = FileService()

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
        self,
        user_id: int,
        title: str,
        content: str,
        category_ids: list[int],
        files: list[UploadFile] | None = None,
    ):

        article = await self.article_repository.create(
            user_id=user_id,
            title=title,
            content=content,
            category_ids=category_ids,
        )
        if files:
            await self.file_service.upload(article_id=article.id, files=files)

        article_info = await self.article_repository.find_by_id(article_id=article.id)
        return self._process_article(article_info)

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

        file_urls = []
        for file in article.files:
            file_url = f"/files/{file.id}"
            file_urls.append(file_url)
        # article의 files 필드에 파일 URL 리스트 할당
        files = file_urls

        # Remove unnecessary data
        del article.likes
        del article.categories
        del article.files

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
            files=files,
        )
