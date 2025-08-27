from app.worker import celery_app


@celery_app.task  # type: ignore
def sum_nums(nums: list[int]) -> int:
    print(f"Summing numbers: {nums}")
    result = sum(nums)
    print(f"Sum result: {result}")
    return result
