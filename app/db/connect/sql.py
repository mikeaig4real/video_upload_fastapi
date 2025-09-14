from contextlib import contextmanager
from typing import Generator
from sqlalchemy import Engine
from sqlmodel import create_engine, SQLModel
from app.core.utils import make_custom_logger, MAX_TRIES, WAIT_SECONDS
from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed
from app.core.config import get_config
from app.user.model.sql import *
from app.video.model.sql import *
from app.upload.model.sql import *
import logging
from sqlalchemy import Engine
from sqlmodel import Session, select
# make a custom logger for logging
CUSTOM_LOGGER = make_custom_logger(__name__)
config = get_config()


if config.DB_TYPE.is_sql:
    # create sql engine
    engine: Engine = create_engine(str(config.DB_URI))

# retries db connection
@retry(
    stop=stop_after_attempt(MAX_TRIES),
    wait=wait_fixed(WAIT_SECONDS),
    before=before_log(CUSTOM_LOGGER, logging.INFO),
    after=after_log(CUSTOM_LOGGER, logging.WARN),
)
async def try_db():
    """
    Try to test connection with the designated sql db at config
    """
    if not engine:
        return
    try:
        with Session(engine) as session:
            # Try to create session to check if DB is awake
            session.exec(select(1))
    except Exception as e:
        CUSTOM_LOGGER.error(e)
        raise e


def init_db():
    """
    Initialize sql db connection
    """
    if not engine:
        return
    if not config.USE_MIGRATIONS:
        SQLModel.metadata.create_all(engine)
    # use alembic
    pass

def get_engine():
    """
    Get sql db engine
    """
    return engine


def get_session() -> Generator[Session, None, None]:
    """
    Yields sql db session
    """
    with Session(engine) as session:
        yield session

@contextmanager
def get_session_context() -> Generator[Session, None, None]:
    """
    Yields sql db session using get_session, to be used outside app scope
    """
    yield from get_session()
