from app.core.config import get_config


config = get_config()


def connect():
    if config.IS_SQL:
        from app.db.connect.sql import try_db, init_db, get_engine, get_session

        return try_db, init_db, get_engine, get_session

    from app.db.connect.mongo import try_db, init_db, get_engine, get_session

    return try_db, init_db, get_engine, get_session
