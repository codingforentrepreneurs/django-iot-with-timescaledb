from datetime import timedelta, datetime
from django.db.models import Avg, Max, Min
from django.db.models.functions import TruncMinute
from django.utils import timezone
from .models import Metric

def get_avg_temp():
    now = timezone.now()
    start_range = (now-timedelta(days=1))
    qs = (
        Metric.timescale
        .filter(time__range=(start_range, now))
        .annotate(time_group=TruncMinute('time'))
        .values('time_group')
        .annotate(avg_temp=Avg('temperature'))
        .order_by('time_group')
    )
    return qs


def get_node_avg_temp():
    now = timezone.now()
    start_range = (now-timedelta(days=1))
    qs = (
        Metric.timescale
        .filter(time__range=(start_range, now))
        .annotate(time_group=TruncMinute('time'))
        .values('time_group', 'node_id')
        .annotate(avg_temp=Avg('temperature'))
        .order_by('time_group', 'node_id')
    )
    return qs


def get_max_min_temp():
    now = timezone.now()
    start_range = (now-timedelta(days=1))
    qs = (
        Metric.timescale
        .filter(time__range=(start_range, now))
        .aggregate(max_temp=Max('temperature'), min_temp=Min("temperature"))
    )
    return qs

def get_node_max_min_temp():
    now = timezone.now()
    start_range = (now-timedelta(days=1))
    qs = (
        Metric.timescale
        .filter(time__range=(start_range, now))
        .values("node_id")
        .annotate(max_temp=Max('temperature'), min_temp=Min("temperature"))
        .order_by('node_id')
    )
    return qs