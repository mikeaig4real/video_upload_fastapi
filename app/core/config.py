from enum import Enum
from functools import lru_cache
import secrets
from typing import Annotated, Any, Dict
from pydantic import AnyUrl, BeforeValidator, MongoDsn, PostgresDsn, computed_field
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict
from app.core.utils import parse_cors


class ENVIRONMENT_TYPE_ENUM(Enum):
    LOCAL = "local"
    STAGING = "staging"
    PRODUCTION = "production"

    @property
    def is_local(self) -> bool:
        return self == ENVIRONMENT_TYPE_ENUM.LOCAL

    @property
    def is_staging(self) -> bool:
        return self == ENVIRONMENT_TYPE_ENUM.STAGING

    @property
    def is_production(self) -> bool:
        return self == ENVIRONMENT_TYPE_ENUM.PRODUCTION


OPTIONAL_STR_TYPE = str | None

DB_URI_TYPES = str | PostgresDsn | MongoDsn | MultiHostUrl


class DB_TYPE_ENUM(Enum):
    POSTGRES = "postgres"
    MONGO = "mongo"
    SQLITE = "sqlite"

    @property
    def is_sql(self) -> bool:
        return self in {
            DB_TYPE_ENUM.POSTGRES,
            DB_TYPE_ENUM.SQLITE,
        }

    @property
    def is_mongo(self) -> bool:
        return self == DB_TYPE_ENUM.MONGO


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
    )
    FRONTEND_HOST: str = "http://localhost:5173"
    ENVIRONMENT: ENVIRONMENT_TYPE_ENUM = ENVIRONMENT_TYPE_ENUM.LOCAL
    PROJECT_NAME: OPTIONAL_STR_TYPE = None
    BACKEND_CORS_ORIGINS: Annotated[list[AnyUrl] | str, BeforeValidator(parse_cors)] = (
        []
    )

    @computed_field
    @property
    def ALL_CORS_ORIGINS(self) -> list[str]:
        return [str(origin).rstrip("/") for origin in self.BACKEND_CORS_ORIGINS] + [
            self.FRONTEND_HOST
        ]

    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    DB_NAME: OPTIONAL_STR_TYPE = None
    ENCODE_ALGORITHM: OPTIONAL_STR_TYPE = "HS256"
    DB_SERVER: OPTIONAL_STR_TYPE = None
    DB_PORT: int | None = None
    DB_USER: OPTIONAL_STR_TYPE = None
    DB_PASSWORD: OPTIONAL_STR_TYPE = None
    DB_TYPE: DB_TYPE_ENUM = DB_TYPE_ENUM.SQLITE
    API_PREFIX: str = "/api"
    MONGO_ATLAS_URI: OPTIONAL_STR_TYPE = None
    USE_MIGRATIONS: bool = False

    @computed_field
    @property
    def IS_SQL(self) -> bool:
        return self.DB_TYPE.is_sql

    @computed_field
    @property
    def DB_URI(self) -> DB_URI_TYPES:
        options: Dict[str, Any] = {
            "username": self.DB_USER,
            "password": self.DB_PASSWORD,
            "host": self.DB_SERVER,
            "port": self.DB_PORT,
            "path": self.DB_NAME,
        }
        match self.DB_TYPE:
            case DB_TYPE_ENUM.POSTGRES:
                return MultiHostUrl.build(scheme="postgresql+psycopg", **options)
            case DB_TYPE_ENUM.MONGO:
                return (
                    str(self.MONGO_ATLAS_URI)
                    if self.MONGO_ATLAS_URI
                    else MultiHostUrl.build(scheme="mongodb", **options)
                )
            case DB_TYPE_ENUM.SQLITE:
                return f"sqlite:///{self.DB_NAME}.db"
            case _:
                raise ValueError(f"Unsupported DB type: {self.DB_TYPE}")


@lru_cache()
def get_config():
    return Config()
