from .article_repository import ArticleRepository, SearchParams, UpdateParams
from ..like.like_repository import LikeRepository


class ArticleService:
    def __init__(self):
        self.article_repository = ArticleRepository()
        self.like_repository = LikeRepository()

    # 메소드 이름 앞의 언더스코어(_)는 이 메소드가 클래스/모듈 내부에서만 사용되는 private 메소드임
    def _get_category_ids(self, categories):
        """카테고리 객체 리스트에서 카테고리 ID 리스트를 추출하는 헬퍼 메소드"""
        return [cat.category_id for cat in categories] if categories else []

    async def find_many(self, user_id: int, skip: int, limit: int):
        articles = await self.article_repository.find_many(
            user_id=user_id, skip=skip, limit=limit
        )

        # 각 article의 응답 형식 변환
        return [
            {
                **article.model_dump(),
                "categories": self._get_category_ids(article.categories),
                "likes_count": await self.like_repository.count(article_id=article.id),
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
        categories = self._get_category_ids(updated_article.categories)
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

        categories = self._get_category_ids(new_article.categories)

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
        categories = self._get_category_ids(updated_article.categories)
        likes_count = await self.like_repository.count(article_id=updated_article.id)
        article_dict = {
            **updated_article.model_dump(),
            "categories": categories,
            "likes_count": likes_count,
        }

        return article_dict

    async def search(self, request: SearchParams):
        articles = await self.article_repository.search(params=request)

        return [
            {
                **article.model_dump(),
                "categories": self._get_category_ids(article.categories),
                "likes_count": await self.like_repository.count(article_id=article.id),
            }
            for article in articles
        ]
