from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import get_config
from app.core.utils import custom_generate_unique_id
from app.exceptions import Error, NotFound, ServerError, Unauthorized
from app.user.router import router as user_router
from app.auth.router import router as auth_router
from app.video.router import router as video_router
from app.uploader.router import router as uploader_router
from app.upload.router import router as upload_router
# from app.workflows.num_chain import num_workflow


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


# @app.get("/num_chain/{x}")
# def run_number_workflow(x: int):
#     task = num_workflow(x)  # type: ignore
#     return {"task_id": task.id}


if len(config.ALL_CORS_ORIGINS):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.ALL_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.get("/")
async def health():
    return {"status": "healthy"}
