import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "daily_words_backend.settings")
app = Celery("daily_words_backend")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

# triggers word sending function every hour
app.conf.beat_schedule = {
    'send-daily-words': {
        'task':'send_daily_words_task',
        'schedule': crontab(minute=0, hour='*')
    }
}