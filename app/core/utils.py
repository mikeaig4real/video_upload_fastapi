import logging
from typing import Any
from fastapi.routing import APIRoute

MAX_TRIES = 60 * 5  # 5 minutes
WAIT_SECONDS = 1
logging.basicConfig(level=logging.INFO)
CUSTOM_LOGGER = logging.getLogger(__name__)


def make_custom_logger(name: str):
    """
    Creates a custom logger by given name
    """
    logger = logging.getLogger(name)
    if not logger.handlers:  # avoid duplicate handlers
        handler = logging.StreamHandler()
        handler.setFormatter(
            logging.Formatter("%(asctime)s [%(name)s] %(levelname)s: %(message)s")
        )
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger


def custom_generate_unique_id(route: APIRoute) -> str:
    """
    Generates and returns a unique id
    """
    return f"{route.tags[0] if len(route.tags) > 0 else ''}-{route.name}"


def parse_cors(v: Any) -> list[str] | str:
    """
    Creates or returns a list url hosts to be allowed with cors
    """
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v  # type: ignore
    raise ValueError(v)
