from odmantic import ObjectId, Reference, Field
from odmantic.model import Model
from typing import Optional
from datetime import datetime, timezone
from app.core.config import UPLOAD_BUCKET_ENUM
from app.models.http_url import HttpCheck, HttpType
from app.user.model.mongo import User


class VideoBase(Model):
    title: str
    description: Optional[str] = None
    is_public: bool = True


class Video(Model):
    id: Optional[ObjectId] = Field(default=None, primary_field=True)
    upload_url: HttpCheck = Field(unique=True)
    user: User = Reference()
    user_id: ObjectId
    title: str
    description: Optional[str] = None
    is_public: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    upload_hash: str = Field(unique=True)
    upload_provider: UPLOAD_BUCKET_ENUM = Field(default=UPLOAD_BUCKET_ENUM.CLOUDINARY)
    asset_id: str = Field(unique=True)


class VideoCreate(Model):
    upload_url: HttpType
    title: str
    description: Optional[str] = None
    is_public: bool = True

class VideoPublic(Model):
    upload_url: HttpCheck
    created_at: datetime
    updated_at: datetime
    user_id: ObjectId


class VideoUpdate(Model):
    title: Optional[str] = None
    description: Optional[str] = None
    is_public: Optional[bool] = None
