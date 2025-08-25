import threading
import time
from typing import TypedDict
import cloudinary
from app.core.config import UPLOAD_BUCKET_ENUM, get_config
from app.upload.crud.base import BaseUploader, UploadParams

config = get_config()

OptionsType = TypedDict(
    "OptionsType",
    {
        "public_id": str,
        "overwrite": bool,
        "timestamp": int,
        "eager": str,
    },
)


class CloudinaryUploader(BaseUploader):
    _has_init: bool = False
    _lock = threading.Lock()

    def __new__(cls):
        if not cls._has_init:
            with cls._lock:
                if not cls._has_init:
                    cloudinary.config(  # type: ignore
                        cloud_name=config.CLOUDINARY_CONFIG["cloud_name"],
                        api_key=config.CLOUDINARY_CONFIG["api_key"],
                        api_secret=config.CLOUDINARY_CONFIG["api_secret"],
                    )
                    cls._has_init = True
        return super().__new__(cls)

    def generate_params(
        self, asset_id: str, resource_type: str = "video"
    ) -> UploadParams:
        options: OptionsType = {
            "public_id": asset_id,
            "overwrite": True,
            "timestamp": int(time.time()),
            "eager": "c_fill,h_300,w_400/jpg",
            # "eager_async": False, uncomment to make upload fail
        }

        signature_data = cloudinary.utils.api_sign_request(options, api_secret=config.CLOUDINARY_CONFIG["api_secret"])  # type: ignore

        return {
            "upload_url": f"https://api.cloudinary.com/v1_1/{config.CLOUDINARY_CONFIG['cloud_name']}/{resource_type}/upload",
            "fields": {
                **options,
                "signature": signature_data,
                "api_key": config.CLOUDINARY_CONFIG["api_key"],
            },
            "asset_id": asset_id,
            "upload_provider": UPLOAD_BUCKET_ENUM.CLOUDINARY,
        }
