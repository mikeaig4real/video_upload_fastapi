from abc import ABC, abstractmethod
from typing import Dict, Any
from typing import TypedDict, Dict

from app.core.config import UPLOAD_BUCKET_ENUM, get_config

config = get_config()

class UploadParams(TypedDict):
    upload_url: str
    fields: Dict[str, Any]
    asset_id: str
    upload_provider: UPLOAD_BUCKET_ENUM


class BaseUploader(ABC):
    """
    Base (abstract) class for bucket crud specific methods
    """
    @abstractmethod
    async def generate_params(
        self, * , asset_id: str, resource_type: str = "video", **kwargs: Any
    ) -> UploadParams: ...
    async def get_resource(
        self, * , asset_id: str, resource_type: str = "video", **kwargs: Any
    ) -> Any: ...
