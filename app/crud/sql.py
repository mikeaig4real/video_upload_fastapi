from sqlmodel import SQLModel, Session, select
from sqlalchemy import asc, desc
from typing import Any, List, Literal, TypeVar
from app.crud.base import BaseCrud, BId, BOptions


SModel = TypeVar("SModel", bound=SQLModel)
SCreate = TypeVar("SCreate", bound=SQLModel)
SUpdate = TypeVar("SUpdate", bound=SQLModel)


class SQLCrud(BaseCrud[SModel, SCreate, SUpdate]):

    def __init__(self, model: type[SModel]):
        self.model = model

    async def create(
        self, data: SCreate, session: Session, *args: Any, **kwargs: Any
    ) -> SModel:
        entity = self.model.model_validate(data)
        session.add(entity)
        session.commit()
        session.refresh(entity)
        return entity

    async def get(self, id: BId, session: Session) -> SModel | None:
        return session.get(self.model, id)

    async def list(self, options: BOptions, session: Session, *args: Any, **kwargs: Any) -> List[SModel]:
        page = options.get("page", 1)
        limit = options.get("limit", 100)
        order_by = options.get("order_by", "id")
        offset = (page - 1) * limit
        order: Literal["asc", "desc"] = options.get("order", "asc")
        column = getattr(self.model, order_by)
        # direction: int = -1 if order == "desc" else 1
        order_clause = desc(column) if order == "desc" else asc(column)
        return list(
            session.exec(
                select(self.model).order_by(order_clause).offset(offset).limit(limit)
            ).all()
        )

    async def update(self, id: BId, data: SUpdate, session: Session, *args: Any, **kwargs: Any) -> SModel | None:
        entity = session.get(self.model, id)
        if not entity:
            return None
        model_data = data.model_dump(exclude_unset=True)
        entity.sqlmodel_update(model_data)
        session.add(entity)
        session.commit()
        session.refresh(entity)
        return entity

    async def delete(self, id: BId, session: Session, *args: Any, **kwargs: Any) -> SModel | None:
        entity = await self.get(id, session=session)
        if not entity:
            return None
        session.delete(entity)
        session.commit()
        return entity
