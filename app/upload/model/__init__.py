from typing import Any
from typing_extensions import Annotated
from fastapi import Query
from pydantic import BaseModel, Field

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

UploadType = Annotated[UploadParams, Query()]


class UploadPublic(BaseModel):
    upload_url: HttpCheck
    fields: dict[str, Any]
    asset_id: str
    upload_provider: UPLOAD_BUCKET_ENUM
