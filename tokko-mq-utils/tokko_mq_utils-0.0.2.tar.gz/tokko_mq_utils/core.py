from typing import Any, Union
import json

from pika import URLParameters, BlockingConnection


__all__ = [
    'MQPublisher',
    'MQConsumer',
]


class MQConnection:

    def __init__(self, broker_url: str, queue: str, **options):
        self.broker_url = broker_url
        self.queue_name = queue
        self.exchange = options.get("exchange", "")
        self.routing_key = options.get("routing_key", self.queue_name)
        self.durable_queue = options.get("durable_queue", False),
        self.passive_connection = options.get("passive_connection", False)
        self.auto_ack = options.get("auto_ack", True)
        self.callback_function = options.get("callback_function")
        if not all([
            self.broker_url,
            self.queue_name,
            all([
                isinstance(self.broker_url, str),
                isinstance(self.queue_name, str),
                isinstance(self.exchange, str),
                isinstance(self.routing_key, str),
            ]),
        ]):
            raise ValueError("Missing RabbitMQ connection settings")
        self.conn_settings = URLParameters(self.broker_url)

    def get_blocking_conn(self):
        self.durable_queue = True
        self.passive_connection = False
        return self.connection

    @property
    def connection(self) -> Any:
        conn = BlockingConnection(self.conn_settings)
        channel = conn.channel()
        channel.queue_declare(
            queue=self.queue_name,
            durable=self.durable_queue,
            passive=self.passive_connection
        )
        return channel

    def disconnect(self) -> bool:
        """Close connection"""
        if self.connection:
            self.connection.close()
            return True
        raise RuntimeError("Connection is not already established")


class MQConsumer(MQConnection):

    def pop_message(self) -> Union[tuple, None]:
        connection = BlockingConnection(URLParameters(self.broker_url))
        channel = connection.channel()
        queue_state = channel.queue_declare(self.queue_name, durable=True, passive=True)
        queue_is_empty = queue_state.method.message_count == 0
        if not queue_is_empty:
            m, prop, body = channel.basic_get(self.queue_name, auto_ack=True)
            self.disconnect()
            if self.callback_function:
                return self.callback_function(m, prop, body)
            return m, prop, body

    def consume(self, prefetch_count: int = None):
        conn = self.get_blocking_conn()
        if not self.callback_function:
            raise RuntimeError("Callback function not found.")
        conn.basic_qos(prefetch_count=prefetch_count or 1)
        callback_fn = self.callback_function
        conn.basic_consume(queue='task_queue', on_message_callback=callback_fn)


class MQPublisher(MQConnection):

    def safe_submit(self, message: Any, encoding=None) -> None:
        """Submit message <Any> to RabbitMQ"""
        if isinstance(message, (list, dict)):
            message = json.dumps(message)
        if not isinstance(message, str):
            message = f"{message}"
        self.submit(
            message.encode(encoding=encoding or "utf8")
        )

    def submit(self, message: bytes) -> None:
        """Submit message <bytes> to RabbitMQ"""
        if not isinstance(message, bytes):
            raise TypeError(f"Expected message as bytes instance,"
                            f" got {type(message)} instead.")
        self.connection.basic_publish(
            exchange=self.exchange,
            routing_key=self.routing_key,
            body=message
        )


