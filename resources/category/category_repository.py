from prisma import Prisma
from typing import List


class CategoryRepository:
    def __init__(self):
        self.prisma = Prisma()

    # 모든 카테고리 조회
    async def get_all_categories(self):
        async with Prisma() as db:
            return await db.category.find_many()

    # 특정 ID의 카테고리 조회
    async def get_category_by_id(self, category_id: int):
        async with Prisma() as db:
            return await db.category.find_unique(where={"id": category_id})

    # 특정 게시글의 카테고리 조회
    async def get_categories_of_article(self, article_id: int):
        async with Prisma() as db:
            return await db.categorytoarticle.find_many(
                where={"articleId": article_id}, include={"category": True}
            )

    # 게시글의 카테고리 업데이트
    async def update_article_categories(self, article_id: int, category_ids: List[int]):
        async with Prisma() as db:
            # 기존 카테고리 연결 삭제
            await db.categorytoarticle.delete_many(where={"articleId": article_id})

            # 새로운 카테고리 연결 생성
            new_connections = [
                {"articleId": article_id, "categoryId": cat_id}
                for cat_id in category_ids
            ]
            await db.categorytoarticle.create_many(data=new_connections)

    # 카테고리 별 게시물
    async def get_articles_by_category(self, category_id: int):
        async with Prisma() as db:
            return await db.article.find_many(
                where={"categories": {"some": {"categoryId": category_id}}},
                include={"user": True},
            )

    async def get_user_categories_with_articles(self, user_id: int):
        async with Prisma() as db:
            categories = await db.category.find_many(
                where={"articles": {"some": {"article": {"userId": user_id}}}},
                include={
                    "articles": {
                        "include": {"article": True},
                        "where": {"article": {"userId": user_id}},
                    }
                },
            )
            return categories
