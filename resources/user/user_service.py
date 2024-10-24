from datetime import datetime, timedelta, timezone
from typing import List, Optional, Dict, Any
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer


from resources.schemas.request import UserSignupRequest
from resources.schemas.response import UserSchema, SignUpSchema, TokenData
from resources.user.user_repository import UserRepository
from resources.auth.auth_utils import hash_password

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


class UserService:
    def __init__(self):
        self.user_repository = UserRepository()

    async def get_users(self) -> List[UserSchema]:
        return await self.user_repository.get_users()

    async def get_user_by_id(self, user_id: int) -> Optional[UserSchema]:
        return await self.user_repository.get_user_by_id(user_id=user_id)

    async def get_user_by_email(self, user_email: str) -> Optional[UserSchema]:
        return await self.user_repository.get_user_by_email(user_email=user_email)

    async def signup_user(self, request: UserSignupRequest) -> SignUpSchema:
        hashed_password = hash_password(request.password)
        return await self.user_repository.create_user(
            username=request.username,
            email=request.email,
            hashed_password=hashed_password,
        )

    async def update_password(self, email: str, new_password: str) -> UserSchema:
        new_hashed_password: str = hash_password(new_password)
        updated_user: UserSchema = await self.user_repository.update_password(
            user_email=email, new_hashed_password=new_hashed_password
        )

        return updated_user
