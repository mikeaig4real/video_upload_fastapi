from app.crud.sql import SQLCrud
from app.upload.model.sql import Upload, UploadCreate, UploadUpdate, UploadPublic # pyright: ignore[reportUnusedImport]


class UploadCrud(SQLCrud[Upload, UploadCreate, UploadUpdate]):
    """
    Upload Crud Class that handles sql specific upload crud implementations
    """
    pass


crud = UploadCrud(Upload)
