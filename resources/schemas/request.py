from pydantic import BaseModel
from typing import Optional


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


# COMMENT--------------
class CommentCreate(BaseModel):
    content: str


# LIKE--------------
class LikeCreate(BaseModel):
    user_id: int
    content_id: int
