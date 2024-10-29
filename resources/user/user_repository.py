from typing import Optional
from resources.schemas.response import User
from config.Connection import prisma_connection


class UserRepository:
    def __init__(self):
        self.prisma = prisma_connection.prisma

    async def find_many(self):
        return await self.prisma.user.find_many(
            include={"articles": True, "comments": True, "likes": True}
        )

    async def find_one_by_id(self, id: int):
        return await self.prisma.user.find_unique(
            where={"id": id},
            include={"articles": True, "comments": True, "likes": True},
        )

    async def find_one_by_email(self, user_email: str):
        return await self.prisma.user.find_unique(
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
                "hashedpassword": hashed_password,
            }
        )

    async def update_password(self, email: str, hashed_password: str):
        return await self.prisma.user.update(
            where={"email": email}, data={"hashedpassword": hashed_password}
        )
