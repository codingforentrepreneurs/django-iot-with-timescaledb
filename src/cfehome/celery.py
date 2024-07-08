import os

from celery import Celery
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cfehome.settings")

app = Celery("cfehome")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

CELERY_BEAT_SCHEDULE = {
    "check-temp": {
        "task": "sensors.tasks.measure_temp_task",
        "schedule": 5.0 # every 5 seconds
    },
}

# celery -A cfehome worker --beat -l info
app.conf.beat_schedule = CELERY_BEAT_SCHEDULE