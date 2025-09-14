from app.core.config import get_config

config = get_config()

# export video crud based on config
if config.IS_SQL:
    from app.video.crud.sql import crud
    from app.video.model.sql import VideoUpdate, VideoPublic, VideoCreate, VideoBase, Video # pyright: ignore[reportUnusedImport]
    
    video_crud = crud
else:
    from app.video.crud.mongo import crud
    from app.video.model.mongo import VideoUpdate, VideoPublic, VideoCreate, VideoBase, Video # pyright: ignore[reportUnusedImport]

    video_crud = crud
