from app.worker import celery_app


@celery_app.task # type: ignore
def half(num: int) -> float:
    print(f"Halving {num}")
    result = float(num) / 2
    print(f"Halved result: {result}")
    return result
