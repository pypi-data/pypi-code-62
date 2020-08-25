
from threading import Thread, Event
from types import FunctionType, MethodType
from typing import Union

from kombu import Connection
from strongtyping.strong_typing import match_typing

from kombunicator.DirectConsumer import DirectConsumer
from kombunicator.TopicConsumer import TopicConsumer
from kombunicator.FanoutConsumer import FanoutConsumer


class MessageConsumer(Thread):

    @match_typing
    def __init__(self, connection_parameter: dict = {}, consumer_type: str = 'direct', exchange_name='',
                 binding_keys: list = [], q_unique=None, accept: list = ['json'],
                 _thread_ready=None, is_rpc=False):
        super().__init__()
        self.daemon = True

        self.connection_parameter = connection_parameter
        self.consumer_type = consumer_type
        self.binding_keys = binding_keys
        self.accept = accept
        self._thread_ready = _thread_ready
        self._is_rpc_server = is_rpc

        if self.consumer_type == 'topic':
            assert type(exchange_name) is str, "'exchange_name' must be string"
            assert type(q_unique) is str, "'q_unique' must be string"

        if self.consumer_type == 'fanout':
            assert type(exchange_name) is str, "'exchange_name' must be string"

        self.exchange_name = exchange_name
        self.q_unique = q_unique

    @match_typing
    def register_message_handler(self, msg_handler: Union[FunctionType, MethodType]):
        self.msg_handler = msg_handler

    def _create_consumer(self, connection):

        consumer_base_params = {
            'connection': connection,
            'accept': self.accept
        }

        if self.consumer_type == 'topic':
            self.consumer = TopicConsumer(
                exchange_name=self.exchange_name,
                binding_keys=self.binding_keys,
                q_unique=self.q_unique,
                **consumer_base_params
            )
            self.consumer.process_message = MethodType(self.msg_handler, TopicConsumer)

        elif self.consumer_type == 'direct':
            self.consumer = DirectConsumer(
                binding_key=self.binding_keys[0],
                is_rpc_server=self._is_rpc_server,
                **consumer_base_params
            )
            self.consumer.process_message = self.msg_handler

        elif self.consumer_type == 'fanout':
            self.consumer = FanoutConsumer(
                exchange_name=self.exchange_name,
                binding_keys=self.binding_keys,
                **consumer_base_params
            )
            self.consumer.process_message = MethodType(self.msg_handler, FanoutConsumer)

        else:
            raise ValueError("consumer_type must be either 'direct' or 'topic' or 'fanout'")

        # set ready event if consumer is ready to accept messages
        def _on_consume_ready(connection, channel, consumers, th_ready=self._thread_ready):
            th_ready.set()

        self.consumer.on_consume_ready = _on_consume_ready

    def run(self):
        """
        Starts the RabbitMQ consumer. This call will be blocking.
        """
        with Connection(**self.connection_parameter) as conn:
            self._create_consumer(conn)
            self.consumer.run()

    def stop(self, ready=None):
        """
        Causes the RabbitMQ consumer to stop consuming
        and return. After that, the thread can be joined.
        """
        if ready is not None and isinstance(ready, Event):
            self._consumer_stopped = ready

            # create a callback routine which sets the stop-event and
            # attach it to the (currently running) consumer.
            def _on_consume_end(connection, channel, stop_event=self._consumer_stopped):
                stop_event.set()
            self.consumer.on_consume_end = _on_consume_end

        self.consumer.should_stop = True
