from fastapi import APIRouter, status, Depends, Query, Body, Path

from resources.schemas.request import CommentCreate, CommentUpdate
from resources.comment.comment_service import CommentService
from resources.schemas.response import UserResponse, User
from resources.auth.auth_service import get_current_user

router = APIRouter(prefix="/comments", tags=["Comments"])


@router.get("/{comment_id}")
async def get_comments_by_id_handler(
    comment_id: int,
    comment_service: CommentService = Depends(),
):
    comments = await comment_service.find_by_id(comment_id)
    return comments


@router.get("/")
async def get_comments_by_filters_handler(
    article_id: int | None,
    user_id: int | None,
    comment_service: CommentService = Depends(),
):
    comments = await comment_service.find_by_filters(
        article_id=article_id, user_id=user_id
    )
    return comments


@router.post("/{article_id}")
async def create_comment_handler(
    article_id: int,
    comment: CommentCreate,
    comment_service: CommentService = Depends(),
    current_user: User | None = Depends(get_current_user),
):
    comment_data = comment.to_comment_data(
        user_id=current_user.id, article_id=article_id
    )
    new_comment = await comment_service.create(comment_data)

    return new_comment


@router.put("/{comment_id}")
async def update_comment_handler(
    comment_id: int,
    new_comment: CommentUpdate,
    comment_service: CommentService = Depends(),
    current_user: User | None = Depends(get_current_user),
):
    new_comment_data = new_comment.to_comment_data(
        user_id=current_user.id, article_id=comment_id
    )
    updated_comment = await comment_service.update(new_comment_data)

    return updated_comment


@router.delete("/{comment_id}")
async def delete_comment_handler(
    comment_id: int,
    comment_service: CommentService = Depends(),
    current_user: User | None = Depends(get_current_user),
):
    await comment_service.delete(user_id=current_user.id, comment_id=comment_id)
    return f"Comment with id:{comment_id} deleted"
