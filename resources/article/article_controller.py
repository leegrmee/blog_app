from fastapi import APIRouter, status, Query, Depends
from typing import List

from resources.schemas.request import ArticleCreate, ArticleUpdate, ArticleSearch
from resources.schemas.response import ArticleSchema, UserSchema
from resources.article.article_service import ArticleService
from resources.auth.auth_service import AuthService

router = APIRouter(prefix="/articles", tags=["Articles"])


# 모든 게시물 조회
@router.get("/", status_code=status.HTTP_200_OK)
async def get_articles_handler(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=30),
    article_service: ArticleService = Depends(),
    current_user: UserSchema = Depends(AuthService.logged_in_user),
) -> List[ArticleSchema]:

    return await article_service.get_all_articles(
        user_id=current_user.id, skip=skip, limit=limit
    )


# 게시물 id로 조회
@router.get("/{article_id}", status_code=status.HTTP_200_OK)
async def get_article_handler(
    article_id: int,
    article_service: ArticleService = Depends(),
    current_user: UserSchema = Depends(AuthService.logged_in_user),
) -> ArticleSchema:
    article = await article_service.get_article_by_articleid(article_id=article_id)

    return article


# 게시물 검색
@router.post("/search", status_code=status.HTTP_200_OK)
async def search_articles_handler(
    search_params: ArticleSearch,
    article_service: ArticleService = Depends(),
    current_user: UserSchema = Depends(AuthService.logged_in_user),
) -> List[ArticleSchema]:
    return await article_service.search_articles(
        category_id=search_params.category_id,
        user_id=search_params.user_id,
        created_date=search_params.created_date,
        updated_date=search_params.updated_date,
        skip=search_params.skip,
        limit=search_params.limit,
    )


# 게시물 생성
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_article_handler(
    article: ArticleCreate,
    article_service: ArticleService = Depends(),
    current_user: UserSchema = Depends(AuthService.logged_in_user),
):

    new_article = await article_service.create_article(
        user_id=current_user.id, title=article.title, content=article.content
    )

    return {"article": {new_article}}


router.get("/{article_id}", status_code=status.HTTP_200_OK)


# 게시물 수정
@router.put("/{article_id}", status_code=status.HTTP_200_OK)
async def update_article_handler(
    article_id: int,
    updated_article: ArticleUpdate,
    article_service: ArticleService = Depends(),
    current_user: UserSchema = Depends(AuthService.logged_in_user),
):

    updated_article: ArticleSchema = await article_service.update_article(
        article_id=article_id,
        user_id=current_user.id,
        new_title=updated_article.title,
        new_content=updated_article.content,
    )

    return {"article": {updated_article}}


# 게시물 삭제
@router.delete("/{article_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_article_handler(
    article_id: int,
    article_service: ArticleService = Depends(),
    current_user: UserSchema = Depends(AuthService.logged_in_user),
):

    result = await article_service.delete_article(
        article_id=article_id, user_id=current_user.id
    )

    return result
