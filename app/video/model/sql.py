from sqlmodel import Field, SQLModel, Relationship
from typing import Optional
from datetime import datetime, timezone
from app.constants import URL_REGEX
from app.core.config import UPLOAD_BUCKET_ENUM
from app.models.http_url import HttpType
from app.user.model.sql import User


class VideoBase(SQLModel):
    title: str
    description: Optional[str] = None
    is_public: bool = True


class Video(VideoBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    upload_url: str = Field(unique=True, regex=URL_REGEX)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={"onupdate": lambda: datetime.now(timezone.utc)},
    )
    user_id: int = Field(default=None, foreign_key="user.id")
    user: User = Relationship(back_populates="videos")
    upload_hash: str = Field(unique=True)
    upload_provider: UPLOAD_BUCKET_ENUM = Field(default=UPLOAD_BUCKET_ENUM.CLOUDINARY)
    asset_id: str = Field(unique=True)


class VideoCreate(VideoBase):
    upload_url: HttpType


class VideoPublic(VideoBase):
    id: int
    upload_url: HttpType
    created_at: datetime
    user_id: int
    updated_at: datetime


class VideoUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_public: Optional[bool] = None
