from datetime import datetime, timedelta, timezone
from typing import TypedDict
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
import jwt
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext

from app.core.config import get_config
from app.user.model import User

config = get_config()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_pass(plain_pass: str, hashed_pass: str) -> bool:
    return pwd_context.verify(plain_pass, hashed_pass)

def hash_pass(plain_pass: str) -> str:
    return pwd_context.hash(secret=plain_pass)


def make_exception(code: int, detail: str):
    return HTTPException(
        status_code=code,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer"},
    )


class ToTokenType(TypedDict, total=False):
    sub: str
    id: str | int
    exp: datetime


class UserTokenType(BaseModel):
    id: str | int
    username: str
    email: EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserTokenType


def create_access_token(data: ToTokenType, expires_delta: timedelta | None = None):
    to_encode = dict(data.copy())
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": int(expire.timestamp())})
    to_encode = jsonable_encoder(to_encode)
    encoded_jwt = jwt.encode(payload=to_encode, key=config.SECRET_KEY, algorithm=config.ENCODE_ALGORITHM)  # type: ignore
    return encoded_jwt


def make_user_token(user: User):
    to_token: ToTokenType = {
        "sub": user.email,
        "id": str(user.id),
    }
    user_info = UserTokenType(username=user.username, email=user.email, id=to_token["id"])
    access_token = create_access_token(to_token)
    token_type = "bearer"
    return Token(access_token=access_token, token_type=token_type, user=user_info)


def decode_token(token: str):
    return jwt.decode(token, config.SECRET_KEY, algorithms=config.ENCODE_ALGORITHM) # type: ignore
