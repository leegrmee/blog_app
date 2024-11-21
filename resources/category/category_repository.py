from config.Connection import prisma_connection
from prisma.errors import PrismaError
import logging
from resources.exceptions import DatabaseException


class CategoryRepository:
    def __init__(self):
        self.prisma = prisma_connection.prisma

    async def find_all(self) -> list:
        try:
            return await self.prisma.category.find_many(
                include={
                    "articles": {
                        "include": {
                            "article": {
                                "include": {
                                    "likes": True  # likes 관계를 포함하여 가져옵니다.
                                }
                            }
                        }
                    }
                }
            )
        except PrismaError as e:
            logging.error(f"Error in find_all: {e}")
            raise DatabaseException(
                detail="Database error occurred while fetching categories."
            )

    async def find_by_article_id(self, article_id: int):
        try:
            return await self.prisma.category.find_many(
                where={"articles": {"some": {"article_id": article_id}}},
                include={
                    "articles": {
                        "include": {
                            "article": {
                                "include": {
                                    "likes": True,
                                }
                            }
                        },
                        "where": {"article_id": article_id},
                    }
                },
            )
        except PrismaError as e:
            logging.error(f"Error in find_by_article_id: {e}")
            raise DatabaseException(
                detail="Database error occurred while fetching categories."
            )

    async def update(self, article_id: int, category_ids: list[int]):
        try:
            async with self.prisma.transaction():
                await self.prisma.category_to_article.delete_many(
                    where={"article_id": article_id}
                )
                if category_ids:
                    new_connections = [
                        {"article_id": article_id, "category_id": cat_id}
                        for cat_id in category_ids
                    ]
                    await self.prisma.category_to_article.create_many(
                        data=new_connections
                    )
        except PrismaError as e:
            logging.error(f"Error in update: {e}")
            raise DatabaseException(
                detail="Database error occurred while updating categories."
            ) from e
