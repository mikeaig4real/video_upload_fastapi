from typing import Annotated
from fastapi import Depends, status
from fastapi.security import OAuth2PasswordBearer
from app.auth.utils import ToTokenType, decode_token, make_exception
from app.core.config import get_config
from app.core.utils import make_custom_logger
from app.db.deps import RequireSession
from app.user.model import User
from app.user.crud import crud as user_crud
# make a custom logger for logging
CUSTOM_LOGGER = make_custom_logger(__name__)
config = get_config()
# set up oauth2_scheme with bearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{config.API_PREFIX}/auth/login")
# create a dependency using set up
RequireOAuth = Annotated[str, Depends(oauth2_scheme)]


async def get_current_user(token: RequireOAuth, session: RequireSession):
    """
    Gets token from dependency, decodes token, uses decoded info to retrieve then return user
    """
    # make an exception to avoid repetition
    auth_exception = make_exception(
        code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials"
    )
    try:
        decoded: ToTokenType = decode_token(token)
        user_email = decoded.get("sub", None)
        user = await user_crud.get_by(field="email", value=user_email, session=session) # type: ignore
        if not user_email or not user:
            raise auth_exception
        return user
    except Exception as e:
        CUSTOM_LOGGER.warning(e)
        raise auth_exception
# create a dependency on get_current_user to be used for protected routes
RequireCurrentUser = Annotated[User, Depends(get_current_user)]
