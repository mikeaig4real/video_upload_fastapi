from odmantic import Model, ObjectId, Field, Reference
from typing import Optional
from datetime import datetime, timezone
from pydantic import BaseModel

from app.core.config import UPLOAD_BUCKET_ENUM, get_config
from app.models.video import UPLOAD_STATUS_ENUM, VIDEO_LABEL_ENUM
from app.models.http_url import HttpCheck
from app.user.model.mongo import User

config = get_config()


class VideoBase(BaseModel):
    title: str
    description: Optional[str] = ""
    duration: float = Field(gt=0)
    is_public: bool = True
    size: int
    label: VIDEO_LABEL_ENUM
    upload_hash: str
    upload_provider: UPLOAD_BUCKET_ENUM = config.UPLOAD_BUCKET
    asset_id: str
    thumbnail_url: Optional[str] = None
    playback_url: HttpCheck
    type: Optional[str] = None
    upload_status: UPLOAD_STATUS_ENUM
    upload_url: HttpCheck


class Video(Model):
    title: str = Field()
    description: Optional[str] = ""
    duration: float = Field(gt=0)
    is_public: bool = True
    size: int
    label: VIDEO_LABEL_ENUM
    upload_hash: str = Field(unique=True)
    upload_provider: UPLOAD_BUCKET_ENUM = config.UPLOAD_BUCKET
    asset_id: str = Field(unique=True)
    thumbnail_url: Optional[str] = None
    playback_url: HttpCheck
    type: Optional[str] = None
    upload_status: UPLOAD_STATUS_ENUM
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    upload_url: HttpCheck = Field()
    user: User = Reference()
    user_id: ObjectId


class VideoCreate(VideoBase):
    pass


class VideoPublic(VideoBase):
    id: str
    created_at: datetime
    updated_at: datetime


class VideoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_public: Optional[bool] = None
