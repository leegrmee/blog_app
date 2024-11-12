from fastapi import UploadFile, HTTPException
from resources.schemas.response import ArticleResponse, UserRole, User
from resources.files.file_service import FileService
from .article_repository import ArticleRepository, SearchParams, UpdateParams
from ..like.like_repository import LikeRepository


class ArticleService:
    def __init__(self):
        self.article_repository = ArticleRepository()
        self.like_repository = LikeRepository()
        self.file_service = FileService()

    async def find_many(self, skip: int, limit: int):
        articles = await self.article_repository.find_many(skip=skip, limit=limit)

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
            await self.file_service.upload(
                article_id=article.id, user_id=user_id, files=files
            )

        article_info = await self.article_repository.find_by_id(article_id=article.id)
        return self._process_article(article_info)

    async def update(self, params: UpdateParams, current_user: User):
        article = await self.article_repository.find_by_id(article_id=params.article_id)
        if not article:
            raise HTTPException(status_code=404, detail="Article not found")

        if article.user_id != current_user.id:
            raise HTTPException(
                status_code=403, detail="You are not the author of this article"
            )

        updated_article = await self.article_repository.update(params)
        return self._process_article(updated_article)

    async def delete(self, article_id: int, current_user: User):
        article = await self.article_repository.find_by_id(article_id=article_id)
        if not article:
            raise HTTPException(status_code=404, detail="Article not found")

        # Check if the user is the author, moderator, or administrator
        if article.user_id != current_user.id and current_user.role not in [
            UserRole.MODERATOR,
            UserRole.ADMIN,
        ]:
            raise HTTPException(
                status_code=403, detail="Insufficient permissions to delete the article"
            )

        await self.article_repository.delete(article_id=article_id)
        return

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
