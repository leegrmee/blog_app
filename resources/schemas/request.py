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


# TOKEN-------------
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None
    user_id: Optional[int] = None
    role: Optional[str] = None


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
