from typing import Any, List, cast
from fastapi import APIRouter, Request, status
from app.auth.utils import make_exception
from app.crud.base import BOptions
from app.models.filter import FilterOptionsType
from app.models.id import IDType
from app.models.success import SuccessModel
from app.responses import SuccessResponse
from app.video.crud import (
    video_crud,
    VideoPublic,
    VideoBase,  # pyright: ignore[reportUnusedImport]
    Video,  # pyright: ignore[reportUnusedImport]
)  # pyright: ignore[reportUnusedImport]
from app.db.deps import RequireSession
from app.core.rate_limiter import limiter

router = APIRouter(prefix="/library")

count_per_req = "10"

@router.get("/{id}", response_model=SuccessModel[VideoPublic])
@limiter.limit("50/minute")  # type: ignore
async def get(
    id: IDType, session: RequireSession, request: Request
):
    video = await video_crud.get(id=id, session=session)  # type: ignore
    if not video:
        raise make_exception(code=status.HTTP_404_NOT_FOUND, detail="Video not found")
    if not video.is_public:
        raise make_exception(code=status.HTTP_403_FORBIDDEN, detail="Video is not public")
    return SuccessResponse(video)


@router.get("/", response_model=SuccessModel[List[VideoPublic]])
@limiter.limit("100/minute")  # type: ignore
async def list(
    filters: FilterOptionsType,
    session: RequireSession,
    request: Request,
):

    options = cast(BOptions, filters.pagination_dict())
    public_only: dict[str, Any] = {
        **filters.video_filters_dict(),
        "is_public": True,
    }
    
    videos = await video_crud.list(
        options=options,
        filters=public_only,
        session=session,  # pyright: ignore[reportArgumentType]
    )
    return SuccessResponse(videos)
