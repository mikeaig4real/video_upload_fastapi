import asyncio

# from datetime import timedelta
from celery import Celery
from celery.schedules import crontab

from app.core.config import get_config  # pyright: ignore[reportUnusedImport]

config = get_config()
# register workers
celery_app = Celery(
    "worker",
    broker=config.REDIS_URL,
    backend=config.DB_URI,
    include=[
        "app.tasks.upload",
    ],
)

# Limit Redis connections to help avoid 'max number of clients reached' errors
celery_app.conf.broker_pool_limit = 2  # type: ignore # Reduce if needed (default is 10)


celery_app.conf.beat_schedule = {  # type: ignore
    "daily-reconcile-videos": {
        "task": "app.tasks.upload.reconcile_videos",
        "schedule": crontab(hour=0, minute=0),  # daily at midnight UTC
        # "schedule": timedelta(minutes=1),  # every 1 minute (testing)
    },
}

celery_app.autodiscover_tasks()  # pyright: ignore[reportUnknownMemberType]
celery_app.conf.timezone = "UTC"  # type: ignore
# Create one global loop and reuse it for all Celery tasks
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
