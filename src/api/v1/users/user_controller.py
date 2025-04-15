from fastapi import APIRouter, Depends, status, Query

from src.api.v1.users.user_service import UserService
from src.schemas.request import UserSignupRequest, UpdateUserRoleRequest
from src.schemas.response import (
    User,
    SignUpResponse,
    UserResponse,
    UserRole,
)
from src.api.v1.auth.role_dependency import require_minimum_role


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", status_code=status.HTTP_200_OK)
async def get_users_handler(
    user_service: UserService = Depends(),
    authorized_user: User = Depends(require_minimum_role(UserRole.ADMIN)),
) -> list[User] | None:
    return await user_service.find_many()


@router.get("/role", status_code=status.HTTP_200_OK)
async def get_user_by_role_handler(
    role: UserRole = Query(..., description="User role"),
    user_service: UserService = Depends(),
    authorized_user: User = Depends(require_minimum_role(UserRole.ADMIN)),
) -> list[UserResponse]:
    return await user_service.find_by_role(role)


@router.get("/{user_id}", status_code=status.HTTP_200_OK)
async def get_user_by_id_handler(
    user_id: int,
    user_service: UserService = Depends(),
    authorized_user: User = Depends(require_minimum_role(UserRole.ADMIN)),
) -> UserResponse:
    return await user_service.find_one_by_id(user_id)


# 회원가입
@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def user_signup_handler(
    request: UserSignupRequest,
    user_service: UserService = Depends(),
) -> SignUpResponse:
    return await user_service.signup(request)


# 권한 부여
@router.put("/role", status_code=status.HTTP_200_OK)
async def update_user_role_handler(
    user_id: int,
    request: UpdateUserRoleRequest,
    user_service: UserService = Depends(),
    authorized_user: User = Depends(require_minimum_role(UserRole.ADMIN)),
) -> User:
    updated_user = await user_service.update_role(
        user_id=user_id, new_role=request.role
    )
    return updated_user
