from app.core.config import get_config


config = get_config()

if config.IS_SQL:
        from app.db.connect.sql import try_db, init_db, get_engine, get_session, get_session_context # pyright: ignore[reportUnusedImport]
else:
    from app.db.connect.mongo import try_db, init_db, get_engine, get_session, get_session_context # pyright: ignore[reportUnusedImport]

