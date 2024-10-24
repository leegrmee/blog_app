from datetime import datetime, timedelta, timezone
from typing import List, Optional, Dict, Any
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer


from resources.schemas.request import UserSignupRequest
from resources.schemas.response import UserSchema, SignUpSchema, TokenData
from resources.user.user_repository import UserRepository


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


class UserService:
    def __init__(self):
        self.encoding: str = "UTF-8"
        self.secretkey: str = (
            "fca1c9a668eb97796fc628eac4ba85a50538279ee2f3a2816ebf3e67a0e6a026"
        )
        self.jwt_algorithm: str = "HS256"
        self.token_expire_minutes = 30
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    async def get_users(self) -> List[UserSchema]:
        return await UserRepository.get_users()

    async def get_user_by_id(self, user_id: int) -> Optional[UserSchema]:
        return await UserRepository.get_user_by_id(user_id)

    async def get_user_by_email(self, user_email: str) -> Optional[UserSchema]:
        return await UserRepository.get_user_by_email(user_email)

    def hash_password(self, plain_password: str) -> str:
        # hashed_password: bytes = bcrypt.hashpw(
        #     plain_password.encode(self.encoding),
        #     salt=bcrypt.gensalt(),
        # )
        hashed_password = self.pwd_context.hash(plain_password)
        return hashed_password.decode(self.encoding)

    async def signup_user(self, request: UserSignupRequest) -> SignUpSchema:
        hashed_password = self.hash_password(request.password)
        return await UserRepository.create_user(
            request.username, request.email, hashed_password
        )

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(
            plain_password.encode(self.encoding),
            hashed_password.encode(self.encoding),
        )

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
            user_id: int = payload.get("user_id")

            if user_id is None:
                raise credentials_exception

            user_id = TokenData(user_id=user_id)

        except JWTError:
            raise credentials_exception

        return user_id

    async def logged_in_user(self, token: str = Depends(oauth2_scheme)) -> UserSchema:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        token_data = await self.verify_access_token(token, credentials_exception)
        user = await UserRepository.get_user_by_id(token_data.user_id)
        if user is None:
            raise credentials_exception

        return user

    async def update_password(self, email: str, new_password: str) -> UserSchema:
        new_hashed_password: str = self.hash_password(new_password)
        updated_password: UserSchema = await UserRepository.update_password(
            user_email=email, new_hashed_password=new_hashed_password
        )

        return UserSchema(email=email)
