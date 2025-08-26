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
    @abstractmethod
    async def create(self, data: BCreate, *args: Any, **kwargs: Any) -> BModel: ...

    @abstractmethod
    async def get(self, id: BId, *args: Any, **kwargs: Any) -> BModel | None: ...

    @abstractmethod
    async def list(
        self, options: BOptions, *args: Any, **kwargs: Any
    ) -> list[BModel]: ...

    @abstractmethod
    async def update(
        self, id: BId, data: BUpdate, *args: Any, **kwargs: Any
    ) -> BModel | None: ...

    @abstractmethod
    async def upsert(
        self, id: BId, data: BCreate, *args: Any, **kwargs: Any
    ) -> BModel | None: ...

    @abstractmethod
    async def delete(self, id: BId, *args: Any, **kwargs: Any) -> BModel | None: ...
