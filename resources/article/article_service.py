from prisma import Prisma
from fastapi import HTTPException
from typing import List, Optional
from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str
    email: str
    password: str


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None


class UserService:
    def __init__(self):
        self.prisma = Prisma()

    async def create_user(self, user: UserCreate) -> dict:
        await self.prisma.connect()
        try:
            new_user = await self.prisma.user.create({"data": user.dict()})
            return new_user
        finally:
            await self.prisma.disconnect()

    async def get_users(self) -> List[dict]:
        await self.prisma.connect()
        try:
            users = await self.prisma.user.find_many()
            return users
        finally:
            await self.prisma.disconnect()

    async def get_user(self, user_id: int) -> dict:
        await self.prisma.connect()
        try:
            user = await self.prisma.user.find_unique(where={"id": user_id})
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            return user
        finally:
            await self.prisma.disconnect()

    async def update_user(self, user_id: int, user: UserUpdate) -> dict:
        await self.prisma.connect()
        try:
            updated_user = await self.prisma.user.update(
                where={"id": user_id}, data=user.dict(exclude_unset=True)
            )
            if not updated_user:
                raise HTTPException(status_code=404, detail="User not found")
            return updated_user
        finally:
            await self.prisma.disconnect()

    async def delete_user(self, user_id: int) -> dict:
        await self.prisma.connect()
        try:
            deleted_user = await self.prisma.user.delete(where={"id": user_id})
            if not deleted_user:
                raise HTTPException(status_code=404, detail="User not found")
            return deleted_user
        finally:
            await self.prisma.disconnect()
