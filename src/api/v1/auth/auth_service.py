from datetime import datetime, timezone, timedelta
from typing import Dict, Any, Tuple
import logging
from fastapi import status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from src.api.v1.users.user_repository import UserRepository
from src.schemas.response import TokenData, User
from src.services.auth.cache import redis_client
from src.core.config.settings import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=True)


class AuthService:
    """
    AuthService class provides authentication and authorization services.
    It includes methods for:
     - creating access tokens,
     - verifying access tokens,
     - retrieving logged-in users.
    """

    def __init__(self):
        self.user_repository = UserRepository()
        self.encoding: str = "UTF-8"
        self.secretkey: str = settings.JWT_SECRET_KEY
        self.jwt_algorithm: str = settings.JWT_ALGORITHM
        self.token_expire_minutes = settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        # schemes = ["bcrypt"] : 비밀번호 암호화 알고리즘
        # deprecated="auto" : 사용되지 않는 알고리즘 자동 처리

    def create_access_token(self, data: Dict[str, Any]) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=self.token_expire_minutes
        )

        # 토큰 페이로드에 추가 보안 정보 포함
        to_encode.update(
            {
                "exp": expire,
                "iat": datetime.now(timezone.utc),
                "iss": "blog-app",  # 토큰 발급자
                "aud": "blog-app-users",  # 토큰 대상자
                "type": "access",  # 토큰 타입
                "sub": data.get("user_email"),  # JWT 표준에 맞게 sub 클레임 사용
            }
        )

        # 민감한 정보는 로깅하지 않음
        logging.info("Token created with expiration: %s", expire)

        jwt_token: str = jwt.encode(
            to_encode,
            self.secretkey,
            algorithm=self.jwt_algorithm,
        )

        return jwt_token

    async def verify_access_token(self, token: str) -> Tuple[TokenData, Dict[str, Any]]:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        try:
            payload = jwt.decode(
                token,
                self.secretkey,
                algorithms=[self.jwt_algorithm],
                audience="blog-app-users",
                issuer="blog-app",
            )

            user_email = payload.get("sub")
            logging.info(f"Token verified for user: {user_email}")

            if not user_email:
                logging.error("user_email not found in payload")
                raise credentials_exception

            token_data = TokenData(user_email=user_email)
            return token_data, payload

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
            token_data, _ = await self.verify_access_token(token)
            logging.info(f"Token data verified: {token_data}")

            # user_email이 있는지 확인
            if not token_data.user_email:
                logging.error("No user_email in token_data")
                raise credentials_exception

            # 사용자 조회 시도
            user = await self.user_repository.find_one_by_email(
                user_email=token_data.user_email
            )

            if user is None:
                logging.error(f"No user found for email: {token_data.user_email}")
                raise credentials_exception

            return user

        except Exception as e:
            logging.error(f"Error in logged_in_user: {str(e)}")
            raise credentials_exception

    async def logout(self, token: str) -> bool:
        """토큰을 블랙리스트에 추가하여 로그아웃 처리"""
        try:
            _, payload = await self.verify_access_token(token)
            exp_timestamp = payload.get("exp")

            # 현재 시간과 만료 시간 사이의 차이 계산
            current_time = int(datetime.now(timezone.utc).timestamp())
            ttl = max(0, exp_timestamp - current_time)

            if ttl <= 0:
                logging.info("Token is already expired")
                return True  # 이미 만료된 토큰은 처리 필요 없음

            # Redis에 블랙리스트 토큰 저장
            redis_client.setex(f"bl_{token}", ttl, "1")
            logging.info(f"Token blacklisted successfully, TTL: {ttl} seconds")
            return True

        except JWTError as e:
            logging.error(f"JWT error during logout: {str(e)}")
            return False
        except Exception as e:
            logging.error(f"Error during logout: {str(e)}")
            return False

    async def login(self, user_email: str, password: str) -> str:
        user = await self.user_repository.find_one_by_email(user_email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not self.pwd_context.verify(password, user.hashedpassword):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        token_data = {"user_email": user.email}
        return self.create_access_token(token_data)


# 전역 인스턴스 생성
auth_service = AuthService()


# 의존성 함수 정의
async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        if redis_client.get(f"bl_{token}"):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token is blacklisted",
                headers={"WWW-Authenticate": "Bearer"},
            )

        user: User = await auth_service.logged_in_user(token)
        return user

    except Exception as e:
        logging.error(f"Error in get_current_user: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e
