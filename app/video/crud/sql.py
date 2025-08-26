from sqlmodel import Session
from app.crud.base import BId
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
    
    async def upsert(
        self, id: BId, data: VideoCreate, session: Session, user_id: int
    ) -> Video:
        if id is None:
            return await self.create(data=data, session=session, user_id=user_id)
        return await super().upsert(id=id, data=data, session=session)


crud = VideoCrud(Video)
