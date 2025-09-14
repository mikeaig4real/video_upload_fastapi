from typing import Annotated

from pydantic import AfterValidator, HttpUrl, StringConstraints

from app.constants import URL_REGEX

# http url validators using pydantic or regex approach
HttpType = Annotated[HttpUrl, AfterValidator(str)]
HttpCheck = Annotated[
    str,
    StringConstraints(strip_whitespace=True, pattern=URL_REGEX),
]
