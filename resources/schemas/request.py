from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# USER--------------
class UserSignupRequest(BaseModel):
    username: str
    password: str  # 해시 전
    email: str


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


class ArticleUpdate(BaseModel):
    title: Optional[str]
    content: Optional[str]


class ArticleSearch(BaseModel):
    category_id: Optional[int] = None
    user_id: Optional[int] = None
    created_date: Optional[datetime] = None
    updated_date: bool = False
    skip: int = 0
    limit: int = 10


# COMMENT--------------
class CommentCreate(BaseModel):
    content: str


class CommentUpdate(BaseModel):
    content: str


# LIKE--------------
class LikeCreate(BaseModel):
    user_id: int
    content_id: int
