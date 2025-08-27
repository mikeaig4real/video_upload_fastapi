from app.worker import celery_app


@celery_app.task  # type: ignore
def subtract(x: int, y: int) -> int:
    return x - y
