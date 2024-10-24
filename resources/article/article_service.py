from fastapi import HTTPException, status
from typing import List, Optional
from datetime import datetime

from .article_repository import ArticleRepository
from ..schemas.response import ArticleSchema


class ArticleService:

    async def get_all_articles(self, user_id: int, skip: int, limit: int):
        return await ArticleRepository.get_all_articles(
            user_id=user_id, skip=skip, limit=limit
        )

    async def get_article_by_articleid(self, article_id: int) -> ArticleSchema:
        article = await ArticleRepository.get_article_by_articleid(
            article_id=article_id
        )
        if article is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Article with id: {article_id} does not exist",
        )
        return article

    async def search_articles(
        self,
        category_id: Optional[int] = None,
        user_id: Optional[int] = None,
        created_date: Optional[datetime] = None,
        updated_date: bool = False,
        skip: int = 0,
        limit: int = 10,
    ) -> List[ArticleSchema]:
        
        return await ArticleRepository.search_articles(
            category_id=category_id,
            user_id=user_id,
            created_date=created_date,
            updated_date=updated_date,
            skip=skip,
            limit=limit,
        )
    

    async def create_article(self, user_id: int, title: str, content: str):

        new_article = await ArticleRepository.create_article(
            user_id=user_id, title=title, content=content
        )

        return new_article

    async def delete_article(self, article_id: int, user_id: int):

        article = await ArticleRepository.get_article_by_articleid(
            article_id=article_id
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
        deleted_count = await ArticleRepository.delete_article(article_id)

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
        new_title: Optional[str],
        new_content: Optional[str],
    ) -> ArticleSchema:

        article = await ArticleRepository.get_article_by_articleid(
            article_id=article_id
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

        updated_article = await ArticleRepository.update_article(
            article_id=article_id, new_title=new_title, new_content=new_content
        )

        return updated_article
