from .article_repository import ArticleRepository, SearchParams, UpdateParams
from ..like.like_repository import LikeRepository


class ArticleService:
    def __init__(self):
        self.article_repository = ArticleRepository()
        self.like_repository = LikeRepository()

    async def find_many(self, user_id: int, skip: int, limit: int):
        articles = await self.article_repository.find_many(
            user_id=user_id, skip=skip, limit=limit
        )

        # 각 article의 응답 형식 변환
        return [
            {
                **article.model_dump(),
                "categories": (
                    [cat.category_id for cat in article.categories]
                    if article.categories
                    else []
                ),
                "likes_count": len(article.likes) if article.likes else 0,
            }
            for article in articles
        ]

    async def find_by_id(self, article_id: int):
        article = await self.article_repository.find_by_id(article_id=article_id)

        if article is None:
            return None

        # id 로 조회할 때마다 조회수 증가
        updated_article = await self.article_repository.increment_view_count(
            article_id=article_id
        )

        categories = (
            [cat.category_id for cat in updated_article.categories]
            if updated_article.categories
            else []
        )

        likes_count = await self.like_repository.count(article_id=article_id)

        article_dict = {
            **updated_article.model_dump(),
            "categories": categories,
            "likes_count": likes_count,
        }

        return article_dict

    async def create(
        self, user_id: int, title: str, content: str, category_ids: list[int]
    ):
        new_article = await self.article_repository.create(
            user_id=user_id,
            title=title,
            content=content,
            category_ids=category_ids,
        )

        categories = (
            [cat.category.id for cat in new_article.categories]
            if new_article.categories
            else []
        )

        article_dict = {
            **new_article.model_dump(),
            "categories": categories,
            "likes_count": 0,
        }
        return article_dict

    async def delete(self, article_id: int, user_id: int):
        article = await self.article_repository.find_by_id(article_id=article_id)
        if article == None:
            return None
        if article.user_id != user_id:
            return None
        # 게시물 삭제
        deleted_article = await self.article_repository.delete(article_id=article_id)

        if deleted_article == 0:
            return (f"Article with id: {article_id} could not be deleted",)

        return {f"Article of {article_id} deleted"}

    async def update(self, request: UpdateParams):
        article = await self.article_repository.find_by_id(
            article_id=request.article_id
        )
        if article is None:
            return (f"Article with id: {request.article_id} does not exist",)

        if article.user_id != request.user_id:
            return ("Not authorized to perform requested action",)

        updated_article = await self.article_repository.update(params=request)

        # 카테고리 처리
        categories = (
            [cat.category_id for cat in updated_article.categories]
            if updated_article.categories
            else []
        )

        article_dict = {
            **updated_article.model_dump(),
            "categories": categories,
            "likes_count": len(article.likes) if article.likes else 0,
        }

        return article_dict

    async def search(self, request: SearchParams):
        articles = await self.article_repository.search(params=request)
        return [
            {
                **article.model_dump(),
                "categories": (
                    [cat.category_id for cat in article.categories]
                    if article.categories
                    else []
                ),
                "likes_count": len(article.likes) if article.likes else 0,
            }
            for article in articles
        ]
