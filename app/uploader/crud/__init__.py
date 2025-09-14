from app.core.config import get_config

config = get_config()
# export uploader crud based on config
if config.UPLOAD_STORAGE_TYPE.is_bucket and config.UPLOAD_BUCKET.is_cloudinary:
    from app.uploader.crud.cloudinary import CloudinaryUploader

    uploader_crud = CloudinaryUploader()
elif config.UPLOAD_STORAGE_TYPE.is_bucket and config.UPLOAD_BUCKET.is_s3:
    from app.uploader.crud.s3 import S3Uploader

    uploader_crud = S3Uploader()
