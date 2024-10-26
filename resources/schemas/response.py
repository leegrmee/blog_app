from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: str
    hashed_password: str

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
    user_id: Optional[int] = None


class ArticleResponse(BaseModel):
    id: int
    user_id: str
    title: str
    content: str
    views: int
    created_date: datetime
    updated_date: datetime

    model_config = ConfigDict(from_attributes=True)


class CommentResponse(BaseModel):
    id: int
    user_id: int
    article_id: int
    content: str
    created_date: datetime
    updated_date: datetime

    model_config = ConfigDict(from_attributes=True)


class CategoryResponse(BaseModel):
    id: int
    name: str
    articles: list[ArticleResponse]

    model_config = ConfigDict(from_attributes=True)


class LikeResponse(BaseModel):
    user_id: int
    article_id: int

    model_config = ConfigDict(from_attributes=True)
