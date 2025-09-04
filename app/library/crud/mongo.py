# from typing import Any
# from fastapi.encoders import jsonable_encoder
# from app.auth.utils import hash_pass
# from app.crud.mongo import MONGOCrud
# from motor.core import AgnosticDatabase
# from app.user.model.mongo import (
#     User,
#     UserCreate,
#     UserUpdate,
#     UserBase,  # pyright: ignore[reportUnusedImport]
#     UserPublic,  # pyright: ignore[reportUnusedImport]
# )


# class UserCrud(MONGOCrud[User, UserCreate, UserUpdate]):

#     async def create(self, *, data: UserCreate, session: AgnosticDatabase[Any], **kwargs: Any) -> User:
#         entity_data = jsonable_encoder(data)
#         password = entity_data.pop("password")
#         entity_data["hashed_password"] = hash_pass(password)
#         entity = self.model(**entity_data)
#         return await self.engine.save(entity)  # type: ignore


# crud = UserCrud(User)
