from pydantic import BaseModel
from typing import Generic, TypeVar

T = TypeVar("T")


class SuccessModel(BaseModel, Generic[T]):
    """
    Success model response
    """
    success: bool = True
    data: T
