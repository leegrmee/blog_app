from fastapi import APIRouter, status, Request, Depends, HTTPException
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
    request: UserLoginRequest,
    user_service: UserService = Depends(),
):

    user: Optional[UserSchema] = await user_service.get_user_by_email(request.email)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials"
        )

    if not user_service.verify_password(request.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials"
        )
        ##검토 필요
    token: str = user_service.create_jwt({"user_email": user.email, "role": user.role})

    return JWTResponse(access_token=token)

    # except ValueError as exc:
    #     # 일반적인 오류 메시지를 사용하여 구체적인 실패 이유를 숨깁니다
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Invalid credentials",
    #         headers={"WWW-Authenticate": "Bearer"},
    #     ) from exc


##검토 필요
# 로그아웃
@router.post("/logout", status_code=status.HTTP_200_OK)
async def user_logout_handler(request: Request):

    # request.session.pop("username", None)

    return {"message": "Successfully logged out"}


# 비밀번호 수정
@router.put("/update}", status_code=status.HTTP_200_OK)
async def password_update_handler(
    request: PasswordUpdateRequest,
    user_service: UserService = Depends(),
):

    verified_user = await user_service.verify_credentials(
        request.email, request.password
    )
    if not verified_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    updated_user: UserSchema = await user_service.update_password(
        user_email=request.email, new_password=request.new_password
    )

    return {"user": updated_user}
