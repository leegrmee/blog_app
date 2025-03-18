from resources.base_repository import BaseRepository


class LikeRepository(BaseRepository):
    def __init__(self):
        super().__init__("like")

    async def add(self, article_id: int, user_id: int):
        """
        좋아요를 추가합니다.
        """
        return await super().create(
            data={
                "article": {"connect": {"id": article_id}},
                "user": {"connect": {"id": user_id}},
            }
        )

    async def remove(self, article_id: int, user_id: int):
        """
        좋아요를 제거합니다.
        """
        return await super().delete(
            where={
                "article_id_user_id": {
                    "article_id": article_id,
                    "user_id": user_id,
                }
            }
        )

    async def find(self, article_id: int, user_id: int):
        """
        특정 사용자의 특정 게시글에 대한 좋아요를 조회합니다.
        """
        return await super().find_unique(
            where={
                "article_id_user_id": {
                    "article_id": article_id,
                    "user_id": user_id,
                }
            }
        )

    async def count(self, article_id: int) -> int:
        """
        특정 게시글의 좋아요 수를 조회합니다.
        """
        return await super().count(where={"article_id": article_id})
