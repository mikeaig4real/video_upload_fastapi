from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm

# create a dependency for oauth2 form
RequireForm = Annotated[OAuth2PasswordRequestForm, Depends()]
