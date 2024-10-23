from fastapi import APIRouter, status, Query
from typing import Optional
from resources.schemas.request import ArticleCreate, ArticleUpdate

router = APIRouter(prefix="/articles", tags=["Articles"])


@router.get("/", status_code=status.HTTP_200_OK)
async def get_articles_handler(
    article_id: Optional[int] = Query(None, description="Filter article by article ID"),
    user_id: Optional[int] = Query(None, description="Filter articles by user ID"),
):

    if article_id is not None:
        # article_id로 필터링
        return {"article": []}
    elif user_id is not None:
        # user_id로 필터링
        return {"articles": []}
    else:
        # 모든 댓글 반환
        return {"articles": []}


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_article_handler(
    article: ArticleCreate,
):
    return {"article": {}}


@router.put("/{article_id}", status_code=status.HTTP_200_OK)
async def update_article_handler(article_id: int, updated_article: ArticleUpdate):
    return {"article": {}}


@router.delete("/{article_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_article_handler(article_id: int):
    return {"message": f"Article of {article_id} deleted"}
