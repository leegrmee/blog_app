from fastapi import APIRouter, Body, HTTPException, Depends

from resources.category.category_service import CategoryService
from resources.schemas.response import User, CategoryResponse
from resources.auth.auth_service import get_current_user


router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("/")
async def get_cats_handler(category_service: CategoryService = Depends()):
    """fetch all categories"""
    return {"categories": await category_service.find_all()}


@router.get("/article/{article_id}")
async def get_cats_of_article_handler(
    article_id: int,
    category_service: CategoryService = Depends(),
    current_user: User | None = Depends(get_current_user),
):
    """fetch categories of an article"""
    return await category_service.find_by_article_id(article_id)


@router.get("/category/{category_id}/articles")
async def get_articles_by_cat_handler(
    category_id: int,
    category_service: CategoryService = Depends(),
):
    """fetch articles of a specific category"""
    return await category_service.find_articles_by_category(category_id)


@router.get("/user/{user_id}/categories-articles")
async def get_user_cats_and_articles_handler(
    user_id: int,
    category_service: CategoryService = Depends(),
    current_user: User | None = Depends(get_current_user),
):
    """fetch categories and articles of a specific user"""
    categories_with_articles = await category_service.find_by_user_id(
        user_id=current_user.id
    )
    return {
        "user_id": current_user.id,
        "categories_with_articles": categories_with_articles,
    }


# 게시물에서 카테고리 삭제
@router.delete("/article/{article_id}/{category_id}")
async def remove_cat_from_article_handler(
    article_id: int,
    category_id: int,
    category_service: CategoryService = Depends(),
    current_user: User | None = Depends(get_current_user),
):
    """remove a specific category from an article"""
    return await category_service.delete(article_id, category_id)
