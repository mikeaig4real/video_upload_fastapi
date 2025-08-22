from abc import ABC, abstractmethod
from typing import Dict, Any
from typing import TypedDict, Dict

from app.core.config import UPLOAD_BUCKET_ENUM

class UploadParams(TypedDict):
    upload_url: str
    fields: Dict[str, Any]
    asset_id: str
    upload_provider: UPLOAD_BUCKET_ENUM


class BaseUploader(ABC):
    @abstractmethod
    def generate_params(
        self, asset_id: str, resource_type: str = "video", *args: Any, **kwargs: Any
    ) -> UploadParams:
        pass
