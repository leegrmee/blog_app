from config.Connection import prisma_connection


class LikeRepository:
    def __init__(self):
        self.prisma = prisma_connection.prisma

    async def add(self, article_id: int, user_id: int):
        return await self.prisma.like.create(
            {"data": {"article_id": article_id, "user_id": user_id}}
        )

    async def remove(self, article_id: int, user_id: int):
        await self.prisma.like.delete(
            {
                "where": {
                    "articleId_userId": {
                        "article_id": article_id,
                        "user_id": user_id,
                    }
                }
            }
        )

    async def find(self, article_id: int, user_id: int):
        return await self.prisma.like.find_first(
            {
                "where": {
                    "article_id": article_id,
                    "user_id": user_id,
                }
            }
        )

    async def count(self, article_id: int) -> int:
        return await self.prisma.like.count({"where": {"article_id": article_id}})
