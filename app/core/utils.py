import logging
from typing import Any
from fastapi.routing import APIRoute

MAX_TRIES = 60 * 5  # 5 minutes
WAIT_SECONDS = 1
logging.basicConfig(level=logging.INFO)
CUSTOM_LOGGER = logging.getLogger(__name__)


def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0] if len(route.tags) > 0 else ''}-{route.name}"


def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v  # type: ignore
    raise ValueError(v)
