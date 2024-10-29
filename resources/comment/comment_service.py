from resources.comment.comment_repository import (
    CommentRepository,
    CommentFilters,
    CommentData,
)


class CommentService:
    def __init__(self):
        self.comment_repository = CommentRepository()

    async def find_by_id(self, comment_id: int):
        return await self.comment_repository.find_by_id(comment_id)

    async def find_by_filters(self, request: CommentFilters):
        return await self.comment_repository.find_by_filters(request)

    async def create(self, request: CommentData):
        return await self.comment_repository.create(request)

    async def update(self, request: CommentData):
        return await self.comment_repository.update(request)

    async def delete(self, user_id: int, comment_id: int):
        delete_comment = await self.comment_repository.find_by_id(comment_id)

        if not delete_comment:
            return f"Comment with id:{comment_id} not found"

        return await self.comment_repository.delete(
            user_id=user_id, comment_id=comment_id
        )
