import helpers
from celery import shared_task
from django.apps import apps

from django.utils import timezone

from . import collect

@shared_task
def measure_temp_task():
    Metric = apps.get_model("sensors", "Metric")
    temp = collect.get_random_temp()
    node_id = helpers.config("NODE_ID", default=0)
    Metric.objects.create(
        node_id=node_id,
        temperature=temp,
        time=timezone.now()
    )