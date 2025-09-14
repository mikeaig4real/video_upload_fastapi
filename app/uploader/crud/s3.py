from typing import Any

import botocore
from app.core.config import UPLOAD_BUCKET_ENUM, get_config
from app.core.utils import make_custom_logger
from app.uploader.crud.base import BaseUploader, UploadParams
from boto3 import client # pyright: ignore[reportUnknownVariableType]
# make a custom logger for logging
CUSTOM_LOGGER = make_custom_logger(__name__)
config = get_config()

class S3Uploader(BaseUploader):
    """
    S3 class used to interact with s3 bucket
    """
    def __init__(self):
        self.bucket = config.S3_CONFIG["bucket"]
        self.s3 = client("s3") # type: ignore

    async def generate_params(
        self, *, asset_id: str, resource_type: str = "video", **kwargs: Any
    ) -> UploadParams:
        """
        Generates signed params to be used by the client to upload a resource to s3
        """
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

    async def get_resource(self, *, asset_id: str, **kwargs: Any) -> dict[str, Any] | None:
        try:
            """
            Retrieves resource info from s3 bucket
            """
            CUSTOM_LOGGER.info(f"Fetching S3 resource {asset_id}")
            response = self.s3.head_object( # type: ignore
                Bucket=self.bucket,
                Key=asset_id,
            )
            return response # type: ignore
        except self.s3.exceptions.NoSuchKey: # type: ignore
            raise FileNotFoundError(
                f"S3 object {asset_id} not found in bucket {self.bucket}"
            )
        except botocore.exceptions.ClientError as e: # type: ignore
            if e.response["Error"]["Code"] == "404": # type: ignore
                CUSTOM_LOGGER.info(
                    f"S3 object {asset_id} not found in bucket {self.bucket}"
                )
            CUSTOM_LOGGER.error(f"Failed to fetch S3 object {asset_id}: {e}")
            return None
