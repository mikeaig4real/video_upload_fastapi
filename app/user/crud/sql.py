from typing import Any
from fastapi.encoders import jsonable_encoder
from sqlmodel import Session
from app.auth.utils import hash_pass
from app.crud.sql import SQLCrud
from app.user.model.sql import User, UserCreate, UserUpdate # pyright: ignore[reportUnusedImport]


class UserCrud(SQLCrud[User, UserCreate, UserUpdate]):
    """
    User Crud Class that handles sql specific user crud implementations
    """
    async def create(self, *, data: UserCreate, session: Session, **kwargs: Any) -> User:
        entity_data = jsonable_encoder(data)
        password = entity_data.pop("password")
        entity_data["hashed_password"] = hash_pass(plain_pass=password)
        entity = self.model.model_validate(entity_data)
        session.add(entity)
        session.commit()
        session.refresh(entity)
        return entity


crud = UserCrud(User)
