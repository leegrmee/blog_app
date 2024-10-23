from pydantic import BaseModel, ConfigDict
from typing import List, Optional


class UserSchema(BaseModel):
    id: int
    username: str
    email: str
    role: str
    hashed_password: str

    model_config = ConfigDict(from_attributes=True)


class SignUpSchema(BaseModel):
    id: int
    username: str
    email: str

    model_config = ConfigDict(from_attributes=True)


# token return
class JWTResponse(BaseModel):
    access_token: str


class ArticleSchema(BaseModel):
    id: int
    username: str
    title: str
    content: str

    model_config = ConfigDict(from_attributes=True)


class AritcleListSchema(BaseModel):
    articles: List[ArticleSchema]

    model_config = ConfigDict(from_attributes=True)


class LikeResponse(BaseModel):
    content_id: int

    model_config = ConfigDict(from_attributes=True)


# TOKEN-------------
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None
    user_id: Optional[int] = None
    role: Optional[str] = None
