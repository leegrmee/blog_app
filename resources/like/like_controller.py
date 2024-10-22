from fastapi import APIRouter
from resources.schemas.request import LikeCreate
from resources.schemas.response import LikeResponse

router = APIRouter(prefix="/likes")


@router.get("/{article_id}")
async def get_likes_of_article_handler(article_id: int):
    return {"likes": []}


@router.get("/{user_id}")
async def get_articles_liked_by_user_handler(user_id: int):
    return {"likes": []}


@router.post("/", response_model=LikeResponse)
async def create_like_handler(like: LikeCreate):
    return {"like": {}}


@router.delete("/{like_id}")
async def delete_like_handler(like_id: int):
    return {"message": "Like cancelled"}
