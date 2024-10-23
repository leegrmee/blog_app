from typing import List, Optional
from resources.schemas.response import UserSchema, SignUpSchema


class UserRepository:
    async def get_users(self) -> List[UserSchema]:
        # Mock implementation
        return []

    async def get_user_by_id(self, user_id: int) -> Optional[UserSchema]:
        # Mock implementation
        return UserSchema(
            id=user_id, username=f"user_{user_id}", email=f"user_{user_id}@example.com"
        )

    async def get_user_by_email(self, user_email: str) -> Optional[UserSchema]:
        # Mock implementation
        return UserSchema

    async def create_user(
        self, username: str, email: str, hashed_password: str
    ) -> SignUpSchema:
        # Mock implementation
        return SignUpSchema(id=1, username=username, email=email)

    async def update_password(
        self, user_email: str, new_hashed_password: str
    ) -> UserSchema:
        # Mock implementation
        return UserSchema(email=user_email)
