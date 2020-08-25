import json
import uuid
import time
from datetime import datetime
from queue import Queue
from threading import Event
from types import FunctionType, MethodType
from typing import Union

from kombu import Connection, Producer
from strongtyping.strong_typing import match_typing

from kombunicator.MessageConsumer import MessageConsumer
from kombunicator.BusPlugins import RPCRequestPlugin, CallbackPlugin


class RPCClient:

    @match_typing
    def __init__(self, connection_parameter: dict, request_key: str,
                 default_callback: Union[FunctionType, MethodType] = None, plugin: str = None):
        """Create a RPC Client to make request to another service. The message is routed via the RabbitMQ default exchange.

        Parameters
        ----------
        connection_parameter : `dict`
            Holds the connection parameters to a RabbitMQ instance.
            - 'hostname': `str` Host where RabbitMQ is accessible
            - 'virtual_host': `str` virtual host of RabbitMQ instance
            - 'port': `int` port to RabbitMQ instance
            - 'userid': `str` username
            - 'password': `str` password
        request_key: `str`
            The request key as given by the RPC Server.
        default_callback: `callable`
            a default callback function for this RCPClient. Will be called if no function is specified during request.
        plugin: `str`
            Plugin for modifying the request and the callback based on an specific receiver message bus.

        """
        self.connection_parameter = connection_parameter
        self.request_key = request_key
        self.default_callback = default_callback

        self.plugin = plugin

    @property
    def _unique_string(self):
        return str(uuid.uuid4().hex)

    @match_typing(excep_raise=TypeError)
    def request(self, message: dict, headers=None, **kwargs):
        """Requests data from a remote PRC server.

        Parameters
        ----------
        message : dict
            representation of data to be processed remotely
        headers: dict
            additional, optional headers set to the message
        kwargs : dict
            - Can have a 'callback' key with a callable attached.
              Then, the callable will be used as callback to process the
              answer received from the remote RPC server. Otherwise
              the default_callback defined in the __init__() method will
              be used.
            - all other KV pairs of kwargs will be passed
              to the callback as parameters.

        Raises
        ------
            ValueError
        """
        reply_callback = kwargs.pop('callback', self.default_callback)
        self.__request(message=message, headers=headers, reply_callback=reply_callback, **kwargs)

    def sync_request(self, message: dict, headers: json = None,
                     reply_callback: Union[FunctionType, MethodType] = None,
                     timeout: Union[int, float] = 5000, **kwargs):

        reply_callback = reply_callback if reply_callback is not None else self.default_callback
        return self.__request(message=message, headers=headers, reply_callback=reply_callback,
                              timeout=timeout, sync=True, **kwargs)

    @match_typing(excep_raise=TypeError)
    def __request(self, *, message: dict, headers: json = None,
                  reply_callback: Union[FunctionType, MethodType] = None,
                  timeout: Union[int, float] = 5000, sync: bool = False, **kwargs):

        message_correlation_id = self._unique_string
        result_queue_name = self._unique_string
        _ready = Event()

        # create a threaded direct message consumer
        self.consumer_thread = MessageConsumer(
            connection_parameter=self.connection_parameter,
            consumer_type='direct',
            binding_keys=[result_queue_name],
            _thread_ready=_ready
        )
        if sync:
            data = Queue()

        @CallbackPlugin(plugin=self.plugin, message_correlation_id=message_correlation_id)
        def _callback(payload, headers=None, properties=None):
            if properties['correlation_id'] == message_correlation_id:
                if sync:
                    data.queue.append((payload, kwargs))
                else:
                    reply_callback(payload, **kwargs)
                self.consumer_thread.stop()
            else:
                # TODO: report bad message routing and/or wrong correlation id
                pass

        self.consumer_thread.register_message_handler(_callback)
        self.consumer_thread.start()
        _ready.wait()
        self._publish_request(message, result_queue_name=result_queue_name,
                              message_correlation_id=message_correlation_id, headers=headers)

        if sync:
            total_time = 0
            sleeping_time = .1
            while True:
                if data.queue:
                    item, kwgs = data.queue.pop()
                    return reply_callback(item, **kwgs)
                elif total_time >= timeout:
                    break
                else:
                    total_time += sleeping_time
                    time.sleep(sleeping_time)
            # to be sure that the consumer_thread is really stopped
            self.consumer_thread.stop()
            raise TimeoutError

    @RPCRequestPlugin()
    def _publish_request(self, message, *, result_queue_name, message_correlation_id, headers=None):
        with Connection(**self.connection_parameter) as connection:
            with Producer(connection) as producer:
                producer.publish(
                    body=message,
                    exchange='',
                    routing_key=self.request_key,
                    reply_to=result_queue_name,
                    correlation_id=message_correlation_id,
                    headers=headers
                )
