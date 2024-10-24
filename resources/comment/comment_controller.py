from fastapi import APIRouter, status, Depends, Query, Body, Path
from typing import Optional

from resources.schemas.request import CommentCreate, CommentUpdate
from resources.comment.comment_service import CommentService
from resources.user.user_service import UserService
from resources.schemas.response import UserSchema

router = APIRouter(prefix="/comments", tags=["Comments"])


def get_comment_service():
    return CommentService()


@router.get("/", status_code=status.HTTP_200_OK)
async def get_comment_handler(
    comment_id: Optional[int] = Query(
        None, description="Filter comments by comment ID"
    ),
    article_id: Optional[int] = Query(
        None, description="Filter comments by article ID"
    ),
    user_id: Optional[int] = Query(None, description="Filter comments by user ID"),
    comment_service: CommentService = Depends(get_comment_service),
    current_user: UserSchema = Depends(UserService.logged_in_user),
):
    comments = await comment_service.get_comments(
        comment_id=comment_id, article_id=article_id, user_id=user_id
    )
    return comments


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_comment_handler(
    comment: CommentCreate = Body(..., description="Comment to create"),
    comment_service: CommentService = Depends(get_comment_service),
    current_user: UserSchema = Depends(UserService.logged_in_user),
):
    return {"comment": {}}


@router.put("/{comment_id}", status_code=status.HTTP_200_OK)
async def update_comment_handler(
    comment_id: int = Path(..., description="The ID of the comment to update"),
    new_comment: CommentUpdate = Body(..., description="Updated comment content"),
    comment_service: CommentService = Depends(get_comment_service),
    current_user: UserSchema = Depends(UserService.logged_in_user),
):
    updated_comment = await comment_service.update_comment(
        user_id=current_user.id, comment_id=comment_id, comment=new_comment.content
    )
    return {"comment": updated_comment}


@router.delete("/{comment_id}", status_code=status.HTTP_200_OK)
async def delete_comment_handler(
    comment_id: int = Path(..., description="The ID of the comment to delete"),
    comment_service: CommentService = Depends(get_comment_service),
    current_user: UserSchema = Depends(UserService.logged_in_user),
):
    await comment_service.delete_comment(user_id=current_user.id, comment_id=comment_id)
    return {"message": f"Comment of {comment_id} deleted"}
