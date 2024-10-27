from fastapi import HTTPException, status

from resources.like.like_repository import LikeRepository
from resources.article.article_repository import ArticleRepository


class LikeService:
    def __init__(self):
        self.like_repository = LikeRepository()
        self.article_repository = ArticleRepository()

    async def like(self, dir: int, article_id: int, user_id: int):
        article = await self.article_repository.get_article_by_articleid(
            articleId=article_id
        )
        if not article:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Article with id: {article_id} does not exist",
            )

        found_like = await self.like_repository.get_like_by_article_id_and_user_id(
            articleId=article_id, userId=user_id
        )

        if dir == 1:
            if found_like:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"user {user_id} has alredy liked post {article_id}",
                )

            await self.like_repository.create_like(articleId=article_id, userId=user_id)
            return {"message": "successfully added like"}

        else:
            if not found_like:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Like does not exist"
                )

            await self.like_repository.cancel_like(articleId=article_id, userId=user_id)

            return {"message": "Like cancelled"}

    async def get_likes_count_by_article_id(self, article_id: int) -> int:
        return await self.like_repository.get_likes_count_by_article_id(
            articleId=article_id
        )
