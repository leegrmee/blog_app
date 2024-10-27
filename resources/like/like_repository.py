from config.Connection import prisma_connection


class LikeRepository:
    def __init__(self):
        self.prisma = prisma_connection.prisma.prisma

    async def create_like(self, articleId: int, userId: int):
        return await self.prisma.like.create(
            {"data": {"articleId": articleId, "userId": userId}}
        )

    async def cancel_like(self, articleId: int, userId: int):
        await self.prisma.like.delete(
            {"where": {"articleId_userId": {"articleId": articleId, "userId": userId}}}
        )

    async def get_like_by_article_id_and_user_id(self, articleId: int, userId: int):
        return await self.prisma.like.find_first(
            {"where": {"articleId": articleId, "userId": userId}}
        )

    async def get_likes_count_by_article_id(self, articleId: int) -> int:
        return await self.prisma.like.count({"where": {"articleId": articleId}})
