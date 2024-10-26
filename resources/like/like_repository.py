from config.Connection import prisma_connection


class LikeRepository:
    def __init__(self):
        self.prisma = prisma_connection.prisma.prisma

    async def create_like(self, article_id: int, user_id: int):
        return await self.prisma.like.create(
            {"data": {"article_id": article_id, "user_id": user_id}}
        )

    async def cancel_like(self, like_id: int):
        await self.prisma.like.delete({"where": {"id": like_id}})

    async def get_like_by_article_id_and_user_id(self, article_id: int, user_id: int):
        return await self.prisma.like.find_first(
            {"where": {"article_id": article_id, "user_id": user_id}}
        )

    async def get_likes_count_by_article_id(self, article_id: int) -> int:
        # 데이터베이스에서 해당 article_id에 대한 좋아요 수를 조회하는 쿼리
        # query = "SELECT COUNT(*) FROM likes WHERE article_id = :article_id"
        return await self.prisma.like.count({"where": {"article_id": article_id}})
