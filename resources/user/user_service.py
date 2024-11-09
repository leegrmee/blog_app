from fastapi import HTTPException, status
from resources.schemas.request import UserSignupRequest
from resources.schemas.response import UserResponse, User, UserRole
from resources.user.user_repository import UserRepository
from resources.auth.auth_utils import hash_password


class UserService:
    def __init__(self):
        self.user_repository = UserRepository()

    async def find_many(self) -> list[User]:
        return await self.user_repository.find_many()

    async def find_one_by_id(self, user_id: int) -> User | None:
        return await self.user_repository.find_one_by_id(id=user_id)

    async def find_one_by_email(self, user_email: str) -> User | None:

        if not user_email:
            raise ValueError("Email is required")

        user = await self.user_repository.find_one_by_email(user_email=user_email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        return user

    async def find_one_by_role(self, role: UserRole):
        return await self.user_repository.find_one_by_role(role=role)

    async def signup(self, request: UserSignupRequest):
        hashed_password = hash_password(request.password)

        # 새 사용자 가입시 기본 권한 부여
        return await self.user_repository.create(
            username=request.username,
            email=request.email,
            hashed_password=hashed_password,
            role=UserRole.USER,
        )

    async def update_password(self, email: str, new_password: str):
        new_hashed_password: str = hash_password(new_password)
        updated_user: UserResponse = await self.user_repository.update_password(
            email=email, hashed_password=new_hashed_password
        )
        return updated_user

    async def update_role(self, user_id: int, new_role: UserRole):
        return await self.user_repository.update_role(
            user_id=user_id, new_role=new_role
        )
