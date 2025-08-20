from typing import Annotated, Any
from fastapi import Depends
from sqlmodel import Session
from app.db.connect import connect
from motor import core


_, _, _, get_session = connect()


RequireSession = Annotated[core.AgnosticDatabase[Any] | Session, Depends(get_session)]
