from fastapi import APIRouter, status
from app.auth.utils import Token, make_exception, make_user_token, verify_pass
from app.db.deps import RequireSession
from app.models.form_data import RequireForm
from app.user.crud import user_crud
from app.user.model import UserCreate

router = APIRouter(prefix="/auth")


@router.post("/login", response_model=Token)
async def login(form_data: RequireForm, session: RequireSession):
    user_email = form_data.username
    user_pass = form_data.password
    user = await user_crud.get_by(field="email", value=user_email, session=session)  # type: ignore
    if not user:
        raise make_exception(
            code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials"
        )
    pass_is_verified = verify_pass(user_pass, hashed_pass=user.hashed_password)
    if not pass_is_verified:
        raise make_exception(
            code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials"
        )
    return make_user_token(user)


@router.post("/register", response_model=Token)
async def register(
    user_data: UserCreate,
    session: RequireSession,
):
    user_exists = await user_crud.get_by(field="email", value=user_data.email, session=session)  # type: ignore
    if user_exists:
        raise make_exception(
            code=status.HTTP_409_CONFLICT, detail="User with that email already exists"
        )
    user = await user_crud.create(data=user_data, session=session)  # type: ignore
    return make_user_token(user)
