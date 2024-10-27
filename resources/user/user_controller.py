from fastapi import APIRouter, status, Depends, HTTPException
from typing import Optional

from resources.user.user_service import UserService

from resources.schemas.request import UserSignupRequest

from resources.schemas.response import User, SignUpResponse


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[User] | None)
async def get_users_handler(user_service: UserService = Depends()) -> list[User] | None:
    return await user_service.get_users()


@router.get("/{user_id}", status_code=status.HTTP_200_OK, response_model=User | None)
async def get_user_by_id_handler(
    user_id: int, user_service: UserService = Depends()
) -> User | None:
    user: User | None = await user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return user


# 회원가입
@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def user_signup_handler(
    request: UserSignupRequest,
    user_service: UserService = Depends(),
) -> SignUpResponse:
    return await user_service.signup_user(request)
