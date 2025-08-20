from fastapi.responses import JSONResponse

from app.constants import (
    CLIENTERROR_RESPONSE,
    ERROR_RESPONSE,
    NOTFOUND_RESPONSE,
    SERVERERROR_RESPONSE,
    UNAUTHORIZED_RESPONSE,
)
from app.core.utils import CUSTOM_LOGGER


class ErrorResponse(JSONResponse):
    code = 500
    response = ERROR_RESPONSE

    def __init__(self, description: str | None = "") -> None:
        if description:
            self.response["description"] = str(description)
        CUSTOM_LOGGER.error(self.response)
        super().__init__(self.response, status_code=self.code)


class Error(ErrorResponse):
    code = 400
    response = CLIENTERROR_RESPONSE


class NotFound(ErrorResponse):
    code = 404
    response = NOTFOUND_RESPONSE


class ServerError(ErrorResponse):
    code = 500
    response = SERVERERROR_RESPONSE


class Unauthorized(ErrorResponse):
    code = 401
    response = UNAUTHORIZED_RESPONSE
