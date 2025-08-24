from datetime import datetime, timezone
from pydantic import BaseModel, EmailStr
from typing import Optional, TYPE_CHECKING
from odmantic import Field, Model

if TYPE_CHECKING:
    from app.video.model.mongo import Video  # type: ignore


class UserBase(BaseModel):
    email: EmailStr
    username: str


class User(Model):
    email: EmailStr = Field(index=True, unique=True)
    username: str = Field(index=True, unique=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class UserCreate(UserBase):
    password: str


class UserPublic(UserBase):
    id: str
    created_at: datetime
    updated_at: datetime


class UserUpdate(BaseModel):
    username: Optional[str] = None
