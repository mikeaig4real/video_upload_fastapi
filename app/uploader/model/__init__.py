from typing import Any, Optional
from typing_extensions import Annotated
from fastapi import Body
from pydantic import BaseModel, Field
from app.models.video import VIDEO_LABEL_ENUM
from app.uploader.model import *
from app.constants import VIDEO_FORMAT_REGEX
from app.core.config import UPLOAD_BUCKET_ENUM, get_config
from app.models.http_url import HttpCheck

config = get_config()


class UploadParams(BaseModel):
    folder: str | None = "videos"
    title: str
    type: str = Field(pattern=VIDEO_FORMAT_REGEX)
    size: float | int = Field(gt=0, le=config.MAX_VIDEO_SIZE)
    upload_hash: str
    description: Optional[str] = ""
    duration: float
    is_public: bool = True
    label: VIDEO_LABEL_ENUM
    upload_hash: str
    upload_provider: UPLOAD_BUCKET_ENUM = config.UPLOAD_BUCKET
    eager: str = "c_fill,h_300,w_400/jpg"
    height: int
    width: int


UploadType = Annotated[UploadParams, Body()]


class UploadPublic(BaseModel):
    upload_url: HttpCheck
    fields: dict[str, Any]
    asset_id: str
    upload_provider: UPLOAD_BUCKET_ENUM


class UploadResource(BaseModel):
    folder: str | None = "videos"
    title: str
    type: str = Field(pattern=VIDEO_FORMAT_REGEX)
    size: float | int = Field(gt=0, le=config.MAX_VIDEO_SIZE)
    upload_hash: str
