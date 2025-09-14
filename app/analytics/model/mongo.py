from pydantic import BaseModel
from odmantic import Model


class AnalyticsBase(BaseModel):
    pass


class Analytics(Model):
    pass


class AnalyticsCreate(AnalyticsBase):
    pass


class AnalyticsPublic(AnalyticsBase):
    pass


class AnalyticsUpdate(BaseModel):
    pass
