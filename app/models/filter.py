from typing import Annotated, Any, Literal
from fastapi import Query
from pydantic import BaseModel, Field

from app.models.video import UPLOAD_STATUS_ENUM, VIDEO_LABEL_ENUM


class FilterOptionsParams(BaseModel):
    """
    Filter params for video records
    """
    model_config = {"extra": "forbid"}

    # pagination related
    limit: int = Field(100, gt=0, le=100)
    page: int = Field(1, ge=1)
    order_by: Literal["created_at", "updated_at"] = "created_at"
    order: Literal["desc", "asc"] = "asc"

    # video related
    title: str | None = None
    type: str | None = None
    upload_status: UPLOAD_STATUS_ENUM | None = None
    label: VIDEO_LABEL_ENUM | None = None
    is_public: bool | None = None

    def pagination_dict(self) -> dict[str, Any]:
        return self.model_dump(include={"limit", "page", "order_by", "order"})

    def video_filters_dict(self) -> dict[str, Any]:
        return self.model_dump(
            include={"title", "type", "upload_status", "label", "is_public"},
            exclude_none=True,
        )


FilterOptionsType = Annotated[FilterOptionsParams, Query()]
