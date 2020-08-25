import zmq
import uuid
import threading
import time
from .config import WorkerIdentity, ZeromqConnection
import logging

logger = logging.getLogger(__name__)


class Status:
    Pending = 'pending'
    Running = 'running'
    Completed = 'completed'
    Faulted = 'faulted'
    Cancelled = 'canceled'


class AlgorithmDaemon:
    __instance = None
    __client_identity = WorkerIdentity
    __zmq_context = zmq.Context()
    # pylint: disable=maybe-no-member
    __zmq_client = __zmq_context.socket(zmq.DEALER)
    # pylint: disable=maybe-no-member
    __zmq_client.setsockopt(zmq.IDENTITY, __client_identity.encode())
    __is_safe_exit = False

    @staticmethod
    def get_instance():
        if AlgorithmDaemon.__instance == None:
            AlgorithmDaemon()
        return AlgorithmDaemon.__instance

    def __init__(self):
        if AlgorithmDaemon.__instance != None:
            raise Exception("This class is singleton!")
        else:
            AlgorithmDaemon.__instance = self

        self.__status = Status.Pending
        logger.info(f"Instantiate daemon {WorkerIdentity}, "
                    f" connection agent service {ZeromqConnection}")
        self.__zmq_client.connect(ZeromqConnection)
        self.__client_recv_thread = threading.Thread(
            target=self.__on_client_recv)
        self.__client_recv_thread.daemon = True
        self.__client_recv_thread.start()
        self.__send_status()
        self.__establist_connect()

    def shutdown(self):
        logger.info("Daemon ready to shutdown.")
        self.__status = Status.Completed
        self.__send_status()
        self.wait_to_exit(10)

    def __on_client_recv(self):
        while not self.__is_safe_exit:
            msgs = self.__zmq_client.recv_multipart()
            if len(msgs) <= 0:
                raise ValueError("Can not recv empty message.")

            action, *msgs = msgs
            self.__handle_action(action, *msgs)

    def __send(self, *args):
        logger.info('Sending message: {}'.format(
            '-'.join([msg for msg in args if msg])))
        messages = []
        messages.extend([x.encode() for x in args])
        try:
            self.__zmq_client.send_multipart(messages)
        except zmq.ZMQError as e:
            if e.errno == zmq.EAGAIN:
                logger.warn(
                    f'occur eagain erro, wait 1 seconds, and try sending again. {str(e)}')
                time.sleep(1)
                self.__zmq_client.send_multipart(messages)

    def __send_status(self, message=''):
        self.__send('status', self.__status, message)

    def __establist_connect(self):
        logger.info("Established connection to agent service.")
        self.__status = Status.Running
        self.__send_status()

    def __handle_action(self, action, *args):
        if not action:
            raise ValueError("Action can not be empty.")
        if action != b'ack':
            raise ValueError(f"Action is not ack, [{action}] ")

        (ack_action, *args) = args
        logger.info(
            f"Agent service acknowledged successful [{action}] [{ack_action}].")

        if ack_action == b'status':
            status = args[0].decode('utf8')
            logger.info(f"Agent service ack status [{status}]")
            if status == Status.Completed or status == Status.Faulted:
                logger.info(f"worker can exit safely.")
                self.__is_safe_exit = True

    def report_progress(self, progress):
        if progress < 0 or progress > 1:
            raise ValueError("Progress {0} is incorrect.".format(progress))
        self.__send('progress', str(progress))

    def on_failed(self, exception):
        logger.error(exception)
        self.__status = Status.Faulted
        self.__send_status(str(exception))
        self.wait_to_exit(10)

    def wait_to_exit(self, timeout):
        start = time.time()
        while not self.__is_safe_exit and time.time() - start < timeout:
            time.sleep(0.1)
        if self.__is_safe_exit:
            logger.info("worker eixt.")
        else:
            logger.info("worker exit with timeout.")
