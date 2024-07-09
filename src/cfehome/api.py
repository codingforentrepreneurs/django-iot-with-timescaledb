from typing import List
from datetime import datetime
from ninja import NinjaAPI, Schema

# from sensors.models import Metric
from sensors import services

api = NinjaAPI()


class NodeMaxMinTempSchema(Schema): # pydantic
    node_id: int
    max_temp: float
    min_temp: float


class MaxMinTempSchema(Schema): # pydantic
    max_temp: float
    min_temp: float


class AvgTempSchema(Schema): # pydantic
    avg_temp: float
    time_group: datetime


class NodeAvgTempSchema(Schema): # pydantic
    node_id: int
    avg_temp: float
    time_group: datetime

@api.get('/temps', response=List[AvgTempSchema])
def get_average_temps(request):
    qs = services.get_avg_temp()
    return qs


@api.get('/temps/node', response=List[NodeAvgTempSchema])
def get_average_temps(request):
    qs = services.get_node_avg_temp()
    return qs


@api.get('/temps/maxmin', response=MaxMinTempSchema)
def get_average_temps(request):
    qs = services.get_max_min_temp()
    return qs

@api.get('/temps/nodes/maxmin', response=List[NodeMaxMinTempSchema])
def get_average_temps(request):
    qs = services.get_node_max_min_temp()
    return qs