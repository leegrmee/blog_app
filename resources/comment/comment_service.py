from resources.comment.comment_repository import CommentRepository
from fastapi import HTTPException, status
from typing import Optional


class CommentService:
    def __init__(self):
        pass

    async def get_comments(
        self,
        comment_id: Optional[int] = None,
        article_id: Optional[int] = None,
        user_id: Optional[int] = None,
    ):
        comments = await CommentRepository.get_comments(
            comment_id=comment_id, article_id=article_id, user_id=user_id
        )

        if comment_id is not None:
            return {"comment": comments[0] if comments else {}}
        elif article_id is not None:
            return {"comments": comments}
        elif user_id is not None:
            return {"comments": comments}
        else:
            return {"comments": comments}

    async def create_comment(self, user_id: int, article_id: int, content: str):
        return await CommentRepository.create_comment(
            user_id=user_id, article_id=article_id, content=content
        )

    async def update_comment(self, user_id: int, comment_id: int, content: str):
        return await CommentRepository.update_comment(
            user_id=user_id, comment_id=comment_id, content=content
        )

    async def delete_comment(self, user_id: int, comment_id: int):
        delete_comment = await self.get_comment(comment_id=comment_id)
        if not delete_comment.get("comment"):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Comment with id: {comment_id} does not exist",
            )
        return await CommentRepository.delete_comment(
            user_id=user_id, comment_id=comment_id
        )
