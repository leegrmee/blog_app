from typing import Optional
from resources.schemas.response import UserResponse, SignUpResponse, User
from config.Connection import prisma_connection


class UserRepository:
    def __init__(self):
        self.prisma = prisma_connection.prisma

    async def get_users(self) -> list[User]:
        users = await self.prisma.user.find_many()
        return [Usere.model_validate(user) for user in users]

    async def get_user_by_id(self, id: int) -> Optional[User]:
        user = await self.prisma.user.find_unique(where={"id": id})
        return User.model_validate(user) if user else None

    async def get_user_by_email(self, user_email: str) -> Optional[User]:
        user = await self.prisma.user.find_unique(where={"email": user_email})
        return User.model_validate(user) if user else None

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
