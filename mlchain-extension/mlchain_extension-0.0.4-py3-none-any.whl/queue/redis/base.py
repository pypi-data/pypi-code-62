from mlchain.base.serializer import MsgpackSerializer
from mlchain import logger
from mlchain.base.exceptions import MlChainError
from bson import ObjectId
import json
import redis
from mlchain.workflows import Task
import os
from contextvars import ContextVar

redis_client = ContextVar('redis_client')

serializer = MsgpackSerializer()

MLCHAIN_EVENT_QUEUE = 'mlchain_event_queue'
MLCHAIN_DATABASE_QUEUE = 'mlchain_database_queue'

class RedisTask(Task):
    def __init__(self, func_, *args, **kwargs):
        assert len(args) == 0, "RedisTask not allow argument parameters"
        Task.__init__(self, func_, *args, **kwargs)

    def exec(self, required=None, send_value=False):
        if required is None:
            return Task.exec(self)
        else:
            raise AssertionError("Can't exec task with required. Please use exec_async")

    def exec_async(self, required=None, send_value=False):
        if required is None:
            required = []
        if not isinstance(self.func_, str):
            queue_name = getattr(self.func_, '__queue__', None)
            if not isinstance(queue_name, str):
                raise AssertionError("Only register task to served function or queue name")
            else:
                post_process = queue_name
        else:
            raise AssertionError("Only register task to served function")
        key = str(ObjectId())
        msg = {
            'post_process': post_process,
            'context_id': key,
            'type': 'task',
            'required': required,
            'send_value': send_value,
            'kwargs': self.kwargs,
            'args': self.args
        }
        client = redis_client.get()
        if client is None:
            raise MlChainError("Not init redis client")
        else:
            client.lpush(MLCHAIN_EVENT_QUEUE, serializer.encode(msg))
        return key

    @staticmethod
    def get_result(task_id):
        client = redis_client.get()
        if client is None:
            raise MlChainError("Not init redis client")
        else:
            return serializer.decode(client.get(task_id))

    @staticmethod
    def get_result_batch(task_ids):
        client = redis_client.get()
        if client is None:
            raise MlChainError("Not init redis client")
        else:
            raws = client.mget(task_ids)
        return [serializer.decode(raw) for raw in raws]


class RedisBase:
    def __init__(self, host=None, port=None, db=None, password=None, version='0.0', name='MLChain', config=None):
        self.host = host or os.getenv('REDIS_HOST', 'localhost')
        self.port = port or os.getenv('REDIS_PORT', 6379)
        self.db = db or os.getenv('REDIS_DB', 0)
        self.password = password or os.getenv('REDIS_PASSWORD', '')
        self.version = version
        self.name = name
        self.serializer = MsgpackSerializer()
        if config is None:
            config = []
        self.config = config
        self.topics = {c['function_name']: c['input'] for c in self.config}
        logger.info(json.dumps(self.config, indent=' '))
        self.client = redis.Redis(host=self.host,
                                  port=self.port,
                                  password=self.password,
                                  db=self.db)

    def publish(self, function_name, key, args, kwargs, context):
        if function_name not in self.topics:
            raise MlChainError("Not found {0} in config. please add function to config".format(function_name))
        if key is None:
            key = str(ObjectId())

        inputs = {
            'args': args,
            'kwargs': kwargs
        }
        try:
            self.client.lpush(self.topics[function_name], self.serializer.encode({
                'value': inputs,
                'context': context,
                'key': key,
                'function_name':function_name,
                'name':self.name,
                'type':'call'
            }))
            return key
        except Exception as e:
            logger.error(str(e))
            raise e
