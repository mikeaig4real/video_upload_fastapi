from enum import Enum

class UPLOAD_STATUS_ENUM(str, Enum):
    IDLE = "idle"
    UPLOADING = "uploading"
    PROCESSING = "processing"
    COMPLETED = "completed"
    ERROR = "error"


class VIDEO_LABEL_ENUM(str, Enum):
    P240 = "240p"
    P360 = "360p"
    P480 = "480p"
    P720 = "720p"
    P1080 = "1080p"
    P4K = "4K"
