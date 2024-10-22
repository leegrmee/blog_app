from fastapi import APIRouter, status, Request, Depends, HTTPException
from typing import List

from resources.user.user_service import UserService

from resources.schemas.request import (
    UserSignupRequest,
    UserLoginRequest,
    PasswordUpdateRequest,
)
from resources.schemas.response import UserSchema, SignUpSchema, JWTResponse


router = APIRouter(prefix="/users")


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
    return await user_service.signup_user(request)


# 로그인
@router.post("/login", status_code=status.HTTP_200_OK)
async def user_login_handler(
    request: UserLoginRequest,
    user_service: UserService = Depends(),
):

    user: UserSchema = await user_service.get_user_by_email(request.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email"
        )

    verified_password: bool = user_service.verify_password(
        plain_password=request.password,
        hashed_password=user.hashed_password,
    )

    if not verified_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password"
        )

    token: str = user_service.create_jwt(username=request.username)

    return JWTResponse(access_token=token)


# 로그아웃
@router.post("/logout", status_code=status.HTTP_200_OK)
async def user_logout_handler(request: Request):

    request.session.pop("username", None)

    return {"message": "Successfully logged out"}


# 유저 정보 수정
@router.put("/update/{user_id}", status_code=status.HTTP_200_OK)
async def password_update_handler(
    request: PasswordUpdateRequest,
    user_id: int,
    user_service: UserService = Depends(),
):
    user = await user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

        # verify email and pw
    if not await user_service.verify_credentials(
        user_id, request.email, request.current_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password"
        )

    updated_user = await user_service.update_password(
        user_id=user_id, new_password=request.new_password
    )

    return {"user": updated_user}
