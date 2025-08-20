from fastapi import APIRouter
from app.auth.deps import RequireCurrentUser
from app.models.id import IDType
from app.models.success import SuccessModel
from app.responses import SuccessResponse
from app.user.crud import user_crud, UserUpdate, UserPublic
from app.db.deps import RequireSession

router = APIRouter(prefix="/user")


@router.get("/{id}", response_model=SuccessModel[UserPublic])
async def get(id: IDType, session: RequireSession, current_user: RequireCurrentUser):
    user = await user_crud.get(
        id=id, session=session # type: ignore
    )
    return SuccessResponse(user)


@router.patch("/{id}", response_model=SuccessModel[UserPublic])
async def update(id: IDType, update: UserUpdate, session: RequireSession, current_user: RequireCurrentUser):
    user = await user_crud.update(
        id=id, data=update, session=session # type: ignore
    )
    return SuccessResponse(user)


@router.delete("/{id}", response_model=SuccessModel[UserPublic])
async def delete(id: IDType, session: RequireSession, current_user: RequireCurrentUser):
    user = await user_crud.delete(
        id=id, session=session # type: ignore
    )
    return SuccessResponse(user)
