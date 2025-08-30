import asyncio
# from datetime import timedelta
from celery import Celery
from celery.schedules import crontab # pyright: ignore[reportUnusedImport]

celery_app = Celery(
    "worker",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
    include=[
        "app.tasks.upload",
    ],
)

celery_app.conf.beat_schedule = {  # type: ignore
    "daily-reconcile-videos": {
        "task": "app.tasks.upload.reconcile_videos",
        "schedule": crontab(hour=0, minute=0),  # daily at midnight UTC
        # "schedule": timedelta(minutes=1),  # every 1 minute (testing)
    },
}

celery_app.autodiscover_tasks()  # pyright: ignore[reportUnknownMemberType]
celery_app.conf.timezone = "UTC" # type: ignore
# Create one global loop and reuse it for all Celery tasks
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
