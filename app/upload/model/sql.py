from datetime import datetime
from sqlalchemy import Column
from sqlmodel import DateTime, Field, SQLModel, func
from typing import Optional
from app.core.config import UPLOAD_BUCKET_ENUM, get_config
from app.models.video import UPLOAD_STATUS_ENUM, VIDEO_LABEL_ENUM


config = get_config()


class UploadBase(SQLModel):
    title: str
    description: Optional[str] = ""
    duration: float
    is_public: bool = True
    size: int = Field(gt=0, le=config.MAX_VIDEO_SIZE)
    label: VIDEO_LABEL_ENUM
    upload_hash: str
    upload_provider: UPLOAD_BUCKET_ENUM = config.UPLOAD_BUCKET
    asset_id: str = Field(sa_column_kwargs={"unique": True})
    type: Optional[str] = None
    upload_status: UPLOAD_STATUS_ENUM = Field(
        default=UPLOAD_STATUS_ENUM.COMPLETED, index=True
    )
    eager: str = "c_fill,h_300,w_400/jpg"
    user_id: int
    height: int
    width: int

class Upload(UploadBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    created_at: datetime | None = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), server_default=func.now()),
    )
    updated_at: datetime | None = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True), onupdate=func.now(), server_default=func.now()
        ),
    )


class UploadCreate(UploadBase):
    pass


class UploadPublic(UploadBase):
    id: int
    created_at: datetime
    updated_at: datetime


class UploadUpdate(SQLModel):
    upload_status: Optional[str] = None
