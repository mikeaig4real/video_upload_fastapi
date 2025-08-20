from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar, TypedDict
from odmantic import ObjectId
from pydantic import BaseModel

BModel = TypeVar("BModel", bound=BaseModel)
BCreate = TypeVar("BCreate", bound=BaseModel)
BUpdate = TypeVar("BUpdate", bound=BaseModel)
BId = int | str | ObjectId


class BOptions(TypedDict, total=False):
    offset: int
    limit: int
    page: int
    order_by: str


class BaseCrud(ABC, Generic[BModel, BCreate, BUpdate]):
    @abstractmethod
    def create(self, data: BCreate, *args: Any, **kwargs: Any) -> Any: ...

    @abstractmethod
    def get(self, id: BId, *args: Any, **kwargs: Any) -> Any: ...

    @abstractmethod
    def list(self, options: BOptions, *args: Any, **kwargs: Any) -> Any: ...

    @abstractmethod
    def update(self, id: BId, data: BUpdate, *args: Any, **kwargs: Any) -> Any: ...

    @abstractmethod
    def delete(self, id: BId, *args: Any, **kwargs: Any) -> Any: ...
