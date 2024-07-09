import os

from celery import Celery
from kombu import Queue, Exchange

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cfehome.settings")

app = Celery("cfehome")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

nodes = [
    "node-1",
    "node-2",
    "node-3",
    "node-4",
    "node-5",
    "node-6",
    "node-7",
    "node-8",
]

CELERY_TASK_QUEUES = []
CELERY_BEAT_SCHEDULE = {}
for node in nodes:
    CELERY_TASK_QUEUES.append(
        Queue(node, Exchange(node), routing_key=node),
    )
    key = f"check-temp-{node}"
    CELERY_BEAT_SCHEDULE[key] = {
        "task": "sensors.tasks.measure_temp_task",
        "schedule": 5.0, # every 5 seconds
        "options": {"queue": node} # apply_async(queue="node-1")
    }

app.conf.task_queues = CELERY_TASK_QUEUES
# celery -A cfehome worker -Q node-2 -l info
# celery -A cfehome beat -l info
app.conf.beat_schedule = CELERY_BEAT_SCHEDULE