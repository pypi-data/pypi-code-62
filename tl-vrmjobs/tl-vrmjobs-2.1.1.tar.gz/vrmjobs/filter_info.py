from typing import List, Dict


class FilterInfo(object):
    """
    Filter criterion that defined by each host to provide extra information
    to the prometheus query
    """
    def __init__(self, category: str, criteria: List[Dict[str, str]]):
        self.category = category
        self.criteria = criteria

    def __str__(self):
        return "{} - {}".format(self.category, self.criteria)
