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
        if ELASTIC_SESSION.initialized:
            es_content = {
                'created_at': serializer.data['created'],
                'scheme': serializer.data['scheme'],
                'method': serializer.data['method'],
                'url_host': serializer.data['url']['host'],
                'url_path': serializer.data['url']['path'],
                'url_raw': serializer.data['url']['raw'],
                'user_agent': serializer.data['user_agent'],
                'response_status_code': serializer.data['responses'][-1]['status_code'],
                'response_content_size': serializer.data['responses'][-1]['content_size']
            }
            resp = ELASTIC_SESSION.add_content(ES_INDEX, ES_TYPE, es_content)
            if resp.status_code == 200:
                return serializer.data, resp.json()
            else:
                return serializer.data, resp.text
        return serializer.data
    else:
        return serializer.errors

@shared_task()
def initialize_es(host:str='elasticsearch', port:str='9200'):
    ELASTIC_SESSION.set_host(host)
    ELASTIC_SESSION.set_port(port)
    resp = ELASTIC_SESSION.create_index(ES_INDEX, REST_TRACKER_ES_MAPPING)
    if resp.status_code == 200:
        ELASTIC_SESSION.initialized = True
        return resp.json()
    else:
        return resp.text


