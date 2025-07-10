# backend/make_celery.py

from celery import Celery
from celery.schedules import crontab
from app import create_app
import os

def celery_init_app(app=None):
    if app is None:
        app = create_app()

    celery = Celery(
        app.import_name,
        broker=app.config["CELERY_BROKER_URL"],
        backend=app.config["CELERY_RESULT_BACKEND"]
    )

    # Celery configuration
    celery.conf.update(
        broker_connection_retry_on_startup=True,
        task_track_started=True,
        task_time_limit=int(os.getenv('CELERY_TASK_TIME_LIMIT', 600)),
        task_soft_time_limit=int(os.getenv('CELERY_TASK_SOFT_TIME_LIMIT', 300)),
        worker_prefetch_multiplier=1,
        worker_max_tasks_per_child=int(os.getenv('CELERY_WORKER_MAX_TASKS_PER_CHILD', 50)),
        task_ignore_result=app.config.get("CELERY_TASK_IGNORE_RESULT", True),
        beat_schedule={
            "auto-reparse-feeds-every-hour": {
                "task": "app.tasks.feed_task.auto_reparse_all",
                "schedule": crontab(minute=0, hour="*"),
            },
            "daily-data-export": {
                "task": "app.tasks.export_task.scheduled_export_task",
                "schedule": crontab(minute=0, hour=0),  # Run at midnight UTC
            }
        }
    )

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    celery.autodiscover_tasks(['app.tasks'])
    return celery

flask_app = create_app()
celery_app = celery_init_app(flask_app)

# Run with:
# celery -A make_celery worker --loglevel=info
# celery -A make_celery beat --loglevel=info
