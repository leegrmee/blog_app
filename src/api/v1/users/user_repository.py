from src.schemas.response import UserRole
from src.core.database.base_repo import BaseRepository
from typing import Optional, Dict, Any, List


class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__("user")

    async def find_many(self, order: Optional[Dict[str, str]] = None) -> List[Any]:
        """
        모든 사용자를 조회합니다.
        """
        return await super().find_many(order=order or {"id": "asc"})

    async def find_one_by_id(self, id: int):
        """
        ID로 사용자를 조회합니다.
        """
        return await super().find_unique(
            where={"id": id},
            include={"articles": True, "comments": True, "likes": True},
        )

    async def find_one_by_email(self, user_email: str):
        """
        이메일로 사용자를 조회합니다.
        """
        return await super().find_unique(where={"email": user_email})

    async def find_by_role(self, role: UserRole):
        """
        역할로 사용자를 조회합니다.
        """
        return await super().find_many(where={"role": role.value})

    async def create(
        self, username: str, email: str, hashed_password: str, role: UserRole
    ):
        """
        새 사용자를 생성합니다.
        """
        prev_user = await self.find_one_by_email(email)
        if prev_user:
            raise Exception("Email already exists")

        return await super().create(
            data={
                "username": username,
                "email": email,
                "hashedpassword": hashed_password,
                "role": role.value,  # Enum 값을 문자열로 저장
            }
        )

    async def update_password(self, email: str, hashed_password: str):
        """
        사용자 비밀번호를 업데이트합니다.
        """
        return await super().update(
            where={"email": email}, data={"hashedpassword": hashed_password}
        )

    async def update_role(self, user_id: int, new_role: UserRole):
        """
        사용자 역할을 업데이트합니다.
        """
        return await super().update(
            where={"id": user_id},
            data={"role": new_role.value},
        )
