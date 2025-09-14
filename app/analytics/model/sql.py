from sqlmodel import SQLModel



class AnalyticsBase(SQLModel):
    pass


class Analytics(AnalyticsBase, table=True):
    pass


class AnalyticsCreate(AnalyticsBase):
    pass


class AnalyticsPublic(AnalyticsBase):
    pass


class AnalyticsUpdate(SQLModel):
    pass
