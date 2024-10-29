from fastapi import HTTPException, status

from resources.like.like_repository import LikeRepository
from resources.article.article_repository import ArticleRepository


class LikeService:
    def __init__(self):
        self.like_repository = LikeRepository()
        self.article_repository = ArticleRepository()

    async def like(self, dir: int, article_id: int, user_id: int):
        article = await self.article_repository.find_by_id(article_id)
        if not article:
            return None

        found_like = await self.like_repository.find(
            article_id=article_id, user_id=user_id
        )

        if dir == 1:
            if found_like:
                return f"You have alredy liked post: {article_id}"

            await self.like_repository.add(article_id=article_id, user_id=user_id)
            return "successfully added like"

        else:
            if not found_like:
                return "You never liked this post before"

            await self.like_repository.remove(article_id=article_id, user_id=user_id)

            return "Like cancelled"

    async def count_likes(self, article_id: int) -> int:
        return await self.like_repository.count(article_id)
