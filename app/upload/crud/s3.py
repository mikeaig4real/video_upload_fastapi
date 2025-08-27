from app.core.config import UPLOAD_BUCKET_ENUM, get_config
from app.upload.crud.base import BaseUploader, UploadParams
from boto3 import client # pyright: ignore[reportUnknownVariableType]
config = get_config()

class S3Uploader(BaseUploader):
    def __init__(self):
        self.bucket = config.S3_CONFIG["bucket"]
        self.s3 = client("s3") # pyright: ignore[reportUnknownMemberType]

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
