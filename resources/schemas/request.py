from datetime import date, datetime

from pydantic import BaseModel, Field
from resources.comment.comment_repository import CommentData, UpdateCommentData
from resources.article.article_repository import UpdateParams
from resources.schemas.response import UserRole

# 필드를 완전히 선택적으로 만들려면 기본값(= None)을 지정해야 합니다.!!!!


# USER--------------
class UserSignupRequest(BaseModel):
    username: str
    email: str
    password: str  # 해시 전


class UserLoginRequest(BaseModel):
    email: str
    password: str  # 해시 전


class UpdateUserRoleRequest(BaseModel):
    role: UserRole


class PasswordUpdateRequest(BaseModel):
    email: str
    password: str  # 해시 전
    new_password: str  # 해시 전


# ARTICLE--------------
class ArticleCreate(BaseModel):
    title: str
    content: str
    select_categories: list[int]

    class Config:
        schema_extra = {
            "example": {
                "title": "Sample Article",
                "content": "This is a sample article.",
                "select_categories": [1, 2, 3],
            }
        }

    # 파일은 폼데이터로 받고, 나머지는 제이손이기 때문에 충돌 방지를 위해 위와 같이 수정


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
    created_date: date | None = None
    updated_date: date | None = None
    skip: int = Field(default=0, ge=0)
    limit: int = Field(default=10, ge=1, le=100)


# COMMENT--------------
class CommentCreate(BaseModel):
    content: str

    def to_comment_data(self, user_id: int, article_id: int) -> CommentData:
        return CommentData(user_id=user_id, article_id=article_id, content=self.content)


class CommentUpdate(BaseModel):
    id: int
    new_content: str

    def to_comment_data(self, user_id: int) -> UpdateCommentData:
        return UpdateCommentData(
            user_id=user_id, id=self.id, new_content=self.new_content
        )


# LIKE--------------
class LikeCreate(BaseModel):
    article_id: int
    dir: int = Field(ge=0, le=1)
