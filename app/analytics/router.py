from fastapi import APIRouter, Request
from app.auth.deps import RequireCurrentUser
from app.models.success import SuccessModel
from app.analytics.crud import AnalyticsUpdate, AnalyticsPublic
from app.db.deps import RequireSession
from app.core.rate_limiter import limiter

router = APIRouter(prefix="/analytics")

# set the number of requests to be made per minute
count_per_req = "50"

@router.get("/", response_model=SuccessModel[AnalyticsPublic])
@limiter.limit(f"{count_per_req}/minute") # type: ignore
async def get(session: RequireSession, current_user: RequireCurrentUser, request: Request):
    """
    Retrieve the analytics for a video for a user
    """
    pass


@router.patch("/", response_model=SuccessModel[AnalyticsPublic])
@limiter.limit(f"{count_per_req}/minute") # type: ignore
async def update(update: AnalyticsUpdate, session: RequireSession, current_user: RequireCurrentUser, request: Request):
    """
    Update the analytics for a video for a user
    """
    pass


@router.delete("/", response_model=SuccessModel[AnalyticsPublic])
@limiter.limit(f"{count_per_req}/minute") # type: ignore
async def delete(session: RequireSession, current_user: RequireCurrentUser, request: Request):
    """
    Delete the analytics for a video for a user ?
    """
    pass
