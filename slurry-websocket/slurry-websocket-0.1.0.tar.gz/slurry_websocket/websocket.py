"""Slurry websocket client."""

from slurry import Section
import trio
from trio_websocket import open_websocket, open_websocket_url
import ujson

CONN_TIMEOUT = 60 # default connect & disconnect timeout, in seconds
MESSAGE_QUEUE_SIZE = 1
MAX_MESSAGE_SIZE = 2 ** 20 # 1 MiB
RECEIVE_BYTES = 4 * 2 ** 10 # 4 KiB

class Websocket(Section):
    """A websocket section.

    .. Note::
        Do not instantiate Websocket sections manually. Instead, use the factory methods
        :meth:`create_websocket` or :meth:`create_websocket_url`.
    :raises HandshakeError: for any networking error,
        client-side timeout (ConnectionTimeout, DisconnectionTimeout),
        or server rejection (ConnectionRejected) during handshakes.
    """
    def __init__(self):
        super().__init__()
        self.ws = None
        self.dumps = True
        self.loads = True

    @classmethod
    def create_websocket(cls, host, port, resource, *, use_ssl, subprotocols=None,
        extra_headers=None,
        message_queue_size=MESSAGE_QUEUE_SIZE, max_message_size=MAX_MESSAGE_SIZE,
        connect_timeout=CONN_TIMEOUT, disconnect_timeout=CONN_TIMEOUT,
        dumps=True, loads=True):
        '''
        Create a WebSocket client connection to a host.

        The websocket will connect when the pipeline is started.

        :param str host: The host to connect to.
        :param int port: The port to connect to.
        :param str resource: The resource, i.e. URL path.
        :param use_ssl: If this is an SSL context, then use that context. If this is
            ``True`` then use default SSL context. If this is ``False`` then disable
            SSL.
        :type use_ssl: bool or ssl.SSLContext
        :param subprotocols: An iterable of strings representing preferred
            subprotocols.
        :param list[tuple[bytes,bytes]] extra_headers: A list of 2-tuples containing
            HTTP header key/value pairs to send with the connection request. Note
            that headers used by the WebSocket protocol (e.g.
            ``Sec-WebSocket-Accept``) will be overwritten.
        :param int message_queue_size: The maximum number of messages that will be
            buffered in the library's internal message queue.
        :param int max_message_size: The maximum message size as measured by
            ``len()``. If a message is received that is larger than this size,
            then the connection is closed with code 1009 (Message Too Big).
        :param float connect_timeout: The number of seconds to wait for the
            connection before timing out.
        :param float disconnect_timeout: The number of seconds to wait when closing
            the connection before timing out.
        :param bool dumps: Unpack json output.
        :param bool loads: Pack json input.
        '''
        websocket = cls()
        websocket.ws = open_websocket(host, port, resource,
            use_ssl=use_ssl, subprotocols=subprotocols,
            extra_headers=extra_headers,
            message_queue_size=message_queue_size, max_message_size=max_message_size,
            connect_timeout=connect_timeout, disconnect_timeout=disconnect_timeout)
        websocket.dumps = dumps
        websocket.loads = loads

        return websocket

    @classmethod
    def create_websocket_url(cls, url, ssl_context=None, *, subprotocols=None,
        extra_headers=None,
        message_queue_size=MESSAGE_QUEUE_SIZE, max_message_size=MAX_MESSAGE_SIZE,
        connect_timeout=CONN_TIMEOUT, disconnect_timeout=CONN_TIMEOUT,
        dumps=True, loads=True):
        '''
        Create a WebSocket client connection to a URL.

        The websocket will connect when the pipeline is started.

        :param str url: A WebSocket URL, i.e. `ws:` or `wss:` URL scheme.
        :param ssl_context: Optional SSL context used for ``wss:`` URLs. A default
            SSL context is used for ``wss:`` if this argument is ``None``.
        :type ssl_context: ssl.SSLContext or None
        :param subprotocols: An iterable of strings representing preferred
            subprotocols.
        :param list[tuple[bytes,bytes]] extra_headers: A list of 2-tuples containing
            HTTP header key/value pairs to send with the connection request. Note
            that headers used by the WebSocket protocol (e.g.
            ``Sec-WebSocket-Accept``) will be overwritten.
        :param int message_queue_size: The maximum number of messages that will be
            buffered in the library's internal message queue.
        :param int max_message_size: The maximum message size as measured by
            ``len()``. If a message is received that is larger than this size,
            then the connection is closed with code 1009 (Message Too Big).
        :param float connect_timeout: The number of seconds to wait for the
            connection before timing out.
        :param float disconnect_timeout: The number of seconds to wait when closing
            the connection before timing out.
        :param bool dumps: Unpack json output.
        :param bool loads: Pack json input.        
        '''
        websocket = cls()
        websocket.ws = open_websocket_url(url,
            ssl_context=ssl_context, subprotocols=subprotocols,
            extra_headers=extra_headers,
            message_queue_size=message_queue_size, max_message_size=max_message_size,
            connect_timeout=connect_timeout, disconnect_timeout=disconnect_timeout)
        websocket.dumps = dumps
        websocket.loads = loads

        return websocket


    async def pump(self, input, output):
        async def send_task():
            send_message = self.ws.send_message
            receive = input.receive
            while True:
                await send_message(await receive())

        async def send_json_task():
            send_message = self.ws.send_message
            receive = input.receive
            while True:
                await send_message(ujson.dumps(await receive()))

        async def receive_task():
            receive_message = self.ws.receive_message
            send = output.send
            while True:
                await send(await receive_message())

        async def receive_json_task():
            receive_message = self.ws.receive_message
            send = output.send
            while True:
                await send(ujson.loads(await receive_message()))

        async with self.ws, trio.open_nursery() as nursery:
            if self.dumps:
                nursery.start_soon(send_json_task)
            else:
                nursery.start_soon(send_task)
            if self.loads:
                nursery.start_soon(receive_json_task)
            else:
                nursery.start_soon(receive_task)
