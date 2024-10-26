from typing import Optional
from resources.schemas.response import UserResponse, SignUpResponse
from config.Connection import prisma_connection


class UserRepository:
    def __init__(self):
        self.prisma = prisma_connection.prisma.prisma

    async def get_users(self) -> list[UserResponse]:
        users = await self.prisma.user.find_many()
        return [UserResponse.model_validate(user) for user in users]

    async def get_user_by_id(self, user_id: int) -> Optional[UserResponse]:
        user = await self.prisma.user.find_unique(where={"id": user_id})
        return UserResponse.model_validate(user) if user else None

    async def get_user_by_email(self, user_email: str) -> Optional[UserResponse]:
        user = await self.prisma.user.find_unique(where={"email": user_email})
        return UserResponse.model_validate(user) if user else None

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

    async def update_password(
        self, user_email: str, new_hashed_password: str
    ) -> UserResponse:
        updated_user = await self.prisma.user.update(
            where={"email": user_email}, data={"hashed_password": new_hashed_password}
        )
        return UserResponse.model_validate(updated_user)
