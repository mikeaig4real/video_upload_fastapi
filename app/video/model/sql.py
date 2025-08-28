from sqlmodel import Field, Index, SQLModel, Relationship
from typing import Optional
from datetime import datetime
from sqlalchemy import Column, DateTime, func

from app.constants import URL_REGEX
from app.core.config import UPLOAD_BUCKET_ENUM, get_config
from app.models.http_url import HttpCheck
from app.models.video import UPLOAD_STATUS_ENUM, VIDEO_LABEL_ENUM
from app.user.model.sql import User

config = get_config()


class VideoBase(SQLModel):
    title: str = Field(index=True)
    description: Optional[str] = None
    duration: int
    is_public: bool = True
    size: int = Field(gt=0, le=config.MAX_VIDEO_SIZE)
    label: VIDEO_LABEL_ENUM
    upload_hash: str = Field(sa_column_kwargs={"unique": True})
    upload_provider: UPLOAD_BUCKET_ENUM = Field(default=UPLOAD_BUCKET_ENUM.CLOUDINARY)
    asset_id: str = Field(sa_column_kwargs={"unique": True})
    thumbnail_url: HttpCheck = Field(regex=URL_REGEX)
    playback_url: HttpCheck = Field(regex=URL_REGEX)
    type: Optional[str] = None
    upload_status: UPLOAD_STATUS_ENUM
    upload_url: HttpCheck = Field(regex=URL_REGEX)
    __table_args__ = (
        Index(
            "idx_user_id_title_type_upload_status_label_is_public",
            "user_id",
            "title",
            "type",
            "upload_status",
            "label",
            "is_public",
        ),
    )


class Video(VideoBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    user: Optional[User] = Relationship(back_populates="videos")
    user_id: int = Field(default=None, foreign_key="user.id", index=True)
    created_at: datetime | None = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )
    # todo: check if ts is implemented for mongo
    updated_at: datetime | None = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True), onupdate=func.now(), server_default=func.now()
        )
    )

class VideoCreate(VideoBase):
    pass


class VideoPublic(VideoBase):
    id: int
    created_at: datetime
    updated_at: datetime

class VideoUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_public: Optional[bool] = None
