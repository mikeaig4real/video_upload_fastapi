from typing import List
from fastapi import APIRouter
from app.auth.deps import RequireCurrentUser
from app.models.filter import FilterOptionsType
from app.models.id import IDType
from app.models.success import SuccessModel
from app.responses import SuccessResponse
from app.upload.model import (
    UploadType,
    UploadPublic,
)  # pyright: ignore[reportUnusedImport]
from app.upload.crud import uploader_crud
from app.db.deps import RequireSession

router = APIRouter(prefix="/upload")


@router.get("/params", response_model=SuccessModel[UploadPublic])
async def get_params(
    upload: UploadType, _: RequireSession, current_user: RequireCurrentUser
):
    """TODO:
    1. Check if video with the same hash already exists
    2. If yes, raise an error on footprint already existing
    3. If no, persist some info about the video in database (adjust video models as needed)
    4. Create a Celery job that will check all uploads have completed in status within time frame,
    or else destroy the video's orphaned uploads
    """
    # video = video_crud.find_by_hash(hash=upload.upload_hash)
    asset_id = f"{upload.folder}/{current_user.id}/{upload.title}"
    params = uploader_crud.generate_params(asset_id=asset_id, resource_type="video")
    return SuccessResponse(params)


# todo: implement local upload
@router.post("/local", response_model=SuccessModel[UploadPublic])
async def upload_local(
    id: IDType, session: RequireSession, current_user: RequireCurrentUser
):
    return SuccessResponse({})


# todo: implement bucket upload
@router.post("/bucket", response_model=SuccessModel[List[UploadPublic]])
async def upload_bucket(
    options: FilterOptionsType,
    session: RequireSession,
    current_user: RequireCurrentUser,
):
    return SuccessResponse({})
