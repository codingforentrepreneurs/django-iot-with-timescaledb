from django.contrib import admin

# Register your models here.
from .models import Metric


class MetricAdmin(admin.ModelAdmin):
    list_display = ("node_id", "temperature", "time")


admin.site.register(Metric, MetricAdmin)