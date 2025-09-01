from sqlmodel import SQLModel, Session, select
from sqlalchemy import asc, desc
from typing import Any, TypeVar
from app.crud.base import BaseCrud, BId, BOptions


SModel = TypeVar("SModel", bound=SQLModel)
SCreate = TypeVar("SCreate", bound=SQLModel)
SUpdate = TypeVar("SUpdate", bound=SQLModel)


# todo: repetitions happening, will refactor later
class SQLCrud(BaseCrud[SModel, SCreate, SUpdate]):

    def __init__(self, model: type[SModel]):
        self.model = model

    async def create(
        self, *, data: SCreate, session: Session, **kwargs: Any
    ) -> SModel:
        entity = self.model.model_validate(data)
        session.add(entity)
        session.commit()
        session.refresh(entity)
        return entity

    async def get(self, *, id: BId, session: Session, **kwargs: Any) -> SModel | None:
        if id is None:
            return None
        return session.get(self.model, id)

    async def get_by(
        self,
        *,
        field: str | None,
        value: Any,
        many: bool = False,
        session: Session,
        **kwargs: Any,
    ) -> SModel | list[SModel] | None:
        if field is None:
            raise ValueError("Field name must be provided")
        column = getattr(self.model, field, None)
        if column is None:
            raise ValueError(f"Invalid field name: {field}")
        if many:
            return list(session.exec(select(self.model).where(column == value)).all())
        return session.exec(select(self.model).where(column == value)).first()

    async def list(
        self,
        *,
        options: BOptions,
        session: Session,
        filters: dict[str, Any] = {},
        **kwargs: Any,
    ) -> list[SModel]:
        page = options.get("page")
        if page is None:
            page = 1
        limit = options.get("limit")
        if limit is None:
            limit = 100
        order_by = options.get("order_by")
        if order_by is None:
            order_by = "id"
        offset = (page - 1) * limit
        order = options.get("order")
        if order is None:
            order = "asc"
        column = getattr(self.model, order_by)
        # direction: int = -1 if order == "desc" else 1
        order_clause = desc(column) if order == "desc" else asc(column)
        query = select(self.model)
        for field, value in filters.items():
            model_field = getattr(self.model, field, None)
            if model_field is not None and value is not None:
                query = query.where(model_field == value)
        return list(
            session.exec(
                query.order_by(order_clause).offset(offset).limit(limit)
            ).all()
        )

    async def update(
        self, *, id: BId, data: SUpdate, session: Session, **kwargs: Any
    ) -> SModel | None:
        entity = await self.get(id=id, session=session)
        if not entity:
            return None
        model_data = data.model_dump(exclude_unset=True)
        entity.sqlmodel_update(model_data)
        session.add(entity)
        session.commit()
        session.refresh(entity)
        return entity

    async def upsert(
        self,
        field: str,
        value: Any,
        data: SCreate,
        session: Session,
        *args: Any,
        **kwargs: Any,
    ) -> SModel:
        entity = await self.get_by(field=field, value=value, session=session)

        if not entity:
            setattr(data, field, value)
            return await self.create(data=data, session=session)
        
        if isinstance(entity, list):
            entity = entity[0]
        
        model_data = data.model_dump(exclude_unset=True)
        entity.sqlmodel_update(model_data)
        session.add(entity)
        session.commit()
        session.refresh(entity)
        return entity

    async def delete(
        self, *, id: BId, session: Session, **kwargs: Any
    ) -> SModel | None:
        entity = await self.get(id=id, session=session)
        if not entity:
            return None
        session.delete(entity)
        session.commit()
        return entity
