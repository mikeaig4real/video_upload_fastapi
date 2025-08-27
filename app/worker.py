from celery import Celery

celery_app = Celery(
    "worker",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
    include=[
        # "app.tasks.to_decimal",
        # "app.tasks.square",
        # "app.tasks.half",
        # "app.tasks.sum_nums",
    ],
)

celery_app.autodiscover_tasks()  # pyright: ignore[reportUnknownMemberType]
