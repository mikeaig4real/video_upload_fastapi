from typing import Any
from fastapi.encoders import jsonable_encoder
from odmantic import ObjectId
from app.crud.base import BId
from app.crud.mongo import MONGOCrud
from motor.core import AgnosticDatabase
from app.user.crud.mongo import User, crud as user_crud
from app.video.model.mongo import (
    Video,
    VideoCreate,
    VideoUpdate,
    VideoBase,  # pyright: ignore[reportUnusedImport]
    VideoPublic,  # pyright: ignore[reportUnusedImport]
)


class VideoCrud(MONGOCrud[Video, VideoCreate, VideoUpdate]):

    async def create(
        self, *, data: VideoCreate, session: AgnosticDatabase[Any], user_id: ObjectId, **kwargs: Any
    ) -> Video:
        entity_data = jsonable_encoder(data)
        user_id = ObjectId(user_id)
        user = await user_crud.get(id=user_id, session=session)
        if not user:
            raise ValueError("User not found")
        entity_data["user"] = User(**user.model_dump())
        entity_data["user_id"] = user_id
        entity = self.model(**entity_data)
        return await self.engine.save(entity)  # type: ignore
    
    async def upsert(
        self, *, id: BId, data: VideoCreate, session: AgnosticDatabase[Any], user_id: ObjectId, **kwargs: Any
    ) -> Video:
        if id is None:
            return await self.create(data=data, session=session, user_id=user_id)
        return await super().upsert(id=id, data=data, session=session)


crud = VideoCrud(Video)
