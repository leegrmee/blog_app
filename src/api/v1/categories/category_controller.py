from fastapi import APIRouter, Depends

from src.api.v1.categories.category_service import CategoryService
from src.schemas.response import (
    User,
    CategoriesResponse,
    CategoryToArticleResponse,
)
from src.api.v1.auth.auth_service import get_current_user

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("/", response_model=CategoriesResponse)
async def get_cats_handler(
    category_service: CategoryService = Depends(),
) -> CategoriesResponse:
    """Fetch all categories."""
    categories = await category_service.find_all()
    return CategoriesResponse(categories=categories)


@router.get("/of-article/", response_model=CategoryToArticleResponse)
async def get_cats_of_article_handler(
    article_id: int,
    category_service: CategoryService = Depends(),
    current_user: User | None = Depends(get_current_user),
) -> CategoryToArticleResponse:
    """Fetch categories of an article."""

    return await category_service.find_by_article_id(article_id=article_id)
