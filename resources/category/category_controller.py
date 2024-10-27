from fastapi import APIRouter, Body, HTTPException, Depends

from resources.category.category_service import CategoryService
from resources.schemas.response import User
from resources.auth.auth_service import get_current_user


router = APIRouter(prefix="/categories", tags=["Categories"])


# 모든 카테고리 조회
@router.get("/")
async def get_cats_handler(category_service: CategoryService = Depends()):
    """모든 카테고리 조회"""
    return {"categories": await category_service.get_categories()}


# 게시물에 카테고리 할당
@router.post("/article/{article_id}")
async def select_cats_for_article_handler(
    article_id: int,
    category_ids: list[int] = Body(...),
    category_service: CategoryService = Depends(),
    current_user: User | None = Depends(get_current_user),
):
    """게시글에 카테고리 할당 (복수 선택 가능)"""
    updated_categories = await category_service.update_article_categories(
        article_id, category_ids
    )
    return {"article_id": article_id, "categories": updated_categories}


# 각 게시글의 카테고리 조회
@router.get("/article/{article_id}")
async def get_cats_of_article_handler(
    article_id: int,
    category_service: CategoryService = Depends(),
    current_user: User | None = Depends(get_current_user),
):
    """게시글의 카테고리 조회"""
    categories = await category_service.get_categories_of_article(article_id)
    return {"article_id": article_id, "categories": categories}


# 게시물에서 카테고리 삭제
@router.delete("/article/{article_id}/{category_id}")
async def remove_cat_from_article_handler(
    article_id: int,
    category_id: int,
    category_service: CategoryService = Depends(),
    current_user: User | None = Depends(get_current_user),
):
    """게시글에서 특정 카테고리 제거"""
    updated_categories = await category_service.remove_category_from_article(
        article_id, category_id
    )
    return {"article_id": article_id, "categories": updated_categories}


# 카테고리별 게시글 조회
@router.get("/category/{category_id}/articles")
async def get_articles_by_cat_handler(
    category_id: int,
    category_service: CategoryService = Depends(),
):
    """특정 카테고리에 속한 게시글 조회"""
    articles = await category_service.get_articles_by_category(category_id)
    return {"category_id": category_id, "articles": articles}


# 유저별 카테고리 및 게시글 조회
@router.get("/user/{user_id}/categories-articles")
async def get_user_cats_and_articles_handler(
    user_id: int,
    category_service: CategoryService = Depends(),
    current_user: User | None = Depends(get_current_user),
):

    categories_with_articles = await category_service.get_user_categories_and_articles(
        user_id=current_user.id
    )
    return {
        "user_id": current_user.id,
        "categories_with_articles": categories_with_articles,
    }
