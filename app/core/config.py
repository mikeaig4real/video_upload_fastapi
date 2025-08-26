from enum import Enum
from functools import lru_cache
import secrets
from typing import Annotated, Any, Dict, TypedDict
from pydantic import AnyUrl, BeforeValidator, MongoDsn, PostgresDsn, computed_field
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict
from app.core.utils import parse_cors
from app.utils import convertSize


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


class CLOUDINARY_CONFIG_TYPE(TypedDict):
    cloud_name: OPTIONAL_STR_TYPE
    api_key: OPTIONAL_STR_TYPE
    api_secret: OPTIONAL_STR_TYPE
    url: OPTIONAL_STR_TYPE


class S3_CONFIG_TYPE(TypedDict):
    bucket: OPTIONAL_STR_TYPE
    access_key: OPTIONAL_STR_TYPE
    secret_key: OPTIONAL_STR_TYPE
    region: OPTIONAL_STR_TYPE


class UPLOAD_BUCKET_ENUM(str, Enum):
    CLOUDINARY = "cloudinary"
    S3 = "s3"
    GOOGLE_CLOUD_STORAGE = "google_cloud_storage"

    @property
    def is_cloudinary(self) -> bool:
        return self == UPLOAD_BUCKET_ENUM.CLOUDINARY

    @property
    def is_s3(self) -> bool:
        return self == UPLOAD_BUCKET_ENUM.S3

    @property
    def is_google_cloud_storage(self) -> bool:
        return self == UPLOAD_BUCKET_ENUM.GOOGLE_CLOUD_STORAGE


class UPLOAD_STORAGE_ENUM(Enum):
    BUCKET = "bucket"
    FILE_SYSTEM = "file_system"

    @property
    def is_bucket(self) -> bool:
        return self == UPLOAD_STORAGE_ENUM.BUCKET

    @property
    def is_file_system(self) -> bool:
        return self == UPLOAD_STORAGE_ENUM.FILE_SYSTEM


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

    MAX_VIDEO_SIZE_MB: int = 10  # Maximum video size in megabytes

    @computed_field
    @property
    def MAX_VIDEO_SIZE(self) -> float:
        return convertSize(self.MAX_VIDEO_SIZE_MB, "MB", "B")

    UPLOAD_BUCKET: UPLOAD_BUCKET_ENUM = UPLOAD_BUCKET_ENUM.CLOUDINARY
    UPLOAD_STORAGE_TYPE: UPLOAD_STORAGE_ENUM = UPLOAD_STORAGE_ENUM.BUCKET

    CLOUDINARY_URL: OPTIONAL_STR_TYPE = None
    CLOUDINARY_CLOUD_NAME: OPTIONAL_STR_TYPE = None
    CLOUDINARY_API_KEY: OPTIONAL_STR_TYPE = None
    CLOUDINARY_API_SECRET: OPTIONAL_STR_TYPE = None

    @property
    def CLOUDINARY_CONFIG(self) -> CLOUDINARY_CONFIG_TYPE:
        if not self.UPLOAD_STORAGE_TYPE.is_bucket:
            raise ValueError("Invalid upload storage type for Cloudinary configuration")

        if not self.UPLOAD_BUCKET.is_cloudinary:
            raise ValueError("Invalid upload bucket for Cloudinary configuration")

        if not all(
            [
                self.CLOUDINARY_URL,
                self.CLOUDINARY_CLOUD_NAME,
                self.CLOUDINARY_API_KEY,
                self.CLOUDINARY_API_SECRET,
            ]
        ):
            raise ValueError("Missing Cloudinary configuration")

        return {
            "url": self.CLOUDINARY_URL,
            "cloud_name": self.CLOUDINARY_CLOUD_NAME,
            "api_key": self.CLOUDINARY_API_KEY,
            "api_secret": self.CLOUDINARY_API_SECRET,
        }

    S3_BUCKET_NAME: OPTIONAL_STR_TYPE = None
    AWS_ACCESS_KEY_ID: OPTIONAL_STR_TYPE = None
    AWS_SECRET_ACCESS_KEY: OPTIONAL_STR_TYPE = None
    AWS_REGION: OPTIONAL_STR_TYPE = None

    @property
    def S3_CONFIG(self) -> S3_CONFIG_TYPE:
        if not self.UPLOAD_STORAGE_TYPE.is_bucket:
            raise ValueError("Invalid storage type for S3 configuration")

        if not self.UPLOAD_BUCKET.is_s3:
            raise ValueError("Invalid bucket type for S3 configuration")

        if not all(
            [
                self.S3_BUCKET_NAME,
                self.AWS_ACCESS_KEY_ID,
                self.AWS_SECRET_ACCESS_KEY,
                self.AWS_REGION,
            ]
        ):
            raise ValueError("Missing S3 configuration")

        return {
            "bucket": self.S3_BUCKET_NAME,
            "access_key": self.AWS_ACCESS_KEY_ID,
            "secret_key": self.AWS_SECRET_ACCESS_KEY,
            "region": self.AWS_REGION,
        }

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
