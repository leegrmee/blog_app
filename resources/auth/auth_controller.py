import logging
from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from resources.auth.auth_utils import verify_password
from resources.schemas.request import PasswordUpdateRequest
from resources.schemas.response import JWTResponse, User
from resources.user.user_service import UserService
from resources.auth.auth_service import get_current_user, auth_service

router = APIRouter(prefix="/auth", tags=["Authentication"])


# 로그인
@router.post("/login", status_code=status.HTTP_200_OK)
async def user_login_handler(
    user_service: UserService = Depends(),
    user_credentials: OAuth2PasswordRequestForm = Depends(),
):

    user: User | None = await user_service.find_one_by_email(user_credentials.username)
    # user_credentials.username - Oauth2 에서 username 은 email 임

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials"
        )

    if not verify_password(user_credentials.password, user.hashedpassword):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials"
        )

    token_data = {"user_email": user.email}
    logging.info(f"Creating token with data: {token_data}")

    token: str = auth_service.create_access_token({"user_email": user.email})

    return JWTResponse(access_token=token)


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

    return "Password updated successfully"
