from sqlmodel import Session
from app.crud.sql import SQLCrud
from app.video.model.sql import (
    VideoBase,  # pyright: ignore[reportUnusedImport]
    Video,
    VideoCreate,
    VideoUpdate,
    VideoPublic,  # pyright: ignore[reportUnusedImport]
)


class VideoCrud(SQLCrud[Video, VideoCreate, VideoUpdate]):

    async def create(
        self, data: VideoCreate, session: Session, user_id: int
    ) -> Video:
        entity = self.model.model_validate(data)
        entity.user_id = user_id
        session.add(entity)
        session.commit()
        session.refresh(entity)
        return entity


crud = VideoCrud(Video)
