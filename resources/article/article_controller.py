from fastapi import APIRouter, status, Query, Depends, HTTPException

from resources.schemas.request import ArticleCreate, ArticleUpdate, ArticleSearch
from resources.schemas.response import ArticleResponse, User
from resources.article.article_service import ArticleService
from resources.auth.auth_service import get_current_user

router = APIRouter(prefix="/articles", tags=["Articles"])


@router.get("/", status_code=status.HTTP_200_OK)
async def get_articles_handler(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=30),
    article_service: ArticleService = Depends(),
    current_user: User | None = Depends(get_current_user),
) -> list[ArticleResponse]:
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required"
        )

    articles = await article_service.find_many(
        user_id=current_user.id, skip=skip, limit=limit
    )

    return [
        ArticleResponse(
            id=article.id,
            user_id=article.user_id,
            title=article.title,
            content=article.content,
            views=article.views,
            created_at=article.created_at,
            updated_at=article.updated_at,
            categories=article_service.get_category_ids(article.categories),
            likes_count=await article_service.like_repository.count(
                article_id=article.id
            ),
        )
        for article in articles
    ]


@router.get("/{article_id}", status_code=status.HTTP_200_OK)
async def get_article_handler(
    article_id: int,
    article_service: ArticleService = Depends(),
    current_user: User | None = Depends(get_current_user),
) -> ArticleResponse:
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required"
        )

    article = await article_service.find_by_id(article_id=article_id)
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Article with id {article_id} not found",
        )

    return ArticleResponse(
        id=article.id,
        user_id=article.user_id,
        title=article.title,
        content=article.content,
        views=article.views,
        created_at=article.created_at,
        updated_at=article.updated_at,
        categories=article_service.get_category_ids(article.categories),
        likes_count=await article_service.like_repository.count(article_id=article.id),
    )


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_article_handler(
    article: ArticleCreate,
    article_service: ArticleService = Depends(),
    current_user: User | None = Depends(get_current_user),
) -> ArticleResponse:
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required"
        )

    new_article = await article_service.create(
        user_id=current_user.id,
        title=article.title,
        content=article.content,
        category_ids=article.select_categories,
    )

    return ArticleResponse(
        id=new_article.id,
        user_id=new_article.user_id,
        title=new_article.title,
        content=new_article.content,
        views=new_article.views,
        created_at=new_article.created_at,
        updated_at=new_article.updated_at,
        categories=article_service.get_category_ids(new_article.categories),
        likes_count=0,
    )


@router.put("/{article_id}", status_code=status.HTTP_200_OK)
async def update_article_handler(
    article_id: int,
    update_article: ArticleUpdate,
    article_service: ArticleService = Depends(),
    current_user: User | None = Depends(get_current_user),
) -> ArticleResponse:
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required"
        )

    update_params = update_article.to_update_data(
        article_id=article_id, user_id=current_user.id
    )

    updated_article = await article_service.update(update_params)
    if not updated_article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Article with id {article_id} not found or not authorized",
        )

    return ArticleResponse(
        id=updated_article.id,
        user_id=updated_article.user_id,
        title=updated_article.title,
        content=updated_article.content,
        views=updated_article.views,
        created_at=updated_article.created_at,
        updated_at=updated_article.updated_at,
        categories=article_service.get_category_ids(updated_article.categories),
        likes_count=await article_service.like_repository.count(
            article_id=updated_article.id
        ),
    )


@router.delete("/{article_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_article_handler(
    article_id: int,
    article_service: ArticleService = Depends(),
    current_user: User | None = Depends(get_current_user),
):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required"
        )

    result = await article_service.delete(
        article_id=article_id, user_id=current_user.id
    )
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Article with id {article_id} not found or not authorized",
        )

    return {"detail": f"Article with id {article_id} deleted"}


@router.post("/search", status_code=status.HTTP_200_OK)
async def search_articles_handler(
    search_params: ArticleSearch,
    article_service: ArticleService = Depends(),
    current_user: User | None = Depends(get_current_user),
) -> list[ArticleResponse]:
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required"
        )

    articles = await article_service.search(search_params)

    return [
        ArticleResponse(
            id=article.id,
            user_id=article.user_id,
            title=article.title,
            content=article.content,
            views=article.views,
            created_at=article.created_at,
            updated_at=article.updated_at,
            categories=article_service.get_category_ids(article.categories),
            likes_count=await article_service.like_repository.count(
                article_id=article.id
            ),
        )
        for article in articles
    ]
