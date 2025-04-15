from prisma.errors import PrismaError
import logging


from src.core.database.base_repo import BaseRepository
from src.core.exceptions.base import DatabaseException


class CategoryRepository(BaseRepository):
    def __init__(self):
        super().__init__("category")

    async def find_all(self) -> list:
        """
        모든 카테고리를 조회합니다.
        """
        try:
            return await super().find_many(
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
        """
        특정 게시글의 카테고리를 조회합니다.
        """
        try:
            return await super().find_many(
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
        """
        게시글의 카테고리를 업데이트합니다.
        """
        try:
            async with self.prisma.tx() as transaction:
                await transaction.category_to_article.delete_many(
                    where={"article_id": article_id}
                )
                if category_ids:
                    new_connections = [
                        {"article_id": article_id, "category_id": cat_id}
                        for cat_id in category_ids
                    ]
                    await transaction.category_to_article.create_many(
                        data=new_connections
                    )
        except PrismaError as e:
            logging.error(f"Error in update: {e}")
            raise DatabaseException(
                detail="Database error occurred while updating categories."
            ) from e
