from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, OAuth2PasswordBearer
from pwdlib import PasswordHash

from app.core.settings import settings
from app.models.user import User

http_bearer = HTTPBearer()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


class AuthService:
    def __init__(self):
        self.password_hash = PasswordHash.recommended()

    async def authenticate_user(self, email: str, password: str) -> User:
        user = await User.get(email=email)

        if user and self.verify_password(password, user.password_hash):
            return user

        raise Exception("Credenciais inválidas")

    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        to_encode.update({"exp": expire})

        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

        return encoded_jwt

    def create_refresh_token(self, data: dict) -> str:
        to_encode = data.copy()
        now = datetime.now(timezone.utc)
        expire = now + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        to_encode.update({"iat": now, "exp": expire, "type": "refresh"})
        return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    @staticmethod
    def validate_access_token(token: str) -> int:
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            return payload.get("sub")
        except jwt.ExpiredSignatureError:
            raise HTTPException(detail="Não autorizado", status_code=401)
        except jwt.InvalidTokenError:
            raise HTTPException(detail="Não autorizado", status_code=401)
        except Exception:
            raise HTTPException(detail="Não autorizado", status_code=401)

    def validate_refresh_token(token: str) -> bool:
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            if payload.get("type") != "refresh":
                raise HTTPException(detail="Não autorizado", status_code=401)
            return payload.get("sub")
        except jwt.ExpiredSignatureError:
            raise HTTPException(detail="Não autorizado", status_code=401)
        except jwt.InvalidTokenError:
            raise HTTPException(detail="Não autorizado", status_code=401)
        except Exception:
            raise HTTPException(detail="Não autorizado", status_code=401)

    def generate_password_hash(self, password: str) -> str:
        return self.password_hash.hash(password)

    def verify_password(self, password: str, hashed_password: str) -> bool:
        try:
            result = self.password_hash.verify(password, hashed_password)
        except Exception:
            result = False
        finally:
            return result

    @staticmethod
    async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
        user_id = AuthService.validate_access_token(token)

        if user_id is None:
            raise HTTPException(detail="Não autorizado", status_code=401)

        return await User.get(id=user_id)
