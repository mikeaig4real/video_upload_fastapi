from app.core.config import get_config

config = get_config()


def get_video_model():
    if config.IS_SQL:
        # sql
        from app.video.model.sql import (
            VideoBase,
            Video,
            VideoPublic,
            VideoCreate,
            VideoUpdate,
        )

        return VideoBase, Video, VideoPublic, VideoCreate, VideoUpdate

    # mongo
    from app.video.model.mongo import (
        VideoBase,
        Video,
        VideoPublic,
        VideoCreate,
        VideoUpdate,
    )

    return VideoBase, Video, VideoPublic, VideoCreate, VideoUpdate
