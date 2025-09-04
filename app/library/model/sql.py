# from datetime import datetime, timezone
# from pydantic import EmailStr
# from sqlmodel import Field, SQLModel, Relationship
# from typing import Optional, List, TYPE_CHECKING

# from app.constants import ENTITY_NAMES

# if TYPE_CHECKING:
#     from app.video.model.sql import Video


# class UserBase(SQLModel):
#     email: EmailStr = Field(index=True, unique=True)
#     username: str = Field(index=True, unique=True)


# class User(UserBase, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True, index=True)
#     hashed_password: str
#     created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
#     updated_at: datetime = Field(
#         default_factory=lambda: datetime.now(timezone.utc),
#         sa_column_kwargs={"onupdate": lambda: datetime.now(timezone.utc)},
#     )

#     videos: List["Video"] = Relationship(
#         back_populates=ENTITY_NAMES.USER.value,
#         sa_relationship_kwargs={"lazy": "selectin"},
#     )


# class UserCreate(UserBase):
#     password: str


# class UserPublic(UserBase):
#     id: int
#     created_at: datetime
#     updated_at: datetime


# class UserUpdate(SQLModel):
#     username: Optional[str] = None
#     email: Optional[EmailStr] = None
