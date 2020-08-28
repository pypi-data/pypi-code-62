import uuid
import threading
import time
import logging
import grpc

from .WorkerBroker_pb2_grpc import WorkerBrokerStub
from .config import WorkerIdentity, GrpcHost, GrpcPort
from .WorkerBroker_pb2 import ReportStatusRequest, ReportProgressRequest

logger = logging.getLogger(__name__)


class AlgorithmDaemon:
    __instance = None
    __client_identity = WorkerIdentity

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

        logger.info(f"Instantiate daemon {WorkerIdentity}, "
                    f" connection agent service {GrpcHost}:{GrpcPort}")
        self.__channel = grpc.insecure_channel(
            f'{GrpcHost}:{GrpcPort}')
        self.__worker_stub = WorkerBrokerStub(
            self.__channel)
        # pylint: disable=maybe-no-member
        self.__worker_stub.ReportStatus(ReportStatusRequest(
            clientAddress=WorkerIdentity,
            status=ReportStatusRequest.Pending))
        self.__establist_connect()

    def shutdown(self):
        logger.info("Daemon ready to shutdown.")
        # pylint: disable=maybe-no-member
        self.__worker_stub.ReportStatus(ReportStatusRequest(
            clientAddress=WorkerIdentity,
            status=ReportStatusRequest.Completed))

    def __establist_connect(self):
        logger.info("Established connection to agent service.")
        # pylint: disable=maybe-no-member
        self.__worker_stub.ReportStatus(ReportStatusRequest(
            clientAddress=WorkerIdentity,
            status=ReportStatusRequest.Running))

    def report_progress(self, progress):
        if progress < 0 or progress > 1:
            raise ValueError("Progress {0} is incorrect.".format(progress))
         # pylint: disable=maybe-no-member
        self.__worker_stub.ReportProgress(ReportProgressRequest(
            clientAddress=WorkerIdentity,
            progress=progress))

    def on_failed(self, exception):
        logger.error(exception)
        # pylint: disable=maybe-no-member
        self.__worker_stub.ReportStatus(ReportStatusRequest(
            clientAddress=WorkerIdentity,
            status=ReportStatusRequest.Faulted,
            message=str(exception)))
