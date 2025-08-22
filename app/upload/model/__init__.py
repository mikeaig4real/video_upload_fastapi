from typing import Any
from typing_extensions import Annotated
from fastapi import Query
from pydantic import BaseModel

from app.core.config import UPLOAD_BUCKET_ENUM
from app.models.http_url import HttpCheck


class UploadParams(BaseModel):
    folder: str | None = "videos"
    title: str | None = None

UploadType = Annotated[UploadParams, Query()]


class UploadPublic(BaseModel):
    upload_url: HttpCheck
    fields: dict[str, Any]
    asset_id: str
    upload_provider: UPLOAD_BUCKET_ENUM

