from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from src.services.auth.auth_utils import verify_password
from src.schemas.request import PasswordUpdateRequest
from src.schemas.response import JWTResponse, User
from src.api.v1.users.user_service import UserService
from src.api.v1.auth.auth_service import (
    get_current_user,
    auth_service,
    oauth2_scheme,
)


router = APIRouter(prefix="/auth", tags=["Authentication"])


# 로그인
@router.post("/login", response_model=JWTResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_service: UserService = Depends(),
):
    """
    OAuth2 호환 로그인 엔드포인트
    username 필드에 이메일을 입력하세요
    """
    user = await user_service.find_one_by_email(form_data.username)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not verify_password(form_data.password, user.hashedpassword):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token_data = {"user_email": user.email}
    access_token = auth_service.create_access_token(token_data)

    return JWTResponse(access_token=access_token, token_type="bearer")


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
