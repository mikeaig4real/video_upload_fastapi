from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm


RequireForm = Annotated[OAuth2PasswordRequestForm, Depends()]
