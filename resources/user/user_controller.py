from fastapi import APIRouter, status, Depends, HTTPException, Body
from typing import List, Optional

from resources.user.user_service import UserService

from resources.schemas.request import (
    UserSignupRequest,
    UserLoginRequest,
    PasswordUpdateRequest,
)
from resources.schemas.response import UserSchema, SignUpSchema, JWTResponse


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[UserSchema])
async def get_users_handler(user_service: UserService = Depends()):
    return await user_service.get_users()


@router.get("/{user_id}", status_code=status.HTTP_200_OK, response_model=UserSchema)
async def get_user_by_id_handler(user_id: int, user_service: UserService = Depends()):
    user: UserSchema = await user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return user


# 회원가입
@router.post(
    "/signup", status_code=status.HTTP_201_CREATED, response_model=SignUpSchema
)
async def user_signup_handler(
    request: UserSignupRequest,
    user_service: UserService = Depends(),
):
    user: SignUpSchema = await user_service.signup_user(request)

    return {"message": "User created successfully", "user_id": user.id}
