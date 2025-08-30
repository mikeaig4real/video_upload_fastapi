from app.core.config import get_config

config = get_config()


if config.IS_SQL:
    from app.upload.crud.sql import crud
    from app.upload.model.sql import Upload, UploadPublic, UploadUpdate, UploadCreate  # type: ignore

    upload_crud = crud
else:
    from app.upload.crud.mongo import crud
    from app.upload.model.mongo import Upload, UploadPublic, UploadUpdate, UploadCreate  # type: ignore

    upload_crud = crud
