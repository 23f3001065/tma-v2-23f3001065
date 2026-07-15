from celery import Celery
from celery.schedules import crontab
from datetime import timedelta

celery = Celery(
    "tma",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

celery.conf.timezone = "Asia/Kolkata"

celery.conf.beat_schedule = {

    "daily-trek-reminders": {

        "task": "tasks.send_daily_reminders",

        "schedule": crontab(hour=8, minute=0)
    },

    "monthly-admin-report": {

        "task": "tasks.send_monthly_admin_report",

        "schedule": crontab(day_of_month=1, hour=9, minute=0)
    }
}

import tasks