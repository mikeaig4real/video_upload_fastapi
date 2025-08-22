from app.core.config import UPLOAD_BUCKET_ENUM, get_config
from app.upload.crud.base import BaseUploader, UploadParams
from boto3 import client # type: ignore
config = get_config()

class S3Uploader(BaseUploader):
    def __init__(self):
        self.bucket = config.UPLOAD_BUCKET.name
        self.s3 = client("s3") # type: ignore

    def generate_params(
        self, asset_id: str, resource_type: str = "video"
    ) -> UploadParams:
        presigned = self.s3.generate_presigned_post( # type: ignore
            Bucket=self.bucket,
            Key=asset_id,
            Fields={"acl": "public-read"},
            Conditions=[{"acl": "public-read"}],
            ExpiresIn=3600,
        )
        return {
            "upload_url": presigned["url"],
            "fields": presigned["fields"],
            "asset_id": asset_id,
            "upload_provider": UPLOAD_BUCKET_ENUM.S3,
        }
