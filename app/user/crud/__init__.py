from app.core.config import get_config

config = get_config()

# export user crud based on config
if config.IS_SQL:
    from app.user.crud.sql import crud
    from app.user.model.sql import UserUpdate, UserPublic, UserCreate  # type: ignore

    user_crud = crud
else:
    from app.user.crud.mongo import crud
    from app.user.model.mongo import UserUpdate, UserPublic, UserCreate  # type: ignore

    user_crud = crud
