from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime


class User(BaseModel):
    id: int
    username: str
    email: str
    role: str
    hashed_password: str = Field(..., alias="hashedPassword")
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


class ArticleResponse(BaseModel):
    id: int
    user_id: int = Field(..., alias="userId")
    title: str
    content: str
    categories: list[int] = Field(default_factory=list)
    views: int
    created_at: datetime = Field(..., alias="createdAt")
    updated_at: datetime = Field(..., alias="updatedAt")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class CommentResponse(BaseModel):
    id: int
    user_id: int = Field(..., alias="userId")
    article_id: int = Field(..., alias="articleId")
    content: str
    created_at: datetime = Field(..., alias="createdAt")
    updated_at: datetime = Field(..., alias="updatedAt")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class CategoryResponse(BaseModel):
    id: int
    name: str
    articles: list[ArticleResponse] | None = []

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class LikeResponse(BaseModel):
    user_id: int = Field(..., alias="userId")
    article_id: int = Field(..., alias="articleId")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class CategoryToArticleResponse(BaseModel):
    article_id: int = Field(..., alias="articleId")
    category_id: int = Field(..., alias="categoryId")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
