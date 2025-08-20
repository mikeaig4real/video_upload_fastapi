from app.crud.sql import SQLCrud
from app.video.model.sql import (
    VideoBase,
    Video,
    VideoCreate,
    VideoUpdate,
    VideoPublic,  # pyright: ignore[reportUnusedImport]
)


class VideoCrud(SQLCrud[VideoBase, VideoCreate, VideoUpdate]):
    pass


crud = VideoCrud(Video)
