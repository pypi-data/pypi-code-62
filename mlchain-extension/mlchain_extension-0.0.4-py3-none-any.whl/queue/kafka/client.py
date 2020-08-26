from mlchain.client.base import MLClient
from bson.objectid import ObjectId
from .server import KafkaBase


class KafkaClient(MLClient, KafkaBase):
    def __init__(self, bootstrap_servers=None, mongo_connection=None, version='0.0', name='MLChain',
                 input_topic=None, check_status=False, headers=None, **kwargs):
        MLClient.__init__(self, api_key=None, api_address=None, serializer='msgpack', name=name,
                          version=version, check_status=check_status, headers=headers, **kwargs)
        KafkaBase.__init__(self, bootstrap_servers, mongo_connection, version=version, name=name,
                           input_topic=input_topic)

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
        output = self.publish(function_name=function_name, key=key, args=args, kwargs=kwargs, context=context)
        return self.serializer.encode({'output': output})

    def _get_function(self, name):
        if name == 'store_get':
            return self.result
        else:
            return MLClient._get_function(self, name)

    def __del__(self):
        self.producer.flush()

    def __delete__(self, instance):
        self.producer.flush()
        instance.producer.flush()
