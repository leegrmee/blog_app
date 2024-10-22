from pydantic import BaseModel, ConfigDict


class UserSchema(BaseModel):
    id: int
    username: str
    email: str

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
    user_id: int
    content_id: int

    model_config = ConfigDict(from_attributes=True)
