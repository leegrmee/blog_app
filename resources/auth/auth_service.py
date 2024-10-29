from fastapi import status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import datetime, timezone, timedelta
from typing import Dict, Any
from passlib.context import CryptContext
import logging
from resources.user.user_repository import UserRepository
from resources.schemas.response import TokenData, User

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

        # 토큰 페이로드 로깅
        logging.info(f"Token data before encoding: {to_encode}")

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
            logging.info(f"Decoded token payload: {payload}")

            user_email = payload.get("user_email")
            logging.info(f"Extracted user_email: {user_email}")  # 추출된 이메일 로깅

            if not user_email:
                logging.error("user_email not found in payload")
                raise credentials_exception

            token_data = TokenData(user_email=user_email)
            logging.info(f"Created TokenData: {token_data}")  # 생성된 TokenData 로깅

            return token_data

        except JWTError as e:
            logging.error(f"JWTError in verify_access_token: {str(e)}")
            raise credentials_exception

    async def logged_in_user(self, token: str) -> User:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        try:
            token_data = await self.verify_access_token(token, credentials_exception)
            logging.info(f"Token data verified: {token_data}")  # 로깅 추가

            # user_email이 있는지 확인
            if not token_data.user_email:
                logging.error("No user_email in token_data")
                raise credentials_exception

            # 사용자 조회 시도
            user = await self.user_repository.find_one_by_email(
                user_email=token_data.user_email
            )
            logging.info(f"User lookup result: {user}")  # 로깅 추가

            if user is None:
                logging.error(f"No user found for email: {token_data.user_email}")
                raise credentials_exception

            return user

        except Exception as e:
            logging.error(f"Error in logged_in_user: {str(e)}")
            raise credentials_exception


# 전역 인스턴스 생성
auth_service = AuthService()


# 의존성 함수 정의
async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        user: User = await auth_service.logged_in_user(token)
        logging.info(f"Current user: {user}")
        logging.info(f"Successfully retrieved user: {user.email}")

        return user
    except Exception as e:
        logging.error(f"Error in get_current_user: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e
