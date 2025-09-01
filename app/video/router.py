from typing import Any, List, cast
from fastapi import APIRouter, Request, status
from app.auth.deps import RequireCurrentUser
from app.auth.utils import make_exception
from app.crud.base import BOptions
from app.models.filter import FilterOptionsType
from app.models.id import IDType
from app.models.success import SuccessModel
from app.responses import SuccessResponse
from app.video.crud import (
    video_crud,
    VideoUpdate,
    VideoPublic,
    VideoCreate,
    VideoBase, # pyright: ignore[reportUnusedImport]
    Video, # pyright: ignore[reportUnusedImport]
)  # pyright: ignore[reportUnusedImport]
from app.db.deps import RequireSession
from app.core.rate_limiter import limiter

router = APIRouter(prefix="/video")


@router.put("/", response_model=SuccessModel[VideoPublic])
@limiter.limit("3/minute") # type: ignore
async def create(
    video: VideoCreate, session: RequireSession, current_user: RequireCurrentUser, request: Request
):
    video = await video_crud.upsert(field="upload_hash", value=video.upload_hash, data=video, user=current_user, session=session)  # type: ignore
    return SuccessResponse(video)


@router.get("/{id}", response_model=SuccessModel[VideoPublic])
@limiter.limit("50/minute")  # type: ignore
async def get(id: IDType, session: RequireSession, _: RequireCurrentUser, request: Request):
    video = await video_crud.get(id=id, session=session)  # type: ignore
    if not video:
        raise make_exception(code=status.HTTP_404_NOT_FOUND, detail="Video not found")
    return SuccessResponse(video)


@router.get("/", response_model=SuccessModel[List[VideoPublic]])
@limiter.limit("100/minute")  # type: ignore
async def list(
    filters: FilterOptionsType,
    session: RequireSession,
    current_user: RequireCurrentUser,
    request: Request
):

    options = cast(BOptions, filters.pagination_dict())
    filters_with_user: dict[str, Any] = {
        "user_id": current_user.id,
        **filters.video_filters_dict(),
    }

    videos = await video_crud.list(
        options=options,
        filters=filters_with_user,
        session=session,  # pyright: ignore[reportArgumentType]
    )
    return SuccessResponse(videos)


@limiter.limit("10/minute")  # type: ignore
@router.patch("/{id}", response_model=SuccessModel[VideoPublic])
async def update(
    id: IDType,
    update: VideoUpdate,
    session: RequireSession,
    _: RequireCurrentUser,
    request: Request
):
    video = await video_crud.update(id=id, data=update, session=session)  # type: ignore
    if not video:
        raise make_exception(code=status.HTTP_404_NOT_FOUND, detail="Video not found")
    return SuccessResponse(video)


@limiter.limit("5/minute")  # type: ignore
@router.delete("/{id}", response_model=SuccessModel[VideoPublic])
async def delete(id: IDType, session: RequireSession, _: RequireCurrentUser, request: Request):
    video = await video_crud.delete(id=id, session=session)  # type: ignore
    if not video:
        raise make_exception(code=status.HTTP_404_NOT_FOUND, detail="Video not found")
    return SuccessResponse(video)
