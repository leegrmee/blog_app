from fastapi import APIRouter, status, Depends, HTTPException
from typing import Optional

from resources.user.user_service import UserService

from resources.schemas.request import UserSignupRequest

from resources.schemas.response import User, SignUpResponse


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[User] | None)
def get_users_handler(user_service: UserService = Depends()) -> list[User] | None:
    # TODO: валидации входных и выходных данных
    # но лучше найти способ использовать
    return user_service.find_many()


@router.get("/{user_id}", status_code=status.HTTP_200_OK, response_model=User | None)
def get_user_by_id_handler(
    user_id: int, user_service: UserService = Depends()
) -> User | None:
    return user_service.find_one_by_id(user_id)


# 회원가입
@router.post("/signup", status_code=status.HTTP_201_CREATED)
def user_signup_handler(
    request: UserSignupRequest,
    user_service: UserService = Depends(),
) -> SignUpResponse:
    return user_service.signup(request)
