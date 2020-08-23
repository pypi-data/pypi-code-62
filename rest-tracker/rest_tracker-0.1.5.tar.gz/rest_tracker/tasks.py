import requests
from celery import shared_task

from . import ELASTIC_SESSION
from .models import REST_TRACKER_ES_MAPPING
from .serializers import Rest_Tracker_Request_Serializer

ES_INDEX = 'rest_tracker'
ES_TYPE = 'request'

@shared_task()
def rest_tracker_task(task_data):
    serializer = Rest_Tracker_Request_Serializer(data=task_data)
    if serializer.is_valid():
        serializer.save()
        # if ELASTIC_SESSION.initialized:
        print(serializer.data)
        return serializer.data
    else:
        return serializer.errors

@shared_task()
def init_es(host:str='localhost', port:str='9200'):
    ELASTIC_SESSION.set_host(host)
    ELASTIC_SESSION.set_port(port)
    resp = ELASTIC_SESSION.create_index(ES_INDEX, REST_TRACKER_ES_MAPPING)
    if resp.status_code == 200:
        ELASTIC_SESSION.initialized = True
        return resp.json()
    else:
        return resp.text


