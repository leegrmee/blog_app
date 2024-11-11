from resources.schemas.response import UserRole
from config.Connection import prisma_connection


class UserRepository:
    def __init__(self):
        self.prisma = prisma_connection.prisma

    async def find_many(self):
        return await self.prisma.user.find_many(order={"id": "asc"})

    async def find_one_by_id(self, id: int):
        return await self.prisma.user.find_unique(
            where={"id": id},
            include={"articles": True, "comments": True, "likes": True},
        )

    async def find_one_by_email(self, user_email: str):
        return await self.prisma.user.find_unique(where={"email": user_email})

    async def find_by_role(self, role: UserRole):
        return await self.prisma.user.find_many(where={"role": role.value})

    async def create(
        self, username: str, email: str, hashed_password: str, role: UserRole
    ):
        prev_user = await self.find_one_by_email(email)
        if prev_user:
            raise Exception("Email already exists")
        return await self.prisma.user.create(
            data={
                "username": username,
                "email": email,
                "hashedpassword": hashed_password,
                "role": role.value,  # Enum 값을 문자열로 저장
            }
        )

    async def update_password(self, email: str, hashed_password: str):
        return await self.prisma.user.update(
            where={"email": email}, data={"hashedpassword": hashed_password}
        )

    async def update_role(self, user_id: int, new_role: UserRole):
        return await self.prisma.user.update(
            where={"id": user_id},
            data={"role": new_role.value},
        )
