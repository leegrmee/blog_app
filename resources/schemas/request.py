from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime


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
    title: Optional[str] = None
    content: Optional[str] = None
    categories: Optional[list[int]] = None

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        json_schema_extra={
            "example": {
                "title": "Updated Title",
                "content": "Updated Content",
                "categories": [1, 2, 3],
            }
        },
    )


class ArticleSearch(BaseModel):
    category_id: Optional[int] = None
    user_id: Optional[int] = None
    created_date: Optional[datetime] = None
    updated_date: Optional[datetime] = None
    skip: int = 0
    limit: int = 10


# COMMENT--------------
class CommentCreate(BaseModel):
    content: str


class CommentUpdate(BaseModel):
    content: str


# LIKE--------------
class LikeCreate(BaseModel):
    article_id: int
    dir: int = Field(ge=0, le=1)
