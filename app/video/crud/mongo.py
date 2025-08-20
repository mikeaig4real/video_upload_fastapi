from typing import Any
from fastapi.encoders import jsonable_encoder
from odmantic import ObjectId
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

    async def create(self, data: VideoCreate, session: AgnosticDatabase[Any]) -> Video:
        entity_data = jsonable_encoder(data)
        user_id = ObjectId(entity_data.get("user_id"))
        user = await user_crud.get(id=user_id, session=session)
        if not user:
            raise ValueError("User not found")
        entity_data["user"] = User(**user.model_dump())
        entity_data["user_id"] = user_id
        entity = self.model(**entity_data)
        return await self.engine.save(entity)  # type: ignore


crud = VideoCrud(Video)
