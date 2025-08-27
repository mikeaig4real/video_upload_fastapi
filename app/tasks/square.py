from app.worker import celery_app


@celery_app.task # type: ignore
def square(num: int) -> int:
    print(f"Squaring {num}")
    result = int(num) ** 2
    print(f"Squared result: {result}")
    return result
