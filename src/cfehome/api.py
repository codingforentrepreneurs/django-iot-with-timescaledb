from typing import List
from datetime import datetime
from ninja import NinjaAPI, Schema

# from sensors.models import Metric
from sensors import services

api = NinjaAPI()

class AvgTempSchema(Schema): # pydantic
    avg_temp: float
    time_group: datetime

@api.get('/temps', response=List[AvgTempSchema])
def get_average_temps(request):
    qs = services.get_avg_temp()
    return qs