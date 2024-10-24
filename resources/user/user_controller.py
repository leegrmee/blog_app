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


# 로그인
@router.post("/login", status_code=status.HTTP_200_OK)
async def user_login_handler(
    request: UserLoginRequest = Body(...),
    user_service: UserService = Depends(),
):

    user: Optional[UserSchema] = await user_service.get_user_by_email(request.email)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials"
        )

    if not user_service.verify_password(request.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials"
        )

    token: str = user_service.create_access_token({"user_id": user.id})

    return JWTResponse(access_token=token)


##검토 필요
# # 로그아웃
# @router.post("/logout", status_code=status.HTTP_200_OK)
# async def user_logout_handler(request: Request):

#     # request.session.pop("username", None)

#     return {"message": "Successfully logged out"}


# 비밀번호 수정
@router.put("/update-password", status_code=status.HTTP_200_OK)
async def password_update_handler(
    request: PasswordUpdateRequest = Body(...),
    user_service: UserService = Depends(),
    current_user: UserSchema = Depends(UserService.logged_in_user),
):
    if current_user.email != request.email:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials"
        )

    if not user_service.verify_password(request.password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials"
        )

    updated_user: UserSchema = await user_service.update_password(
        email=current_user.email, new_password=request.new_password
    )

    return {"message": "Password updated successfully", "user": updated_user}
