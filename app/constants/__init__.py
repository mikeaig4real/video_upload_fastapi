from enum import Enum
from typing import Dict
from typing import Any

VIDEO_FORMAT_REGEX = r"^(video\/\w+)$"

URL_REGEX = r"^(https?:\/\/)([\w.-]+)(\.[a-zA-Z]{2,})(:[0-9]+)?(\/.*)?$"

ResponseType = dict[str, str | bool | Dict[str, Any]]

SUCCESS_RESPONSE: ResponseType = {"success": True, "data": {}}
ERROR_RESPONSE: ResponseType = {"success": False, "description": ""}
NOTFOUND_RESPONSE: ResponseType = ERROR_RESPONSE | {"description": "Unknown request or entity"}
CLIENTERROR_RESPONSE: ResponseType = ERROR_RESPONSE | {"description": "Request error"}
SERVERERROR_RESPONSE: ResponseType = ERROR_RESPONSE | {"description": "Internal server error"}
UNAUTHORIZED_RESPONSE: ResponseType = ERROR_RESPONSE | {"description": "Unauthorized access"}

class ENTITY_NAMES(Enum):
    USER = "user"
    VIDEO = "video"
