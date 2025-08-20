from fastapi import APIRouter
from app.auth.deps import RequireCurrentUser
from app.models.success import SuccessModel
from app.responses import SuccessResponse
from app.user.crud import user_crud, UserUpdate, UserPublic
from app.db.deps import RequireSession

router = APIRouter(prefix="/user")


@router.get("/", response_model=SuccessModel[UserPublic])
async def get(session: RequireSession, current_user: RequireCurrentUser):
    user = await user_crud.get(id=current_user.id, session=session)  # type: ignore
    return SuccessResponse(user)


@router.patch("/", response_model=SuccessModel[UserPublic])
async def update(update: UserUpdate, session: RequireSession, current_user: RequireCurrentUser):
    user = await user_crud.update(
        id=current_user.id, data=update, session=session  # type: ignore
    )
    return SuccessResponse(user)


@router.delete("/", response_model=SuccessModel[UserPublic])
async def delete(session: RequireSession, current_user: RequireCurrentUser):
    user = await user_crud.delete(id=current_user.id, session=session)  # type: ignore
    return SuccessResponse(user)
