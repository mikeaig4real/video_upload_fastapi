from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler
from app.core.config import get_config
from app.core.utils import custom_generate_unique_id
from app.exceptions import Error, NotFound, ServerError, Unauthorized
from app.user.router import router as user_router
from app.auth.router import router as auth_router
from app.video.router import router as video_router
from app.uploader.router import router as uploader_router
from app.upload.router import router as upload_router
from app.library.router import router as library_router
from app.core.rate_limiter import limiter

config = get_config()


@asynccontextmanager
async def lifespan(app: FastAPI):
    from app.db.connect import try_db, init_db

    await try_db()
    init_db()
    yield

app = FastAPI(
    title=config.PROJECT_NAME if config.PROJECT_NAME else "Default",
    openapi_url=f"{config.API_PREFIX}/openapi.json",
    generate_unique_id_function=custom_generate_unique_id,
    lifespan=lifespan,
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)  # type: ignore


@app.exception_handler(Exception)
async def exception_handler(_, e: str):
    return ServerError(e)


@app.exception_handler(ValueError)
async def value_handler(_, e: str):
    return Error(e)


@app.exception_handler(HTTPException)
async def http_exception_handler(_, exc: HTTPException):
    if exc.status_code == 401:
        return Unauthorized(exc.detail)
    elif exc.status_code == 404:
        return NotFound(exc.detail)
    return Error(exc.detail)


app.include_router(user_router, prefix=config.API_PREFIX)
app.include_router(auth_router, prefix=config.API_PREFIX)
app.include_router(video_router, prefix=config.API_PREFIX)
app.include_router(uploader_router, prefix=config.API_PREFIX)
app.include_router(upload_router, prefix=config.API_PREFIX)
app.include_router(library_router, prefix=config.API_PREFIX)


if config.ENVIRONMENT.is_production and len(config.ALL_FRONTEND_HOSTS):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.ALL_FRONTEND_HOSTS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
elif len(config.ALL_CORS_ORIGINS):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.ALL_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.get("/")
@limiter.limit("10/minute")  # type: ignore
async def health(request: Request):
    return {"status": "healthy"}
