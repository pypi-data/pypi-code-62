from .filter_info import FilterInfo
from .vrm_type import VrmType
from typing import List


class QueryAck(object):
    """
    System job that will be encapsulated inside an UDP packet and send to the monitor host
    after the collector host successfully initialized the metric exporters of a worker.
    """

    def __init__(self, packet_id: str, hostname: str, job: str, filters: List['FilterInfo'], packet_type: 'VrmType'):
        self.packet_id = packet_id
        self.hostname = hostname
        self.job = job
        self.filters = filters
        self.type = packet_type

    def __str__(self):
        filter_str = ""
        for f in self.filters:
            filter_str += "{} ".format(str(f))
        return "[{}] {} - job: {} - filters: {}".format(str(self.type),
                                                        self.hostname,
                                                        self.job,
                                                        filter_str)

    def __repr__(self):
        filter_str = ""
        for f in self.filters:
            filter_str += "{} ".format(str(f))
        return "{}({} - job: {} - filters: {})".format(self.__class__.__name__,
                                                       self.hostname,
                                                       self.job,
                                                       filter_str)
