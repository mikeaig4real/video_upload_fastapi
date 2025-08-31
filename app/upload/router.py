from fastapi import APIRouter, Request, status
from app.auth.deps import RequireCurrentUser
from app.auth.utils import make_exception
from app.models.success import SuccessModel
from app.responses import SuccessResponse
from app.upload.crud import upload_crud, UploadUpdate, UploadPublic
from app.db.deps import RequireSession
from app.core.rate_limiter import limiter

router = APIRouter(prefix="/upload")

count_per_req = "5"


@router.get("/", response_model=SuccessModel[UploadPublic])
@limiter.limit(f"{count_per_req}/minute") # type: ignore
async def get(asset_id: str, session: RequireSession, _: RequireCurrentUser, request: Request):
    upload = await upload_crud.get_by(field="asset_id", value=asset_id, session=session)  # type: ignore
    if not upload:
        raise make_exception(code=status.HTTP_404_NOT_FOUND, detail="Upload not found")
    return SuccessResponse(upload)


@router.patch("/{id}", response_model=SuccessModel[UploadPublic])
@limiter.limit(f"{count_per_req}/minute") # type: ignore
async def update(
    id: str, update: UploadUpdate, session: RequireSession, _: RequireCurrentUser, request: Request
):
    upload = await upload_crud.update(
        id=id, data=update, session=session  # type: ignore
    )
    if not upload:
        raise make_exception(code=status.HTTP_404_NOT_FOUND, detail="Upload not found")
    return SuccessResponse(upload)


@router.delete("/{id}", response_model=SuccessModel[UploadPublic])
@limiter.limit(f"{count_per_req}/minute") # type: ignore
async def delete(id: str, session: RequireSession, _: RequireCurrentUser, request: Request):
    upload = await upload_crud.delete(id=id, session=session)  # type: ignore
    if not upload:
        raise make_exception(code=status.HTTP_404_NOT_FOUND, detail="Upload not found")
    return SuccessResponse(upload)
