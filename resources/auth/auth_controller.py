import logging
from fastapi import APIRouter, status, Depends, HTTPException
from resources.auth.auth_utils import verify_password
from resources.schemas.request import (
    PasswordUpdateRequest,
    UserLoginRequest,
)
from resources.schemas.response import JWTResponse, User
from resources.auth.cache import redis_client
from resources.user.user_service import UserService
from resources.auth.auth_service import (
    get_current_user,
    auth_service,
    oauth2_scheme,
)
from jose import JWTError

router = APIRouter(prefix="/auth", tags=["Authentication"])


# 로그인
@router.post("/login", status_code=status.HTTP_200_OK)
async def user_login_handler(
    user_credentials: UserLoginRequest,
    user_service: UserService = Depends(),
):
    user: User | None = await user_service.find_one_by_email(user_credentials.email)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="User not found"
        )

    if not verify_password(user_credentials.password, user.hashedpassword):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid password"
        )

    token_data = {"user_email": user.email}
    logging.info(f"Creating token with data: {token_data}")

    token: str = auth_service.create_access_token({"user_email": user.email})

    return JWTResponse(access_token=token)


# logout
@router.post("/logout", status_code=status.HTTP_200_OK)
async def user_logout_handler(
    current_user: User = Depends(get_current_user),
    token: str = Depends(oauth2_scheme),
):
    success_logout = await auth_service.logout(token)

    if not success_logout:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Failed to logout",
        )

    return {"message": "Logged out successfully"}


# 비밀번호 수정
@router.put("/update-password", status_code=status.HTTP_200_OK)
async def password_update_handler(
    request: PasswordUpdateRequest,
    user_service: UserService = Depends(),
    current_user: User | None = Depends(get_current_user),
):
    if current_user.email != request.email:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials"
        )

    if not verify_password(request.password, current_user.hashedpassword):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials"
        )

    await user_service.update_password(
        email=current_user.email, new_password=request.new_password
    )

    return {"message": "Password updated successfully"}
