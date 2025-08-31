from typing import Any, List
from fastapi import APIRouter, Request, status
from app.auth.deps import RequireCurrentUser
from app.auth.utils import make_exception
from app.models.filter import FilterOptionsType
from app.models.id import IDType
from app.models.success import SuccessModel
from app.models.video import UPLOAD_STATUS_ENUM
from app.responses import SuccessResponse
from app.uploader.model import (
    UploadType,
    UploadPublic,
)  # pyright: ignore[reportUnusedImport]
from app.uploader.crud import uploader_crud
from app.upload.crud import upload_crud, UploadCreate
from app.db.deps import RequireSession
from app.video.crud import video_crud
from app.core.rate_limiter import limiter

router = APIRouter(prefix="/uploader")

count_per_req = "3"


@router.post("/params", response_model=SuccessModel[UploadPublic])
@limiter.limit(f"{count_per_req}/minute") # type: ignore
async def get_params(
    upload: UploadType, session: RequireSession, current_user: RequireCurrentUser, request: Request
):
    video = await video_crud.get_by(field="upload_hash", value=upload.upload_hash, session=session)  # type: ignore
    if video:
        raise make_exception(
            code=status.HTTP_409_CONFLICT, detail="Possible duplicate video encountered"
        )
    asset_id = f"{upload.folder}/{current_user.id}/{upload.title}"
    params = await uploader_crud.generate_params(
        asset_id=asset_id, resource_type="video"
    )
    await upload_crud.create(
        data=UploadCreate(
            asset_id=asset_id,
            user_id=current_user.id,
            upload_status=UPLOAD_STATUS_ENUM.PROCESSING,
            **upload.model_dump(exclude={"id", "folder"}),
        ),
        session=session,  # type: ignore
    )
    return SuccessResponse(params)


# todo: implement local upload
@router.post("/local", response_model=SuccessModel[UploadPublic])
@limiter.limit(f"{count_per_req}/minute") # type: ignore
async def upload_local(
    id: IDType, session: RequireSession, current_user: RequireCurrentUser, request: Request
):
    return SuccessResponse({})


# todo: implement bucket upload
@router.post("/bucket", response_model=SuccessModel[List[UploadPublic]])
@limiter.limit(f"{count_per_req}/minute") # type: ignore
async def upload_bucket(
    options: FilterOptionsType,
    session: RequireSession,
    current_user: RequireCurrentUser,
    request: Request
):
    return SuccessResponse({})


@router.get("/resource/{folder}/{title}", response_model=SuccessModel[Any])
@limiter.limit(f"{count_per_req}/minute") # type: ignore
async def get_resource(
    folder: str,
    title: str,
    session: RequireSession,
    current_user: RequireCurrentUser,
    request: Request
):
    asset_id = f"{folder}/{current_user.id}/{title}"
    resource = await uploader_crud.get_resource(
        asset_id=asset_id, resource_type="video"
    )
    return SuccessResponse(resource)

