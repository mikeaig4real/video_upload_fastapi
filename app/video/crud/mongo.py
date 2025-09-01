from typing import Any, cast
from fastapi.encoders import jsonable_encoder
from app.crud.mongo import MONGOCrud
from motor.core import AgnosticDatabase
from app.user.crud.mongo import User
from app.video.model.mongo import (
    Video,
    VideoCreate,
    VideoUpdate,
    VideoBase,  # pyright: ignore[reportUnusedImport]
    VideoPublic,  # pyright: ignore[reportUnusedImport]
)


class VideoCrud(MONGOCrud[Video, VideoCreate, VideoUpdate]):

    async def upsert(
        self, *, field: str, value: Any, data: VideoCreate, session: AgnosticDatabase[Any], user: User, **kwargs: Any
    ) -> Video:
        entity_data = jsonable_encoder(data)
        entity_data["user"] = user
        entity_data["user_id"] = user.id
        entity = self.model(**entity_data)
        return await super().upsert(
            field=field, value=value, data=cast(VideoCreate, entity), session=session
        )


crud = VideoCrud(Video)
