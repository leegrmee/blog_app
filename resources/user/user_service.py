from datetime import datetime, timedelta
import bcrypt
from jose import jwt
from typing import List, Optional

from resources.schemas.request import UserSignupRequest
from resources.schemas.response import UserSchema, SignUpSchema
from resources.user.user_repository import UserRepository


class UserService:
    def __init__(self):
        self.user_repository = UserRepository()
        self.encoding: str = "UTF-8"
        self.secretkey: str = (
            "fca1c9a668eb97796fc628eac4ba85a50538279ee2f3a2816ebf3e67a0e6a026"
        )
        self.jwt_algorithm: str = "HS256"

    async def get_users(self) -> List[UserSchema]:
        return await self.user_repository.get_users()

    async def get_user_by_id(self, user_id: int) -> Optional[UserSchema]:
        return await self.user_repository.get_user_by_id(user_id)

    async def get_user_by_email(self, user_email: str) -> Optional[UserSchema]:
        return await self.user_repository.get_user_by_email(user_email)

    def hash_password(self, plain_password: str) -> str:
        hashed_password: bytes = bcrypt.hashpw(
            plain_password.encode(self.encoding),
            salt=bcrypt.gensalt(),
        )
        return hashed_password.decode(self.encoding)

    async def signup_user(self, request: UserSignupRequest) -> SignUpSchema:
        hashed_password = self.hash_password(request.password)
        return await self.user_repository.create_user(
            request.username, request.email, hashed_password
        )

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(
            plain_password.encode(self.encoding),
            hashed_password.encode(self.encoding),
        )

    def create_jwt(self, username: str) -> str:

        return jwt.encode(
            {
                "sub": username,  # 원래 유니크한 식별자를 받아야함
                "exp": datetime.now()
                + timedelta(days=1),  # 요청 현재 시각 에서+ 하루 유효
            },
            self.secretkey,
            algorithm=self.jwt_algorithm,
        )

    async def verify_credentials(
        self, user_id: int, email: str, current_password: str
    ) -> bool:
        user = await self.get_user_by_id(user_id)
        if not user or user.email != email:
            return False
        if not self.verify_password(current_password, user.hashed_password):
            return False

        return True

    async def update_password(self, user_id: int, new_password: str):

        new_hashed_password = self.hash_password(new_password)

        return await self.user_repository.update_password(user_id, new_hashed_password)
