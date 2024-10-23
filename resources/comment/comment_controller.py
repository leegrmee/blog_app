from fastapi import APIRouter, status, Depends, Query, Body
from typing import Optional
from resources.schemas.request import CommentCreate

router = APIRouter(prefix="/comments", tags=["Comments"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_comment_handler(comment: CommentCreate):
    return {"comment": {}}


@router.get("/", status_code=status.HTTP_200_OK)
async def get_comment_handler(
    comment_id: Optional[int] = Query(
        None, description="Filter comments by comment ID"
    ),
    article_id: Optional[int] = Query(
        None, description="Filter comments by article ID"
    ),
    user_id: Optional[int] = Query(None, description="Filter comments by user ID"),
):

    # 실제 구현에서는 데이터베이스에서 댓글을 조회합니다
    if comment_id is not None:
        return {"comment": {}}

    elif article_id is not None:
        # article_id로 필터링
        return {"comments": []}
    elif user_id is not None:
        # user_id로 필터링
        return {"comments": []}
    else:
        # 모든 댓글 반환
        return {"comments": []}


@router.put("/{user_id}/{comment_id}", status_code=status.HTTP_200_OK)
async def update_comment_handler(
    user_id: int,
    comment_id: int,
    comment: str = Body(...),
):
    return {"comment": {}}


@router.delete("/{user_id}/{comment_id}")
async def delete_comment_handler(comment_id: int):
    return {"message": f"Comment of {comment_id} deleted"}
