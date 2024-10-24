from typing import List, Optional
from datetime import datetime
from ..schemas.response import ArticleSchema


class ArticleRepository:
    def __init__(self):
        # Prisma 클라이언트 초기화 로직
        pass

    def get_all_articles(
        self, user_id: int, skip: int, limit: int
    ) -> List[ArticleSchema]:
        # 모든 게시물 반환
        # ex)
        # articles = await self.prisma.article.find_many(
        #     where={"user_id": user_id},
        #     skip=skip,
        #     take=limit,
        #     order={"created_at": "desc"}
        # )
        # return [ArticleSchema.from_orm(article) for article in articles]
        return {"articles": []}

    def get_article_by_articleid(self, article_id: int) -> Optional[ArticleSchema]:
        # Prisma 로직 구현 필요
        return None

    def search_articles(
        self,
        category_id: Optional[int] = None,
        user_id: Optional[int] = None,
        created_date: Optional[datetime] = None,
        updated_date: bool = False,
        skip: int = 0,
        limit: int = 10,
    ) -> List[ArticleSchema]:
        # # Prisma를 사용하여 특정 게시물 반환
        # ex:
        # article = await self.prisma.article.find_unique(where={"id": article_id})
        # return ArticleSchema.from_orm(article) if article else None
        return []

    def create_article(self, user_id: int, title: str, content: str) -> ArticleSchema:

        # Prisma를 사용하여 새 게시물 생성
        # ex:
        # new_article = await self.prisma.article.create(
        #     data={
        #         "user_id": user_id,
        #         "title": title,
        #         "content": content
        #     }
        # )
        # return ArticleSchema.from_orm(new_article)

        return {"user_id": user_id, "title": title, "content": content}

    def delete_article(self, article_id: int):

        # Prisma를 사용하여 게시물 수정
        # ex
        # update_data = {}
        # if new_title is not None:
        #     update_data["title"] = new_title
        # if new_content is not None:
        #     update_data["content"] = new_content
        # updated_article = await self.prisma.article.update(
        #     where={"id": article_id},
        #     data=update_data
        # )
        # return ArticleSchema.from_orm(updated_article)
        return 1

    def update_article(
        self, article_id: int, new_title: str, new_content: str
    ) -> ArticleSchema:

        # Prisma를 사용하여 게시물 수정
        # ex:
        # update_data = {}
        # if new_title is not None:
        #     update_data["title"] = new_title
        # if new_content is not None:
        #     update_data["content"] = new_content
        # updated_article = await self.prisma.article.update(
        #     where={"id": article_id},
        #     data=update_data
        # )
        # return ArticleSchema.from_orm(updated_article)
        return ArticleSchema(id=article_id, title=new_title, content=new_content)
