import threading
import time
from typing import Any, TypedDict
import cloudinary
import cloudinary.api
from app.core.config import UPLOAD_BUCKET_ENUM, get_config
from app.core.utils import CUSTOM_LOGGER
from app.uploader.crud.base import BaseUploader, UploadParams

config = get_config()

OptionsType = TypedDict(
    "OptionsType",
    {
        "public_id": str,
        "overwrite": bool,
        "timestamp": int,
        "eager": str,
        # "eager_async": bool,
    },
)

from typing import TypedDict, List


class DerivedResource(TypedDict):
    transformation: str
    transformation_signature: str
    format: str
    bytes: int
    id: str
    url: str
    secure_url: str
    extension: str


class CloudinaryResource(TypedDict):
    asset_id: str
    public_id: str
    format: str
    version: int
    resource_type: str
    type: str
    created_at: str
    bytes: int
    width: int
    height: int
    folder: str
    url: str
    secure_url: str
    next_cursor: str
    derived: List[DerivedResource]


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

    async def generate_params(
        self, *, asset_id: str, resource_type: str = "video", **kwargs: Any
    ) -> UploadParams:
        options: OptionsType = {
            "public_id": asset_id,
            "overwrite": True,
            "timestamp": int(time.time()),
            "eager": "c_fill,h_300,w_400/jpg",
            # "eager_async": False,  # uncomment to make upload fail
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

    async def get_resource(
        self, *, asset_id: str, resource_type: str = "video", **kwargs: Any
    ) -> CloudinaryResource | None:
        try:
            CUSTOM_LOGGER.info(f"Fetching Cloudinary resource {asset_id}")
            resource = cloudinary.api.resource(  # type: ignore
                asset_id,
                resource_type=resource_type,
            )
            return resource  # type: ignore
        except cloudinary.exceptions.NotFound as e:  # type: ignore
            # Cloudinary raises error if resource does not exist
            CUSTOM_LOGGER.warning(f"Asset with id {asset_id} not found")
            return None
        except Exception as e:
            CUSTOM_LOGGER.warning(
                f"Failed to retrieve Cloudinary resource {asset_id}: {e}"
            )
            return None
