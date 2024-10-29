from .category_repository import CategoryRepository


class CategoryService:
    def __init__(self):
        self.category_repository = CategoryRepository()

    async def find_all(self):
        """모든 카테고리 조회"""
        categories = await self.category_repository.find_all()

        result = [
            {
                "id": cat.id,
                "name": cat.name,
                "articles": [cat_to_article.article for cat_to_article in cat.articles],
            }
            for cat in categories
        ]
        return result

    async def find_by_id(self, category_id: int) -> dict | None:
        """특정 카테고리 조회"""
        categories = await self.category_repository.find_by_id(id=category_id)
        if categories:
            return {
                "id": categories.id,
                "name": categories.name,
                "articles": [
                    cat_to_article.article for cat_to_article in categories.articles
                ],
            }
        return None

    async def find_by_article_id(self, article_id: int):
        """특정 게시글의 카테고리 조회"""
        categories = await self.category_repository.find_by_article_id(
            article_id=article_id
        )

        result = [
            {
                "article_id": article_id,
                "categories": [
                    {
                        "id": category.id,
                        "name": category.name,
                    }
                    for category in categories
                ],
            }
        ]

        return result

    async def find_articles_by_category(self, category_id: int):
        """특정 카테고리의 게시글 조회"""
        articles = await self.category_repository.find_articles_by_category(category_id)
        result = [
            {
                "category_id": category_id,
                "articles": [
                    {
                        "id": article.id,
                        "title": article.title,
                        "content": article.content,
                        "views": article.views,
                        "created_at": article.created_at,
                        "updated_at": article.updated_at,
                        "user_id": article.user_id,
                    }
                    for article in articles
                ],
            }
        ]

        return result

    async def find_by_user_id(self, user_id: int):
        """사용자가 선택한 카테고리 및 카테고리별 작성한 게시글 조회"""
        categories = await self.category_repository.find_by_user_id(user_id=user_id)

        result = [
            {
                "id": category.id,
                "name": category.name,
                "articles": [
                    cat_to_article.article for cat_to_article in category.articles
                ],
            }
            for category in categories
        ]
        return result

    async def delete(self, article_id: int, category_id: int):
        """게시글에서 특정 카테고리 제거"""
        await self.category_repository.delete(
            article_id=article_id, category_id=category_id
        )
        # 업데이트된 카테고리 목록을 반환
        return await self.find_by_article_id(article_id)
