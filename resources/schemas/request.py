from pydantic import BaseModel, Field
from datetime import datetime
from resources.comment.comment_repository import CommentData
from resources.article.article_repository import UpdateParams


# 필드를 완전히 선택적으로 만들려면 기본값(= None)을 지정해야 합니다.!!!!


# USER--------------
class UserSignupRequest(BaseModel):
    username: str
    email: str
    password: str  # 해시 전


class UserLoginRequest(BaseModel):
    email: str
    password: str  # 해시 전


class PasswordUpdateRequest(BaseModel):
    email: str
    password: str  # 해시 전
    new_password: str  # 해시 전


# ARTICLE--------------
class ArticleCreate(BaseModel):
    title: str
    content: str
    select_categories: list[int]


class ArticleUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    categories: list[int] | None = None

    def to_update_data(self, article_id: int, user_id: int) -> UpdateParams:
        return UpdateParams(
            article_id=article_id,
            user_id=user_id,
            title=self.title,
            content=self.content,
            categories=self.categories,
        )


class ArticleSearch(BaseModel):
    user_id: int | None = None
    category_id: int | None = None
    created_date: datetime | None = None
    updated_date: datetime | None = None
    skip: int = 0
    limit: int = 10


# COMMENT--------------
class CommentCreate(BaseModel):
    content: str

    def to_comment_data(self, user_id: int, article_id: int) -> CommentData:
        return CommentData(user_id=user_id, article_id=article_id, content=self.content)


class CommentUpdate(BaseModel):
    id: int
    new_content: str


# LIKE--------------
class LikeCreate(BaseModel):
    article_id: int
    dir: int = Field(ge=0, le=1)
