from typing import Annotated
from fastapi import Body
from pydantic import BaseModel, EmailStr, Field


class BodyParams(BaseModel):
    model_config = {"extra": "forbid"}

    password: str = Field(max_length=20, min_length=5)
    username: str = Field(max_length=20, min_length=9)
    email: EmailStr


BodyType = Annotated[BodyParams, Body()]
