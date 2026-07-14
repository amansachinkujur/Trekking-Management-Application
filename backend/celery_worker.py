from celery import Celery
from celery.schedules import crontab

from app import create_app

# Create Flask app
flask_app = create_app()

# Create Celery app
celery = Celery(
    flask_app.import_name,
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

# Celery Beat schedule
celery.conf.beat_schedule = {
    "daily-reminder": {
        "task": "app.tasks.send_daily_reminders",
        "schedule": crontab(hour=9, minute=0),
    },
    "monthly-report": {
        "task": "app.tasks.send_monthly_report",
        "schedule": crontab(hour=9, minute=0, day_of_month=1),
    },
}

celery.conf.timezone = "Asia/Kolkata"


class ContextTask(celery.Task):

    def __call__(self, *args, **kwargs):

        with flask_app.app_context():

            return self.run(*args, **kwargs)


celery.Task = ContextTask

# Import all Celery tasks
import app.tasks