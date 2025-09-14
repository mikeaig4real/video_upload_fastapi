from typing import Annotated, Any
from fastapi import Depends
from sqlmodel import Session
from app.db.connect import get_session
from motor import core

# create a session dependency for api
RequireSession = Annotated[core.AgnosticDatabase[Any] | Session, Depends(get_session)]
