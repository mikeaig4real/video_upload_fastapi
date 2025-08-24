from enum import Enum
from typing import Literal


class UPLOAD_STATUS_ENUM(Enum):
    IDLE = "idle"
    UPLOADING = "uploading"
    PROCESSING = "processing"
    COMPLETED = "completed"
    ERROR = "error"

VIDEO_LABEL = Literal["240p" , "360p" , "480p" , "720p" , "1080p" , "4K"]
