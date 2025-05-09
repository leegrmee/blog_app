from enum import Enum
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import List


class UserRole(str, Enum):
    USER = "user"
    AUTHOR = "author"
    MODERATOR = "moderator"
    ADMIN = "admin"


class FileType(str, Enum):
    IMAGE = "image"
    DOCUMENT = "document"
    OTHER = "other"


class FileResponse(BaseModel):
    id: int
    filename: str
    mimetype: str
    size: int
    type: FileType
    url: str


# 역할의 계층 정의 (숫자가 클수록 높은 권한)
ROLE_HIERARCHY = {
    UserRole.USER: 1,
    UserRole.AUTHOR: 2,
    UserRole.MODERATOR: 3,
    UserRole.ADMIN: 4,
}


class User(BaseModel):
    id: int
    username: str
    email: str
    role: UserRole
    hashedpassword: str = Field(..., alias="hashedPassword")
    created_at: datetime = Field(..., alias="createdAt")
    updated_at: datetime = Field(..., alias="updatedAt")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class UserResponse(BaseModel):
    email: str
    role: UserRole

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


class FileUploadResponse(BaseModel):
    urls: list[str]

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
    files: List[FileResponse] | None = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class CommentResponse(BaseModel):
    id: int
    user_id: int
    article_id: int
    content: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class CommentUpdateResponse(BaseModel):
    id: int
    content: str
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class ArticleToCategory(BaseModel):
    id: int
    user_id: int
    title: str | None = None
    content: str | None = None
    views: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    likes_count: int = 0

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class CategoryInfo(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class CategoryResponse(BaseModel):
    id: int
    name: str
    articles: list[ArticleToCategory] | None = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class CategoriesResponse(BaseModel):
    categories: list[CategoryResponse]

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class CategoryToArticleResponse(BaseModel):
    article: ArticleToCategory
    categories: list[CategoryInfo]

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class UserCatArticleResponse(BaseModel):
    user_id: int
    categories_with_articles: CategoriesResponse

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
