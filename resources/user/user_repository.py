from typing import Optional
from resources.schemas.response import User
from config.Connection import prisma_connection


class UserRepository:
    def __init__(self):
        self.prisma = prisma_connection.prisma

    def find_many(self) -> list[User]:
        return self.prisma.user.find_many(
            include={"articles": True, "comments": True, "likes": True}
        )

    def find_one_by_id(self, id: int) -> Optional[User]:
        return self.prisma.user.find_unique(
            where={"id": id},
            include={"articles": True, "comments": True, "likes": True},
        )

    def find_one_by_email(self, user_email: str) -> Optional[User]:
        return self.prisma.user.find_unique(
            where={"email": user_email},
            include={"articles": True, "comments": True, "likes": True},
        )

    async def create(self, username: str, email: str, hashed_password: str):
        prevUser = await self.find_one_by_email(email)
        if prevUser:
            raise Exception("Email already exists")
        return await self.prisma.user.create(
            data={
                "username": username,
                "email": email,
                "hashed_password": hashed_password,
            }
        )

    def update_password(self, email: str, hashed_password: str):
        return self.prisma.user.update(
            where={"email": email}, data={"hashed_password": hashed_password}
        )
