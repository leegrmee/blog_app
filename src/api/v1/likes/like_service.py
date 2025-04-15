from src.api.v1.likes.like_repository import LikeRepository
from src.api.v1.articles.article_repository import ArticleRepository


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

            else:
                await self.like_repository.add(article_id=article_id, user_id=user_id)
                await self.article_repository.increment_likes_count(article_id)
                return "successfully added like"

        else:
            if not found_like:
                return "You never liked this post before"

            await self.like_repository.remove(article_id=article_id, user_id=user_id)
            await self.article_repository.decrement_likes_count(article_id)

            return "Like cancelled"

    async def count_likes(self, article_id: int) -> int:
        count = await self.like_repository.count(article_id)
        await self.article_repository.set_likes_count(article_id, count)

        return count
