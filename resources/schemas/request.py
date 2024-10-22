from pydantic import BaseModel


# USER--------------


class UserSignupRequest(BaseModel):
    id: int
    username: str
    password: str
    email: str


class UserLoginRequest(BaseModel):
    email: str
    password: str


class PasswordUpdateRequest(BaseModel):
    email: str
    current_password: str
    new_password: str


# ARTICLE--------------


class ArticleCreate(BaseModel):
    title: str
    content: str
    user_id: int


class ArticleUpdate(BaseModel):
    title: str
    content: str


# COMMENT--------------


class CommentCreate(BaseModel):
    content: str
    article_id: int
    user_id: int


# LIKE--------------


class LikeCreate(BaseModel):
    user_id: int
    content_id: int
