from datetime import datetime, timezone
from pydantic import BaseModel
from typing import Optional
from odmantic import Field, Model, ObjectId

from app.core.config import UPLOAD_BUCKET_ENUM, get_config
from app.models.video import UPLOAD_STATUS_ENUM, VIDEO_LABEL_ENUM

config = get_config()

class UploadBase(BaseModel):
    title: str
    description: Optional[str] = ""
    duration: float
    is_public: bool = True
    size: int = Field(gt=0, le=config.MAX_VIDEO_SIZE)
    label: VIDEO_LABEL_ENUM
    upload_hash: str
    upload_provider: UPLOAD_BUCKET_ENUM = config.UPLOAD_BUCKET
    asset_id: str = Field(index=True, unique=True)
    type: Optional[str] = None
    upload_status: UPLOAD_STATUS_ENUM = Field(index=True)
    eager: str = "c_fill,h_300,w_400/jpg"
    user_id: ObjectId 


class Upload(Model):
    title: str
    description: Optional[str] = ""
    duration: float
    is_public: bool = True
    size: int = Field(gt=0, le=config.MAX_VIDEO_SIZE)
    label: VIDEO_LABEL_ENUM
    upload_hash: str
    upload_provider: UPLOAD_BUCKET_ENUM = config.UPLOAD_BUCKET
    asset_id: str = Field(index=True, unique=True)
    type: Optional[str] = None
    upload_status: UPLOAD_STATUS_ENUM = Field(index=True)
    eager: str = "c_fill,h_300,w_400/jpg"
    user_id: ObjectId
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class UploadCreate(UploadBase):
    pass


class UploadPublic(UploadBase):
    id: str
    created_at: datetime
    updated_at: datetime


class UploadUpdate(BaseModel):
    upload_status: Optional[str] = None
