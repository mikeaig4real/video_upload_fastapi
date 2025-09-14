from fastapi import APIRouter, Request
from app.auth.deps import RequireCurrentUser
from app.models.success import SuccessModel
from app.responses import SuccessResponse
from app.user.crud import user_crud, UserUpdate, UserPublic
from app.db.deps import RequireSession
from app.core.rate_limiter import limiter

router = APIRouter(prefix="/user")

count_per_req = "10"

@router.get("/", response_model=SuccessModel[UserPublic])
@limiter.limit(f"{count_per_req}/minute") # type: ignore
async def get(session: RequireSession, current_user: RequireCurrentUser, request: Request):
    """
    Retrieve a single user record
    """
    user = await user_crud.get(id=current_user.id, session=session)  # type: ignore
    return SuccessResponse(user)


@router.patch("/", response_model=SuccessModel[UserPublic])
@limiter.limit(f"{count_per_req}/minute") # type: ignore
async def update(update: UserUpdate, session: RequireSession, current_user: RequireCurrentUser, request: Request):
    """
    Update a single user record
    """
    user = await user_crud.update(
        id=current_user.id, data=update, session=session  # type: ignore
    )
    return SuccessResponse(user)


@router.delete("/", response_model=SuccessModel[UserPublic])
@limiter.limit(f"{count_per_req}/minute") # type: ignore
async def delete(session: RequireSession, current_user: RequireCurrentUser, request: Request):
    """
    Delete a single user record
    """
    user = await user_crud.delete(id=current_user.id, session=session)  # type: ignore
    return SuccessResponse(user)


