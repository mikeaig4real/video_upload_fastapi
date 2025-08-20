from fastapi.encoders import jsonable_encoder
from typing import Any

from app.constants import ResponseType


def SuccessResponse(data: Any) -> ResponseType:
    return {"success": True, "data": jsonable_encoder(data)}
