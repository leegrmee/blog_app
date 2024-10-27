from pydantic import BaseModel, ConfigDict
from datetime import datetime


class User(BaseModel):
    id: int
    username: str
    email: str
    role: str
    hashed_password: str

    model_config = ConfigDict(from_attributes=True)


class UserResponse(BaseModel):
    email: str
    role: str

    model_config = ConfigDict(from_attributes=True)


class SignUpResponse(BaseModel):
    id: int
    username: str
    email: str

    model_config = ConfigDict(from_attributes=True)


# token return
class JWTResponse(BaseModel):
    access_token: str


# TOKEN-------------
class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_email: str | None


class ArticleResponse(BaseModel):
    id: int
    userId: int
    title: str
    content: str
    views: int
    createdAt: datetime
    updatedAt: datetime

    model_config = ConfigDict(from_attributes=True)


class CommentResponse(BaseModel):
    id: int
    userId: int
    articleId: int
    content: str
    createdAt: datetime
    updatedAt: datetime

    model_config = ConfigDict(from_attributes=True)


class CategoryResponse(BaseModel):
    id: int
    name: str
    articles: list[ArticleResponse]

    model_config = ConfigDict(from_attributes=True)


class LikeResponse(BaseModel):
    userId: int
    articleId: int

    model_config = ConfigDict(from_attributes=True)
