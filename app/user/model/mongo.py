from datetime import datetime, timezone
from pydantic import EmailStr
from typing import Optional, TYPE_CHECKING
from odmantic import Field
from odmantic import Model

if TYPE_CHECKING:
    from app.video.model.mongo import Video  # type: ignore


class UserBase(Model):
    email: EmailStr = Field()
    username: str = Field()


class User(Model):
    email: EmailStr = Field(index=True)
    username: str = Field()
    hashed_password: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class UserCreate(Model):
    password: str = Field()
    email: EmailStr = Field()
    username: str = Field()


class UserPublic(Model):
    email: EmailStr = Field()
    username: str = Field()


class UserUpdate(Model):
    username: Optional[str] = None
