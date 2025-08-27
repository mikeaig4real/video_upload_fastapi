from app.worker import celery_app


@celery_app.task # type: ignore
def to_decimal(binary: int) -> int:
    print(f"Converting binary {binary} to decimal")
    decimal = int(str(binary), 2)
    print(f"Converted decimal: {decimal}")
    return decimal
