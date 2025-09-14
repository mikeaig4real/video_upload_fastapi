from app.core.config import get_config

config = get_config()

# export models based on db type from config
if config.IS_SQL:
    from app.analytics.model.sql import  AnalyticsBase, Analytics, AnalyticsPublic, AnalyticsCreate, AnalyticsUpdate # pyright: ignore[reportUnusedImport]
else:
    from app.analytics.model.mongo import AnalyticsBase, Analytics, AnalyticsPublic, AnalyticsCreate, AnalyticsUpdate # pyright: ignore[reportUnusedImport]
