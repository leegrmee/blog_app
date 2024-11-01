from resources.comment.comment_repository import (
    CommentRepository,
    CommentFilters,
    CommentData,
    UpdateCommentData,
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

    async def update(self, request: UpdateCommentData):

        data = UpdateCommentData(id=request.id, new_content=request.new_content)
        return await self.comment_repository.update(data)

    async def delete(self, comment_id: int):
        return await self.comment_repository.delete(comment_id=comment_id)
