from app.core.config import get_config

config = get_config()

if config.IS_SQL:
    from app.user.model.sql import  UserBase, User, UserPublic, UserCreate, UserUpdate # pyright: ignore[reportUnusedImport]
else:
    from app.user.model.mongo import UserBase, User, UserPublic, UserCreate, UserUpdate # pyright: ignore[reportUnusedImport]

