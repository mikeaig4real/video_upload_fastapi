from odmantic import Model, Field, Reference
from typing import Optional
from datetime import datetime, timezone
from pydantic import BaseModel

from app.core.config import UPLOAD_BUCKET_ENUM
from app.models.video import UPLOAD_STATUS_ENUM
from app.models.http_url import HttpCheck
from app.user.model.mongo import User



class VideoBase(BaseModel):
    title: str
    description: Optional[str] = None
    is_public: bool = True
    size: float
    label: str
    upload_hash: str
    upload_provider: UPLOAD_BUCKET_ENUM = UPLOAD_BUCKET_ENUM.CLOUDINARY
    asset_id: str
    thumbnail_url: Optional[str] = None
    playback_url: HttpCheck
    type: Optional[str] = None
    upload_status: UPLOAD_STATUS_ENUM
    created_at: datetime = datetime.now(timezone.utc)
    updated_at: datetime = datetime.now(timezone.utc)
    upload_url: HttpCheck



class Video(Model):
    title: str = Field(unique=True)
    description: Optional[str] = None
    is_public: bool = True
    size: float
    label: str
    upload_hash: str = Field(unique=True)
    upload_provider: UPLOAD_BUCKET_ENUM = Field(default=UPLOAD_BUCKET_ENUM.CLOUDINARY)
    asset_id: str = Field(unique=True)
    thumbnail_url: Optional[str] = None
    playback_url: HttpCheck
    type: Optional[str] = None
    upload_status: UPLOAD_STATUS_ENUM
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    upload_url: HttpCheck = Field(unique=True)
    user: User = Reference()



class VideoCreate(VideoBase):
    pass


class VideoPublic(VideoBase):
    id: str
    user_id: str


class VideoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_public: Optional[bool] = None
