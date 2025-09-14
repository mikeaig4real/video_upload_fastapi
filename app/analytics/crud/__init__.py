from app.core.config import get_config

config = get_config()

# export crud based on db type from config
if config.IS_SQL:
    from app.analytics.crud.sql import crud
    from app.analytics.model.sql import AnalyticsUpdate, AnalyticsPublic, AnalyticsCreate  # type: ignore

    analytics_crud = crud
else:
    from app.analytics.crud.mongo import crud
    from app.analytics.model.mongo import AnalyticsUpdate, AnalyticsPublic, AnalyticsCreate  # type: ignore

    analytics_crud = crud
