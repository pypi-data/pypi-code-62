from mlchain.client.base import MLClient
from bson.objectid import ObjectId
from .base import RedisBase
from mlchain import logger
import json


class RedisClient(MLClient, RedisBase):

    def __init__(self, host=None, port=None, db=None, password=None, version='0.0', name='MLChain', check_status=False,
                 headers=None):
        MLClient.__init__(self, api_key=None, api_address=None, serializer='msgpack', name=name,
                          version=version, check_status=check_status, headers=headers)
        RedisBase.__init__(self, host=host, port=port, db=db, password=password, version=version, name=name)
        self.config = self.serializer.decode(self.client.get('mlchain_queue_{0}:{1}'.format(self.name, self.version)))
        logger.info(json.dumps(self.config, indent=' '))
        self.topics = {c['function_name']: c['input'] for c in self.config}

    def _get(self, api_name, headers=None, params=None):
        """
        GET data from url
        """
        pass

    def _post(self, function_name, headers=None, args=None, kwargs=None):

        if args is None:
            args = []
        if kwargs is None:
            kwargs = {}
        if headers is None:
            headers = {}
        context = headers
        key = str(ObjectId())
        context['context_id'] = key
        output = self.publish(function_name, key=key, args=args, kwargs=kwargs, context=context)
        return self.serializer.encode({'output': output})

    def _get_function(self, name):
        if name == 'store_get':
            return self.result
        else:
            return MLClient._get_function(self, name)

    def result(self, key):
        output = self.client.get(key)
        if output is not None:
            out = self.serializer.decode(output)
            if '__error__' in out:
                status = 'FAILURE'
            else:
                status = 'SUCCESS'
            return {'status': status, 'output': out, 'time': 0}
        return {'status': None, 'output': None, 'time': 0}
