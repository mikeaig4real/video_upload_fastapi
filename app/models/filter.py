from typing import Annotated, Literal
from fastapi import Query
from pydantic import BaseModel, Field


class FilterParams(BaseModel):
    model_config = {"extra": "forbid"}

    limit: int = Field(100, gt=0, le=100)
    page: int = Field(1, ge=1)
    order_by: Literal["created_at", "updated_at"] = "created_at"
    order: Literal["desc", "asc"] = "asc"

FilterType = Annotated[FilterParams, Query()]
