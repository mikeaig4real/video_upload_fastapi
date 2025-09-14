from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar, TypedDict
from odmantic import ObjectId
from pydantic import BaseModel

BModel = TypeVar("BModel", bound=BaseModel)
BCreate = TypeVar("BCreate", bound=BaseModel)
BUpdate = TypeVar("BUpdate", bound=BaseModel)
BId = int | str | ObjectId | None


class BOptions(TypedDict, total=False):
    offset: int | None
    limit: int | None
    page: int | None
    order_by: str | None
    order: str | None


class BaseCrud(ABC, Generic[BModel, BCreate, BUpdate]):
    """
    Base (abstract) class for db crud specific methods
    """
    @abstractmethod
    async def create(self, *, data: BCreate, **kwargs: Any) -> BModel: ...

    @abstractmethod
    async def get(self, *, id: BId, **kwargs: Any) -> BModel | None: ...

    @abstractmethod
    async def get_by(
        self, *, field: str, value: Any, many: bool, **kwargs: Any
    ) -> BModel | list[BModel] | None: ...

    @abstractmethod
    async def list(self, *, options: BOptions, **kwargs: Any) -> list[BModel]: ...

    @abstractmethod
    async def update(
        self, *, id: BId, data: BUpdate, **kwargs: Any
    ) -> BModel | None: ...

    @abstractmethod
    async def upsert(
        self, *, id: BId, data: BCreate, **kwargs: Any
    ) -> BModel | None: ...

    @abstractmethod
    async def delete(self, *, id: BId, **kwargs: Any) -> BModel | None: ...
