from fastapi import APIRouter, status, Depends
from resources.schemas.request import LikeCreate
from resources.schemas.response import UserResponse
from resources.auth.auth_service import get_current_user
from resources.like.like_service import LikeService

router = APIRouter(prefix="/likes", tags=["Likes"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def like_handler(
    like: LikeCreate,
    like_service: LikeService = Depends(),
    current_user: UserResponse = Depends(get_current_user),
):

    await like_service.like(
        dir=like.dir, article_id=like.article_id, user_id=current_user.id
    )

    return {"like": {}}


@router.get("/{article_id}")
async def get_likes_of_article_handler(
    article_id: int, like_service: LikeService = Depends()
):

    likes_count = await like_service.get_likes_count_by_article_id(article_id)

    return {"likes_count": likes_count}
