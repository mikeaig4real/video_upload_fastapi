from typing import Any, cast
from sqlmodel import Session
from app.crud.sql import SQLCrud
from app.user.model.sql import User
from app.video.model.sql import (
    VideoBase,  # pyright: ignore[reportUnusedImport]
    Video,
    VideoCreate,
    VideoUpdate,
    VideoPublic,  # pyright: ignore[reportUnusedImport]
)


class VideoCrud(SQLCrud[Video, VideoCreate, VideoUpdate]):
    """
    Video Crud Class that handles sql specific video crud implementations
    """
    async def upsert(
        self, field: str, value: Any, data: VideoCreate, session: Session, user: User
    ) -> Video:
        entity = self.model.model_validate(data)
        entity.user_id = cast(int, user.id)
        return await super().upsert(
            field=field, value=value, data=cast(VideoCreate, entity), session=session
        )


crud = VideoCrud(Video)
