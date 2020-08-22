from .filter_info import FilterInfo
from typing import List


class QueryInfo(object):
    """
    Define structure of the information of a pair job-filters that
    will be exchanged via probe packets from worker/collector/monitor host
    """
    def __init__(self, job: str, filters: List['FilterInfo']):
        self.job = job
        self.filters = filters

    def __str__(self):
        filter_str = ""
        for f in self.filters:
            filter_str += "{} ".format(str(f))
        return "{} {}".format(self.job, filter_str)

    def __repr__(self):
        filter_str = ""
        for f in self.filters:
            filter_str += "{}".format(str(f))
        return "{}({} {})".format(self.__class__.__name__, self.job, filter_str)
