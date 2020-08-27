from typing import List


class ReportInit(object):
    """
    Report job that will be encapsulated inside an UDP packet
    and send to ONOS controller by a monitor host
    """

    def __init__(self, packet_type: str, measurement: str, tags: List[str], fields: List[str],
                 timestamp: int):
        self.type = packet_type
        self.measurement = measurement
        self.tags = tags
        self.fields = fields
        self.timestamp = timestamp

    def __str__(self):
        return "[{}] {},{} {} {}".format(str(self.type),
                                         str(self.measurement),
                                         ','.join(self.tags),
                                         ','.join(self.fields),
                                         str(self.timestamp))

    def __repr__(self):
        return "{}({},{} {} {})".format(self.__class__.__name__,
                                        str(self.measurement),
                                        ','.join(self.tags),
                                        ','.join(self.fields),
                                        str(self.timestamp))
