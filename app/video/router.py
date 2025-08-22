from typing import List
from fastapi import APIRouter
from app.auth.deps import RequireCurrentUser
from app.models.filter import FilterType
from app.models.id import IDType
from app.models.success import SuccessModel
from app.responses import SuccessResponse
from app.video.crud import video_crud, VideoUpdate, VideoPublic, VideoCreate, VideoBase, Video # pyright: ignore[reportUnusedImport]
from app.db.deps import RequireSession

router = APIRouter(prefix="/video")


@router.post("/", response_model=SuccessModel[VideoPublic])
async def create(
    video: VideoCreate, session: RequireSession, current_user: RequireCurrentUser
):
    video = await video_crud.create(data=video, user_id=current_user.id, session=session)  # type: ignore
    return SuccessResponse(video)


@router.get("/{id}", response_model=SuccessModel[VideoPublic])
async def get(id: IDType, session: RequireSession, current_user: RequireCurrentUser):
    video = await video_crud.get(id=id, session=session)  # type: ignore
    return video


@router.get("/", response_model=SuccessModel[List[VideoPublic]])
async def list(
    options: FilterType, session: RequireSession, current_user: RequireCurrentUser
):
    videos = await video_crud.list(options=options.model_dump(), session=session)  # type: ignore
    return videos


@router.patch("/{id}", response_model=SuccessModel[VideoPublic])
async def update(
    id: IDType,
    update: VideoUpdate,
    session: RequireSession,
    current_user: RequireCurrentUser,
):
    video = await video_crud.update(id=id, data=update, session=session)  # type: ignore
    return video


@router.delete("/{id}", response_model=SuccessModel[VideoPublic])
async def delete(id: IDType, session: RequireSession, current_user: RequireCurrentUser):
    video = await video_crud.delete(id=id, session=session)  # type: ignore
    return video
