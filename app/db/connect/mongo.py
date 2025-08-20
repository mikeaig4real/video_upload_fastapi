import logging
from typing import Any, Generator

from pymongo import MongoClient
from app.core.utils import CUSTOM_LOGGER, MAX_TRIES, WAIT_SECONDS
from app.core.config import get_config
from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed
from pymongo.errors import ConnectionFailure
from odmantic import AIOEngine, SyncEngine
from motor import motor_asyncio, core
from pymongo.driver_info import DriverInfo

__version__ = "2023.11.10"

config = get_config()

DRIVER_INFO = DriverInfo(str(config.PROJECT_NAME), version=__version__)


if not config.IS_SQL and config.DB_TYPE.is_mongo:
    client: motor_asyncio.AsyncIOMotorClient[Any] = motor_asyncio.AsyncIOMotorClient(
        str(config.DB_URI), driver=DRIVER_INFO
    )
    sync_client: MongoClient[Any] = MongoClient(str(config.DB_URI))
    db: core.AgnosticDatabase[Any] = client[str(config.DB_NAME)]
    engine = AIOEngine(client=client, database=str(config.DB_NAME))
    sync_engine = SyncEngine(client=sync_client, database=str(config.DB_NAME))


@retry(
    stop=stop_after_attempt(MAX_TRIES),
    wait=wait_fixed(WAIT_SECONDS),
    before=before_log(CUSTOM_LOGGER, logging.INFO),
    after=after_log(CUSTOM_LOGGER, logging.WARN),
)
async def try_db():
    if not engine:
        return
    try:
        await db.command("ping")
    except ConnectionFailure as e:
        CUSTOM_LOGGER.error(e)
        raise e


def init_db():
    pass


def get_engine():
    return engine


def get_session() -> Generator[core.AgnosticDatabase[Any], None, None]:
    yield db
    
    
def get_sync_engine():
    return sync_engine
