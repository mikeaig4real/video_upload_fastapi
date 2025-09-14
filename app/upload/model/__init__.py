from app.core.config import get_config

config = get_config()
# export upload models based on config
if config.IS_SQL:
    from app.upload.model.sql import  UploadBase, Upload, UploadCreate, UploadUpdate # pyright: ignore[reportUnusedImport]
else:
    from app.upload.model.mongo import UploadBase, Upload, UploadCreate, UploadUpdate # pyright: ignore[reportUnusedImport]

