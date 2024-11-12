from fastapi import APIRouter, Depends, Query

from resources.schemas.request import CommentCreate, CommentUpdate
from resources.comment.comment_service import CommentService
from resources.schemas.response import (
    User,
    CommentResponse,
    CommentUpdateResponse,
    UserRole,
)
from resources.auth.auth_service import get_current_user
from resources.auth.role_dependency import require_minimum_role

router = APIRouter(prefix="/comments", tags=["Comments"])


@router.get("/")
async def get_comments_handler(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=30),
    comment_service: CommentService = Depends(),
) -> list[CommentResponse]:
    return await comment_service.find_many(skip=skip, limit=limit)


@router.get("/by-filters")
async def get_comments_by_filters_handler(
    article_id: int | None = None,
    user_id: int | None = None,
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
    authorized_user: User | None = Depends(require_minimum_role(UserRole.AUTHOR)),
) -> CommentResponse:
    comment_data = comment.to_comment_data(
        user_id=authorized_user.id, article_id=article_id
    )
    new_comment = await comment_service.create(comment_data)

    return new_comment


@router.put("/")
async def update_comment_handler(
    new_comment: CommentUpdate,
    comment_service: CommentService = Depends(),
    current_user: User | None = Depends(get_current_user),
) -> CommentUpdateResponse:
    new_comment = new_comment.to_comment_data(user_id=current_user.id)
    updated_comment = await comment_service.update(new_comment, current_user)
    return updated_comment


@router.delete("/{comment_id}")
async def delete_comment_handler(
    comment_id: int,
    comment_service: CommentService = Depends(),
    current_user: User | None = Depends(get_current_user),
):
    deleted_comment = await comment_service.delete(
        comment_id, current_user=current_user
    )
    if deleted_comment is None:
        return f"Comment with id:{comment_id} not found"

    return f"Comment with id:{comment_id} deleted"
