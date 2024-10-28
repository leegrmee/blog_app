from datetime import datetime
from config.Connection import prisma_connection
from typing import Optional


class ArticleRepository:
    def __init__(self):
        self.prisma = prisma_connection.prisma

    def find_many(self, user_id: int, skip: int, limit: int):
        return self.prisma.article.find_many(
            where={"userId": user_id},
            skip=skip,
            take=limit,
            order={"createdAt": "desc"},
            include={"user": True},
        )

    def find_by_id(self, article_id: int):
        article = self.prisma.article.find_unique(
            where={"id": article_id},
            include={"user": True, "categories": {"include": {"category": True}}},
        )
        if not article:
            return None

        categories = (
            [cat.category.id for cat in article.categories]
            if article.categories
            else []
        )
        article_dict = {**article.model_dump(), "categories": categories}
        return article_dict

    def increment_view_count(self, article_id: int):
        return self.prisma.article.update(
            where={"id": article_id},
            data={"views": {"increment": 1}},
            include={"user": True},
        )

    class SearchParams:
        def __init__(
            self,
            category_id: Optional[int] = None,
            user_id: Optional[int] = None,
            created_at: Optional[datetime] = None,
            updated_at: Optional[datetime] = None,
            skip: int = 0,
            limit: int = 10,
        ):
            self.category_id = category_id
            self.user_id = user_id
            self.created_at = created_at
            self.updated_at = updated_at
            self.skip = skip
            self.limit = limit

    def search(self, params: SearchParams):
        filters = {}
        if params.category_id is not None:
            filters["categories"] = {"some": {"categoryId": params.category_id}}
        if params.user_id is not None:
            filters["userId"] = params.user_id
        if params.created_at is not None:
            filters["createdAt"] = params.created_at
        if params.updated_at:
            filters["updatedAt"] = params.updated_at

        return self.prisma.article.find_many(
            where=filters,
            skip=params.skip,
            take=params.limit,
            include={"user": True, "categories": True},
        )

    def create(self, user_id: int, title: str, content: str):
        return self.prisma.article.create(
            data={
                "user": {"connect": {"id": user_id}},
                "title": title,
                "content": content,
            }
        )

    def delete(self, article_id: int):
        article = self.prisma.article.find_unique(where={"id": article_id})
        if not article:
            return None
        return self.prisma.article.delete(where={"id": article_id})

    class UpdateParams:
        def __init__(
            self,
            article_id: int,
            title: Optional[str] = None,
            content: Optional[str] = None,
            categories: Optional[list[int]] = None,
        ):
            self.article_id = article_id
            self.title = title
            self.content = content
            self.categories = categories

    def update(self, params: UpdateParams):
        article = self.prisma.article.find_unique(where={"id": params.article_id})
        if not article:
            return None

        update_data = {}
        if params.title is not None:
            update_data["title"] = params.title
        if params.content is not None:
            update_data["content"] = params.content
        if params.categories is not None:
            update_data["categories"] = {
                "deleteMany": {},
                "create": [
                    {"category": {"connect": {"id": cat_id}}}
                    for cat_id in params.categories
                ],
            }

        updated_article = self.prisma.article.update(
            where={"id": article.id},
            data=update_data,
            include={"user": True, "categories": {"include": {"category": True}}},
        )

        categories = (
            [cat.category.id for cat in updated_article.categories]
            if updated_article.categories
            else []
        )
        article_dict = {**updated_article.model_dump(), "categories": categories}
        return article_dict
