from typing import Any, Dict, List, Literal, Tuple, TypeVar
from fastapi.encoders import jsonable_encoder
from odmantic import AIOEngine, Model
from motor.core import AgnosticDatabase
from pydantic import BaseModel
from app.db.connect.mongo import get_engine
from app.crud.base import BaseCrud, BId, BOptions

OModel = TypeVar("OModel", bound=Model)
OCreate = TypeVar("OCreate", bound=BaseModel)
OUpdate = TypeVar("OUpdate", bound=BaseModel)

OffsetType = Dict[str, str | int | Tuple[str, str | int] | Dict[str, int | str]]


class MONGOCrud(BaseCrud[OModel, OCreate, OUpdate]):

    def __init__(self, model: type[Model]):
        self.model = model
        self.engine: AIOEngine = get_engine()

    async def create(self, data: OCreate, session: AgnosticDatabase[Any], *args: Any, **kwargs: Any) -> OModel:
        entity_data = jsonable_encoder(data)
        entity = self.model(**entity_data)
        return await self.engine.save(entity)  # type: ignore

    async def get(self, id: BId, session: AgnosticDatabase[Any], *args: Any, **kwargs: Any) -> OModel | None:
        return await self.engine.find_one(self.model, self.model.id == id)  # type: ignore

    async def list(
        self, options: BOptions, session: AgnosticDatabase[Any], *args: Any, **kwargs: Any
    ) -> List[OModel]:
        limit = options.get("limit", 100)
        page = options.get("page", 1)
        skip = (page - 1) * limit
        order_by = options.get("order_by", "id")
        column = getattr(self.model, order_by)
        order: Literal["asc", "desc"] = options.get("order", "asc")
        # direction: int = -1 if order == "desc" else 1
        if order == "desc":
            sort = column.desc()
        else:
            sort = column.asc()
        offset: OffsetType = {
            "skip": skip,
            "limit": limit,
            "sort": sort,
        }
        return list(await self.engine.find(self.model, **offset))  # type: ignore

    async def update(
        self, id: BId, data: OUpdate, session: AgnosticDatabase[Any], *args: Any, **kwargs: Any
    ) -> OModel | None:
        entity_db = await self.get(id=id, session=session)
        if not entity_db:
            return None
        entity_data = jsonable_encoder(data)
        if isinstance(data, dict):
            update_data = data
        else:
            update_data = data.model_dump(exclude_unset=True)
        for field in entity_data:
            if field in update_data:
                setattr(entity_db, field, update_data[field])
        # TODO: Check if this saves changes with the setattr calls
        await self.engine.save(entity_db)  # type: ignore
        return entity_db
    
    async def upsert(
        self, id: BId, data: OCreate, session: AgnosticDatabase[Any], update: bool = False, *args: Any, **kwargs: Any
    ) -> OModel | None:
        entity_db = await self.get(id=id, session=session)
        
        if not entity_db:
            return await self.create(data=data, session=session)
        
        if not update:
            return entity_db
        
        entity_data = jsonable_encoder(data)
        if isinstance(data, dict):
            update_data = data
        else:
            update_data = data.model_dump(exclude_unset=True)
        for field in entity_data:
            if field in update_data:
                setattr(entity_db, field, update_data[field])
        # TODO: Check if this saves changes with the setattr calls
        await self.engine.save(entity_db)  # type: ignore
        return entity_db

    async def delete(self, id: BId, session: AgnosticDatabase[Any], *args: Any, **kwargs: Any) -> OModel | None:
        entity_db = await self.get(id=id, session=session)
        if entity_db:
            await self.engine.delete(entity_db)  # type: ignore
        return entity_db
