from fastapi import UploadFile
from .article_repository import ArticleRepository, SearchParams, UpdateParams
from ..schemas.response import ArticleResponse, UserRole, User
from ..files.file_service import FileService
from ..like.like_repository import LikeRepository
from ..exceptions import PermissionDeniedException
import logging


class ArticleService:
    """
    ArticleService includes methods for
     - searching articles,
     - creating articles,
     - updating articles,
     - deleting articles.

    It also includes a staticmethod for transforming article data into ArticleResponse.
    """

    def __init__(self):
        self.article_repository = ArticleRepository()
        self.like_repository = LikeRepository()
        self.file_service = FileService()

    async def find_many(self, skip: int, limit: int):
        articles = await self.article_repository.find_many(skip=skip, limit=limit)
        return [self.process_article(article) for article in articles]

    async def find_by_id(self, article_id: int):
        article = await self.article_repository.find_by_id(article_id=article_id)
        # 조회수 증가
        await self.article_repository.increment_view_count(article_id=article_id)
        return self.process_article(article)

    async def search(self, params: SearchParams):
        # Create a SearchParams instance
        params = SearchParams(
            category_id=params.category_id,
            user_id=params.user_id,
            created_date=params.created_date,
            updated_date=params.updated_date,
            skip=params.skip,
            limit=params.limit,
        )

        articles = await self.article_repository.search(params)
        return [self.process_article(article) for article in articles]

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
            await self.file_service.upload(
                article_id=article.id, user_id=user_id, files=files
            )
        article_info = await self.article_repository.find_by_id(article_id=article.id)
        return self.process_article(article_info)

    async def update(self, params: UpdateParams, current_user: User):
        article = await self.article_repository.find_by_id(article_id=params.article_id)
        if article.user_id != current_user.id:
            raise PermissionDeniedException(
                detail="Only the author can update articles."
            )
        updated_article = await self.article_repository.update(params)
        return self.process_article(updated_article)

    async def delete(self, article_id: int, current_user: User):
        article = await self.article_repository.find_by_id(article_id=article_id)
        if article.user_id != current_user.id and current_user.role not in [
            UserRole.MODERATOR,
            UserRole.ADMIN,
        ]:
            raise PermissionDeniedException(
                detail="Insufficient permissions to delete the article."
            )

        # Fetch associated file IDs
        file_ids = [file.id for file in article.files]
        for file_id in file_ids:
            await self.file_service.delete(id=file_id, current_user=current_user)

        await self.article_repository.delete(article_id=article_id)

    @staticmethod
    def process_article(article):
        """
        This method processes article data for ArticleResponse.
        - Calculate likes_count
        - Extract category IDs
        - Extract file URLs
        """

        # Calculate likes_count
        article.likes_count = len(article.likes) if article.likes else 0

        # Extract category IDs
        categories = [item.category.id for item in article.categories]

        file_urls = [f"/files/{file.id}" for file in article.files]
        files = file_urls

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
