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
    1. check if hash already exists in db too? probably validate size and type too?
    # video = video_crud.find_by_hash(hash=upload.upload_hash)
    2. Save some residue data incase the process is not completed properly
    3. Schedule a background task in advance with retries, use upload_status to check if upload was complete
    if true, kill task
    else, use asset id to grab info from bucket, and persist it, 
    else if data did not even get to bucket, delete existing residue data, kill task too
    PS: make sure to make possible modifications to model/schemas as needed
    """
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
