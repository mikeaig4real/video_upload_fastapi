from contextlib import contextmanager
import logging
from typing import Any, Generator

from pymongo import MongoClient
from app.core.utils import make_custom_logger, MAX_TRIES, WAIT_SECONDS
from app.core.config import get_config
from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed
from pymongo.errors import ConnectionFailure
from odmantic import AIOEngine, SyncEngine
from motor import motor_asyncio, core
from pymongo.driver_info import DriverInfo

__version__ = "2023.11.10"
# make a custom logger for logging
CUSTOM_LOGGER = make_custom_logger(__name__)
config = get_config()

DRIVER_INFO = DriverInfo(str(config.PROJECT_NAME), version=__version__)


if not config.IS_SQL and config.DB_TYPE.is_mongo:
    # create mongo engines, clients
    client: motor_asyncio.AsyncIOMotorClient[Any] = motor_asyncio.AsyncIOMotorClient(
        str(config.DB_URI), driver=DRIVER_INFO
    )
    sync_client: MongoClient[Any] = MongoClient(str(config.DB_URI))
    db: core.AgnosticDatabase[Any] = client[str(config.DB_NAME)]
    engine = AIOEngine(client=client, database=str(config.DB_NAME))
    sync_engine = SyncEngine(client=sync_client, database=str(config.DB_NAME))

# retries db connection
@retry(
    stop=stop_after_attempt(MAX_TRIES),
    wait=wait_fixed(WAIT_SECONDS),
    before=before_log(CUSTOM_LOGGER, logging.INFO),
    after=after_log(CUSTOM_LOGGER, logging.WARN),
)
async def try_db():
    """
    Try to test connection with the designated mongo db at config
    """
    if not engine:
        return
    try:
        await db.command("ping")
    except ConnectionFailure as e:
        CUSTOM_LOGGER.error(e)
        raise e


def init_db():
    """
    Initialize mongo db connection
    """
    pass


def get_engine():
    """
    Get mongo db engine
    """
    return engine


def get_session() -> Generator[core.AgnosticDatabase[Any], None, None]:
    """
    Yields mongo db session
    """
    yield db

@contextmanager
def get_session_context() -> Generator[core.AgnosticDatabase[Any], None, None]:
    """
    Yields mongo db session using get_session, to be used outside app scope
    """
    yield from get_session()

def get_sync_engine():
    """
    Get mongo db sync engine
    """
    return sync_engine
