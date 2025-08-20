from typing import Generator
from sqlalchemy import Engine
from sqlmodel import create_engine, SQLModel
from app.core.utils import CUSTOM_LOGGER, MAX_TRIES, WAIT_SECONDS
from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed
from app.core.config import get_config
from app.user.model.sql import *
from app.video.model.sql import *
import logging
from sqlalchemy import Engine
from sqlmodel import Session, select

config = get_config()


if config.DB_TYPE.is_sql:
    engine: Engine = create_engine(str(config.DB_URI))


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
        with Session(engine) as session:
            session.exec(select(1))
    except Exception as e:
        CUSTOM_LOGGER.error(e)
        raise e


def init_db():
    if not engine:
        return
    if not config.USE_MIGRATIONS:
        SQLModel.metadata.create_all(engine)
    # use alembic
    pass


def get_engine():
    return engine


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
