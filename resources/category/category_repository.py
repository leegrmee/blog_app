from config.Connection import prisma_connection


class CategoryRepository:
    def __init__(self):
        self.prisma = prisma_connection.prisma

    async def find_all(self) -> list:
        return await self.prisma.category.find_many(
            include={"articles": {"include": {"article": True}}}
        )

    async def find_by_id(self, id: int):
        return await self.prisma.category.find_unique(
            where={"id": id}, include={"articles": {"include": {"article": True}}}
        )

    async def find_by_article_id(self, article_id: int):
        return await self.prisma.category.find_many(
            where={"articles": {"some": {"article_id": article_id}}}
        )

    # prism client py 에서 select 대신 include 사용

    # 유저가 쓴 게시물에 속한 카테고리 찾기
    async def find_by_user_id(self, user_id: int):
        return await self.prisma.category.find_many(
            where={"articles": {"some": {"article": {"user_id": user_id}}}},
            include={
                "articles": {
                    "include": {"article": True},
                    "where": {"article": {"user_id": user_id}},
                }
            },
        )

    async def delete(self, article_id: int, category_id: int):
        await self.prisma.category_to_article.delete(
            where={
                "article_id_category_id": {
                    "article_id": article_id,
                    "category_id": category_id,
                }
            }
        )

    async def update(self, article_id: int, category_ids: list[int]):
        await self.prisma.category_to_article.delete_many(
            where={"article_id": article_id}
        )
        if category_ids:
            new_connections = [
                {"article_id": article_id, "category_id": cat_id}
                for cat_id in category_ids
            ]
            await self.prisma.category_to_article.create_many(data=new_connections)
