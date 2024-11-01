from fastapi import APIRouter, status, Depends, Query, Body, Path

from resources.schemas.request import CommentCreate, CommentUpdate
from resources.comment.comment_service import CommentService
from resources.schemas.response import User, CommentResponse, CommentUpdateResponse
from resources.auth.auth_service import get_current_user

router = APIRouter(prefix="/comments", tags=["Comments"])


@router.get("/")
async def get_comments_by_id_handler(
    comment_id: int,
    comment_service: CommentService = Depends(),
) -> CommentResponse:
    return await comment_service.find_by_id(comment_id)


@router.get("/by-filters")
async def get_comments_by_filters_handler(
    article_id: int | None,
    user_id: int | None,
    comment_service: CommentService = Depends(),
) -> list[CommentResponse]:

    comment_filters = {"article_id": article_id, "user_id": user_id}
    comments = await comment_service.find_by_filters(comment_filters)

    return comments


@router.post("/")
async def create_comment_handler(
    article_id: int,
    comment: CommentCreate,
    comment_service: CommentService = Depends(),
    current_user: User | None = Depends(get_current_user),
) -> CommentResponse:
    comment_data = comment.to_comment_data(
        user_id=current_user.id, article_id=article_id
    )
    new_comment = await comment_service.create(comment_data)

    return new_comment


@router.put("/")
async def update_comment_handler(
    new_comment: CommentUpdate,
    comment_service: CommentService = Depends(),
    current_user: User | None = Depends(get_current_user),
) -> CommentUpdateResponse:
    updated_comment = await comment_service.update(new_comment)
    return updated_comment


@router.delete("/")
async def delete_comment_handler(
    comment_id: int,
    comment_service: CommentService = Depends(),
    current_user: User | None = Depends(get_current_user),
):
    deleted_comment = await comment_service.delete(comment_id=comment_id)
    if deleted_comment is None:
        return f"Comment with id:{comment_id} not found"

    return f"Comment with id:{comment_id} deleted"
