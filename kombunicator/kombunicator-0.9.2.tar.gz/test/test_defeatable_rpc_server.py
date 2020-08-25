
from threading import Event
from uuid import uuid4
import time
import queue

from test import broker_connection_parameter, celery_app
from test.rpc_server import defeat_rpc_processor_name

from kombunicator import RPCServer, RPCClient


received_messages = queue.Queue()


def defeat_answer_processor(data):
    received_messages.put(data)
    print(f"\n\nanswer_processor {data.get('index')}, {data.get('processed')}, {received_messages.qsize()}")


class Test_DefeatableRPCServer:
    listening_key = 'defeat_rpc_key'
    received_messages = list()

    def setup_server(self):
        self.server_ready = Event()
        self.server = RPCServer(
            connection_parameter=broker_connection_parameter,
            listening_key=self.listening_key,
            celery_app=celery_app,
            processing_task_name=defeat_rpc_processor_name,
            ready=self.server_ready
        )

    def start_server(self):
        self.server.start()
        self.server_ready.wait()
        self.server_ready.clear()

    def stop_server(self):
        is_stopped = Event()
        self.server.stop(ready=is_stopped)
        is_stopped.wait()
        self.server.join()

    def get_rpc_client(self):
        client = RPCClient(
            connection_parameter=broker_connection_parameter,
            request_key=self.listening_key,
            default_callback=defeat_answer_processor
        )
        return client

    def test_defeatable_server(self):
        self.setup_server()
        self.start_server()

        client = self.get_rpc_client()

        # put messages while server is running
        for i in range(5):
            data = dict(index=i, unique=uuid4().hex)
            client.request(data)

        # give time for the messages to arrive
        time.sleep(2)
        assert received_messages.qsize() == 5

        # turn off server, put another 5 messages.
        # length of list must remain 5
        self.stop_server()
        for j in range(5):
            data = dict(index=i + j + 1, unique=uuid4().hex)
            client.request(data)

        # give time for the messages to arrive
        time.sleep(2)
        assert received_messages.qsize() == 5

        # turn on server again, put no new messages
        self.setup_server()
        self.start_server()
        # give time for the messages to arrive
        time.sleep(2)
        assert received_messages.qsize() == 10
