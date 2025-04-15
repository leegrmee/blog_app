from fastapi import APIRouter, status, Depends

from src.schemas.request import LikeCreate
from src.schemas.response import User
from src.api.v1.auth.auth_service import get_current_user
from src.api.v1.likes.like_service import LikeService

router = APIRouter(prefix="/likes", tags=["Likes"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def like_handler(
    like: LikeCreate,
    like_service: LikeService = Depends(),
    current_user: User | None = Depends(get_current_user),
):

    return await like_service.like(
        dir=like.dir, article_id=like.article_id, user_id=current_user.id
    )


# сделать артикл id как квери параметр
@router.get("/")
async def count_likes_of_article_handler(
    article_id: int, like_service: LikeService = Depends()
):

    return await like_service.count_likes(article_id)
