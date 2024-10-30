from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime


class User(BaseModel):
    id: int
    username: str
    email: str
    role: str
    hashedpassword: str = Field(..., alias="hashedPassword")
    created_at: datetime = Field(..., alias="createdAt")
    updated_at: datetime = Field(..., alias="updatedAt")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class UserResponse(BaseModel):
    email: str
    role: str

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class SignUpResponse(BaseModel):
    id: int
    username: str
    email: str

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


# token return
class JWTResponse(BaseModel):
    access_token: str


# TOKEN-------------
class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_email: str
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class LikeResponse(BaseModel):
    user_id: int = Field(..., alias="userId")
    article_id: int = Field(..., alias="articleId")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class ArticleResponse(BaseModel):
    id: int
    user_id: int
    title: str | None = None
    content: str | None = None
    views: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    categories: list[int] | None = Field(default_factory=list)
    likes_count: int = 0

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class CommentResponse(BaseModel):
    id: int
    user_id: int
    article_id: int
    content: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class CategoryResponse(BaseModel):
    id: int
    name: str
    articles: list[ArticleResponse] | None = []

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class CategoryToArticleResponse(BaseModel):
    article_id: int = Field(..., alias="articleId")
    category_id: int = Field(..., alias="categoryId")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
