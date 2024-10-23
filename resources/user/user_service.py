from datetime import datetime, timedelta, timezone
from typing import List, Optional, Dict, Any
from jose import jwt, JWTError
from passlib.context import CryptContext


from resources.schemas.request import UserSignupRequest
from resources.schemas.response import UserSchema, SignUpSchema, TokenData
from resources.user.user_repository import UserRepository


class UserService:
    def __init__(self):
        self.user_repository = UserRepository()
        self.encoding: str = "UTF-8"
        self.secretkey: str = (
            "fca1c9a668eb97796fc628eac4ba85a50538279ee2f3a2816ebf3e67a0e6a026"
        )
        self.jwt_algorithm: str = "HS256"
        self.token_expire_minutes = 30
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    async def get_users(self) -> List[UserSchema]:
        return await self.user_repository.get_users()

    async def get_user_by_id(self, user_id: int) -> Optional[UserSchema]:
        return await self.user_repository.get_user_by_id(user_id)

    async def get_user_by_email(self, user_email: str) -> Optional[UserSchema]:
        return await self.user_repository.get_user_by_email(user_email)

    def hash_password(self, plain_password: str) -> str:
        # hashed_password: bytes = bcrypt.hashpw(
        #     plain_password.encode(self.encoding),
        #     salt=bcrypt.gensalt(),
        # )
        hashed_password = self.pwd_context.hash(plain_password)
        return hashed_password.decode(self.encoding)

    async def signup_user(self, request: UserSignupRequest) -> SignUpSchema:
        hashed_password = self.hash_password(request.password)
        return await self.user_repository.create_user(
            request.username, request.email, hashed_password
        )

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(
            plain_password.encode(self.encoding),
            hashed_password.encode(self.encoding),
        )

    def create_access_token(self, data: Dict[str, Any]) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=self.token_expire_minutes
        )
        to_encode.update({"exp": expire, "iat": datetime.now(timezone.utc)})
        # iat = issued at

        jwt_token: str = jwt.encode(
            to_encode,
            self.secretkey,
            algorithm=self.jwt_algorithm,
        )

        return jwt_token

    async def verify_access_token(self, token: str, credentials_exception) -> int:

        try:
            payload = jwt.decode(token, self.secretkey, algorithms=[self.jwt_algorithm])
            user_id: int = payload.get("user_id")
            if user_id is None:
                raise credentials_exception

            token_data = TokenData(user_id=user_id)

        except JWTError:
            raise credentials_exception

        return token_data

    async def update_password(self, user_email: int, new_password: str) -> UserSchema:

        new_hashed_password: str = self.hash_password(new_password)
        updated_password: UserSchema = await self.user_repository.update_password(
            user_email, new_hashed_password
        )

        return updated_password
