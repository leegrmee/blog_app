from fastapi import status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import datetime, timezone, timedelta
from typing import Dict, Any
from passlib.context import CryptContext

from resources.user.user_repository import UserRepository
from resources.schemas.response import TokenData, UserResponse

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


class AuthService:
    def __init__(self):
        self.user_repository = UserRepository()
        self.encoding: str = "UTF-8"
        self.secretkey: str = (
            "fca1c9a668eb97796fc628eac4ba85a50538279ee2f3a2816ebf3e67a0e6a026"
        )
        self.jwt_algorithm: str = "HS256"
        self.token_expire_minutes = 30
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def create_access_token(self, data: Dict[str, Any]) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=self.token_expire_minutes
        )
        to_encode.update({"exp": expire, "iat": datetime.now(timezone.utc)})
        # iat = issued at

        jwt_token: str = jwt.encode(
            to_encode,
            self.secretkey,
            algorithm=self.jwt_algorithm,
        )

        return jwt_token

    async def verify_access_token(self, token: str, credentials_exception) -> TokenData:

        try:
            payload = jwt.decode(token, self.secretkey, algorithms=[self.jwt_algorithm])
            user_email: int = payload.get("user_email")

            if user_email is None:
                raise credentials_exception

            return TokenData(user_email=user_email)

        except JWTError:
            raise credentials_exception

    async def logged_in_user(self, token: str) -> UserResponse:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        token_data = await self.verify_access_token(token, credentials_exception)
        user = await self.user_repository.get_user_by_email(
            user_email=token_data.user_email
        )
        if user is None:
            raise credentials_exception

        return user


# 전역 인스턴스 생성
auth_service = AuthService()


# 의존성 함수 정의
async def get_current_user(token: str = Depends(oauth2_scheme)):
    return await auth_service.logged_in_user(token)
