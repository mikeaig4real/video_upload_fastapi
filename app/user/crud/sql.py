from fastapi.encoders import jsonable_encoder
from pydantic import EmailStr
from sqlmodel import Session, select
from app.auth.utils import hash_pass
from app.crud.sql import SQLCrud
from app.user.model.sql import User, UserCreate, UserUpdate, UserPublic, UserBase # pyright: ignore[reportUnusedImport]


class UserCrud(SQLCrud[User, UserCreate, UserUpdate]):
    async def find_by_email(self, email: EmailStr, session: Session) -> User | None:
        statement = select(User).where(User.email == email)
        user = session.exec(statement).first()
        return user

    async def create(self, data: UserCreate, session: Session) -> User:
        entity_data = jsonable_encoder(data)
        password = entity_data.pop("password")
        entity_data["hashed_password"] = hash_pass(plain_pass=password)
        entity = self.model.model_validate(entity_data)
        session.add(entity)
        session.commit()
        session.refresh(entity)
        return entity


crud = UserCrud(User)
