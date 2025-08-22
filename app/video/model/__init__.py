from app.core.config import get_config

config = get_config()


if config.IS_SQL:
    from app.video.model.sql import (
        VideoBase,  # pyright: ignore[reportUnusedImport]
        Video,  # pyright: ignore[reportUnusedImport]
        VideoPublic,  # pyright: ignore[reportUnusedImport]
        VideoCreate,  # pyright: ignore[reportUnusedImport]
        VideoUpdate,  # pyright: ignore[reportUnusedImport]
    )
else:
    from app.video.model.mongo import (
        VideoBase,  # pyright: ignore[reportUnusedImport]
        Video,  # pyright: ignore[reportUnusedImport]
        VideoPublic,  # pyright: ignore[reportUnusedImport]
        VideoCreate,  # pyright: ignore[reportUnusedImport]
        VideoUpdate,  # pyright: ignore[reportUnusedImport]
    )
