from fastapi import APIRouter, status, Depends, HTTPException, Body
from typing import Optional

from resources.auth.auth_utils import verify_password
from resources.schemas.request import UserLoginRequest, PasswordUpdateRequest
from resources.schemas.response import JWTResponse, UserSchema
from resources.user.user_service import UserService
from resources.auth.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


# 로그인
@router.post("/login", status_code=status.HTTP_200_OK)
async def user_login_handler(
    request: UserLoginRequest = Body(...),
    user_service: UserService = Depends(),
    auth_service: AuthService = Depends(),
):

    user: Optional[UserSchema] = await user_service.get_user_by_email(request.email)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials"
        )

    if not verify_password(request.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials"
        )

    token: str = auth_service.create_access_token({"user_id": user.id})

    return JWTResponse(access_token=token)


"""While the UserService handles the business logic of updating the password 
in the database, the auth_controller.py is responsible for the security checks 
and ensuring that the user is authenticated and authorized to make such changes. """


# 비밀번호 수정
@router.put("/update-password", status_code=status.HTTP_200_OK)
async def password_update_handler(
    request: PasswordUpdateRequest = Body(...),
    user_service: UserService = Depends(),
    current_user: UserSchema = Depends(AuthService.logged_in_user),
):
    if current_user.email != request.email:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials"
        )

    if not verify_password(request.password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials"
        )

    updated_user: UserSchema = await user_service.update_password(
        email=current_user.email, new_password=request.new_password
    )

    return {"message": "Password updated successfully", "user": updated_user}
