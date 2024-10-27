from typing import Optional
from resources.schemas.response import UserResponse, SignUpResponse, User
from config.Connection import prisma_connection
import logging


class UserRepository:
    def __init__(self):
        self.prisma = prisma_connection.prisma

    async def get_users(self) -> list[User]:
        users = await self.prisma.user.find_many()
        return [User.model_validate(user) for user in users]

    async def get_user_by_id(self, id: int) -> Optional[User]:
        user = await self.prisma.user.find_unique(where={"id": id})
        return User.model_validate(user) if user else None

    async def get_user_by_email(self, user_email: str) -> Optional[User]:
        try:
            logging.info(f"Attempting to find user with email: {user_email}")

            user = await self.prisma.user.find_unique(where={"email": user_email})
            logging.info(
                f"Database query result: {user}"
            )  # 데이터베이스 조회 결과 로깅

            if user is None:
                logging.warning(f"No user found with email: {user_email}")
                return None

            return User.model_validate(user)

        except Exception as e:
            logging.error(f"Error in get_user_by_email: {str(e)}")
            raise

    async def create_user(
        self, username: str, email: str, hashed_password: str
    ) -> SignUpResponse:
        new_user = await self.prisma.user.create(
            data={
                "username": username,
                "email": email,
                "hashed_password": hashed_password,
            }
        )
        return SignUpResponse.model_validate(new_user)

    async def update_password(self, email: str, hashed_password: str) -> UserResponse:
        updated_user = await self.prisma.user.update(
            where={"email": email}, data={"hashed_password": hashed_password}
        )
        return UserResponse.model_validate(updated_user)
