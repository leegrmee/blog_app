from src.api.v1.comments.comment_repository import (
    CommentRepository,
    CommentFilters,
    CommentData,
    UpdateCommentData,
)
from src.schemas.response import User, UserRole
from fastapi import HTTPException


class CommentService:
    def __init__(self):
        self.comment_repository = CommentRepository()

    async def find_many(self, skip: int = 0, limit: int = 10):
        return await self.comment_repository.find_many(skip=skip, limit=limit)

    async def find_by_filters(self, request: CommentFilters):
        return await self.comment_repository.find_by_filters(request)

    async def create(self, request: CommentData):
        return await self.comment_repository.create(request)

    async def update(self, request: UpdateCommentData, current_user: User):
        comment = await self.comment_repository.find_by_id(request["id"])
        if comment is None:
            raise HTTPException(status_code=404, detail="Comment not found")

        if comment.user_id != current_user.id:
            raise HTTPException(
                status_code=403, detail="Insufficient permissions to update the comment"
            )

        return await self.comment_repository.update(request)

    async def delete(self, comment_id: int, current_user: User):
        comment = await self.comment_repository.find_by_id(comment_id)
        if comment is None:
            return HTTPException(
                status_code=404, detail="You are not the author of this comment"
            )

        if comment.user_id != current_user.id and current_user.role not in [
            UserRole.MODERATOR,
            UserRole.ADMIN,
        ]:
            raise HTTPException(
                status_code=403, detail="Insufficient permissions to delete the comment"
            )

        await self.comment_repository.delete(comment_id=comment_id)
        return
