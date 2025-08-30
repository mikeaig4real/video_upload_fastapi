from app.crud.mongo import MONGOCrud
from app.upload.model.mongo import (
    Upload,
    UploadCreate,
    UploadUpdate,  # pyright: ignore[reportUnusedImport]
    UploadPublic,  # pyright: ignore[reportUnusedImport]
)


class UploadCrud(MONGOCrud[Upload, UploadCreate, UploadUpdate]):
    pass


crud = UploadCrud(Upload)
