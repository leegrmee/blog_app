from resources.schemas.request import UserSignupRequest
from resources.schemas.response import UserResponse, SignUpResponse, User
from resources.user.user_repository import UserRepository
from resources.auth.auth_utils import hash_password


class UserService:
    def __init__(self):
        self.user_repository = UserRepository()

    async def get_users(self) -> list[User]:
        return await self.user_repository.get_users()

    async def get_user_by_id(self, user_id: int) -> User | None:
        return await self.user_repository.get_user_by_id(id=user_id)

    async def get_user_by_email(self, user_email: str) -> User | None:
        return await self.user_repository.get_user_by_email(email=user_email)

    async def signup_user(self, request: UserSignupRequest) -> SignUpResponse:
        hashed_password = hash_password(request.password)
        return await self.user_repository.create_user(
            username=request.username,
            email=request.email,
            hashed_password=hashed_password,
        )

    async def update_password(self, email: str, new_password: str) -> UserResponse:
        new_hashed_password: str = hash_password(new_password)
        updated_user: UserResponse = await self.user_repository.update_password(
            email=email, hashed_password=new_hashed_password
        )
        return updated_user
