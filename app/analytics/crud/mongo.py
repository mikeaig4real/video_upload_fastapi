from app.crud.mongo import MONGOCrud
from app.analytics.model.mongo import (
    Analytics,
    AnalyticsCreate,
    AnalyticsUpdate,  # pyright: ignore[reportUnusedImport]
)


class AnalyticsCrud(MONGOCrud[Analytics, AnalyticsCreate, AnalyticsUpdate]):
    """
    Analytics Crud Class that handles mongo specific analytics crud implementations
    """
    pass


crud = AnalyticsCrud(Analytics)
