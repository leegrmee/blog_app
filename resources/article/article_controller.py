from fastapi import APIRouter, status, Depends, UploadFile, Query, Form, File

from resources.schemas.request import ArticleUpdate, ArticleSearch
from resources.schemas.response import ArticleResponse, User, UserRole
from resources.article.article_service import ArticleService
from resources.auth.auth_service import get_current_user
from resources.auth.role_dependency import require_minimum_role

router = APIRouter(prefix="/articles", tags=["Articles"])


@router.get("/", status_code=status.HTTP_200_OK)
async def get_articles_handler(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=30),
    article_service: ArticleService = Depends(),
    current_user: User | None = Depends(get_current_user),
) -> list[ArticleResponse]:

    articles = await article_service.find_many(skip=skip, limit=limit)

    return articles


@router.get("/{article_id}", status_code=status.HTTP_200_OK)
async def get_article_handler(
    article_id: int,
    article_service: ArticleService = Depends(),
    current_user: User | None = Depends(get_current_user),
) -> ArticleResponse:

    article = await article_service.find_by_id(article_id=article_id)
    if not article:
        return {"message": f"Article with id {article_id} not found"}

    return article


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_article_handler(
    title: str = Form(...),
    content: str = Form(...),
    select_categories: str = Form(...),
    files: list[UploadFile] = File(None),
    article_service: ArticleService = Depends(),
    authorized_user: User = Depends(require_minimum_role(UserRole.AUTHOR)),
) -> ArticleResponse:

    # Parse select_categories into a list of integers
    category_ids = [
        int(id.strip()) for id in select_categories.split(",") if id.strip().isdigit()
    ]

    # Call the service layer with the parsed data
    article = await article_service.create(
        user_id=authorized_user.id,
        title=title,
        content=content,
        category_ids=category_ids,
        files=files,
    )
    return article


@router.put("/", status_code=status.HTTP_200_OK)
async def update_article_handler(
    article_id: int,
    update_article: ArticleUpdate,
    article_service: ArticleService = Depends(),
    current_user: User = Depends(get_current_user),
) -> ArticleResponse:

    update_params = update_article.to_update_data(
        article_id=article_id, user_id=current_user.id
    )

    updated_article = await article_service.update(update_params, current_user)
    return updated_article


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_article_handler(
    article_id: int,
    article_service: ArticleService = Depends(),
    current_user: User = Depends(get_current_user),
):

    await article_service.delete(article_id=article_id, current_user=current_user)
    return {"detail": f"Article with id {article_id} deleted"}


@router.post("/search", status_code=status.HTTP_200_OK)
async def search_articles_handler(
    search_params: ArticleSearch,
    article_service: ArticleService = Depends(),
    current_user: User | None = Depends(get_current_user),
) -> list[ArticleResponse]:

    articles = await article_service.search(search_params)

    return articles
