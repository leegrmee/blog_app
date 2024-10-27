from fastapi import HTTPException, status
from datetime import datetime

from resources.category.category_repository import CategoryRepository
from .article_repository import ArticleRepository
from ..schemas.response import ArticleResponse


class ArticleService:
    def __init__(self):
        self.article_repository = ArticleRepository()
        self.category_repository = CategoryRepository()

    async def get_all_articles(
        self, user_id: int, skip: int, limit: int
    ) -> list[ArticleResponse]:
        return await self.article_repository.get_all_articles(
            userId=user_id, skip=skip, limit=limit
        )

    async def get_article_by_articleid(self, article_id: int) -> ArticleResponse:
        article = await self.article_repository.get_article_by_articleid(
            articleId=article_id
        )
        if article is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Article with id: {article_id} does not exist",
            )
        # 특정 게시물을 조회 할 때 조회수 증가
        updated_article = await self.article_repository.increment_views(
            articleId=article_id
        )
        if updated_article is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update view count",
            )

        return updated_article

    async def create_article(
        self, user_id: int, title: str, content: str, category_ids: list[int]
    ) -> ArticleResponse:

        new_article = await self.article_repository.create_article(
            userId=user_id,
            title=title,
            content=content,
        )

        if category_ids:
            await self.category_repository.update_article_categories(
                articleId=new_article.id, categoryIds=category_ids
            )

        return new_article

    async def delete_article(self, article_id: int, user_id: int):

        article = await self.article_repository.get_article_by_articleid(
            articleId=article_id
        )
        if article == None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Article with id: {article_id} does not exist",
            )

        if article.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to perform requested action",
            )
        # 게시물 삭제
        deleted_count = await self.article_repository.delete_article(
            articleId=article_id
        )

        if deleted_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Article with id: {article_id} could not be deleted",
            )

        return {"message": f"Article of {article_id} deleted"}

    async def update_article(
        self,
        article_id: int,
        user_id: int,
        new_title: str | None,
        new_content: str | None,
    ) -> ArticleResponse:

        article = await self.article_repository.get_article_by_articleid(
            articleId=article_id
        )
        if article is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Article with id: {article_id} does not exist",
            )
        if article.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to perform requested action",
            )

        updated_article = await self.article_repository.update_article(
            articleId=article_id, new_title=new_title, new_content=new_content
        )

        return updated_article

    async def search_articles(
        self,
        category_id: int | None,
        user_id: int | None,
        created_date: datetime | None,
        updated_date: datetime | None,
        skip: int = 0,
        limit: int = 10,
    ) -> list[ArticleResponse]:

        result = await self.article_repository.search_articles(
            categoryId=category_id,
            userId=user_id,
            createdAt=created_date,
            updatedAt=updated_date,
            skip=skip,
            limit=limit,
        )

        return result
