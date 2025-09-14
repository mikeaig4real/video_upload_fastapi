from app.crud.sql import SQLCrud
from app.analytics.model.sql import (
    Analytics,
    AnalyticsCreate,
    AnalyticsUpdate,
)  # pyright: ignore[reportUnusedImport]


class AnalyticsCrud(SQLCrud[Analytics, AnalyticsCreate, AnalyticsUpdate]):
    """
    Analytics Crud Class that handles sql specific analytics crud implementations
    """

    pass


crud = AnalyticsCrud(Analytics)
