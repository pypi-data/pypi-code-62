import json
from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4


def criteria_matches(criteria: dict, instance):
    for k in criteria:
        if k not in instance.__dict__:
            raise ValueError("%s is not a valid property %s" % (k, type(instance)))
    for k, v in criteria.items():
        if getattr(instance, k) != v:
            return False
        elif k == "Timestamp" and getattr(instance, k) < v:
            return False
    return True


class FilterableList(list):
    def filter(self, criteria):
        if not criteria:
            return self
        f_list = FilterableList()
        for item in self:
            if criteria_matches(criteria, item):
                f_list.append(item)
        return f_list


class Level(str, Enum):
    ERROR = 'ERROR'
    WARNING = 'WARNING'


class ProcessOutput:
    """
    A ProcessOutput object with TimeStamp, Level, Location abd Message as compulsory data.
    """

    def __init__(self, level, message, line_number=None, resource_name=None, test_name=None,
                 region=None, stack_name=None):
        self.Timestamp: datetime = datetime.now()
        self.Level: Level = level
        if line_number:
            self.Location: str = line_number
        self.Message = message
        if test_name:
            self.TestName: str = test_name
        if stack_name:
            self.StackName: str = stack_name
        if region:
            self.Region = region
        if resource_name:
            self.Resource = resource_name

    def __str__(self):
        return "{} {} {}".format(self.Timestamp, self.Level, self.Message)

    def __repr__(self):
        return "<Event object {} at {}>".format(self.Message, hex(id(self)))


class ProcessOutputs(FilterableList):
    pass


class Stacks(FilterableList):
    pass


class Resource:
    def __init__(self, resource_dict: dict):
        self.logical_id: str = resource_dict["LogicalResourceId"]
        self.type: str = resource_dict["ResourceType"]
        self.status: str = resource_dict["ResourceStatus"]
        self.physical_id: str = ""
        self.last_updated_timestamp: datetime = datetime.fromtimestamp(0)
        self.status_reason: str = ""
        if "PhysicalResourceId" in resource_dict.keys():
            self.physical_id = resource_dict["PhysicalResourceId"]
        if "LastUpdatedTimestamp" in resource_dict.keys():
            self.last_updated_timestamp = resource_dict["LastUpdatedTimestamp"]
        if "ResourceStatusReason" in resource_dict.keys():
            self.status_reason = resource_dict["ResourceStatusReason"]

    def __str__(self):
        return "<Resource {} {}>".format(self.logical_id, self.status)


class Resources(FilterableList):
    pass


class Event:
    def __init__(self, event_dict: dict):
        self.event_id: str = event_dict["EventId"]
        self.stack_name: str = event_dict["StackName"]
        self.logical_id: str = event_dict["LogicalResourceId"]
        self.type: str = event_dict["ResourceType"]
        self.status: str = event_dict["ResourceStatus"]
        self.physical_id: str = ""
        self.timestamp: datetime = datetime.fromtimestamp(0)
        self.status_reason: str = ""
        self.properties: dict = {}
        if "PhysicalResourceId" in event_dict.keys():
            self.physical_id = event_dict["PhysicalResourceId"]
        if "Timestamp" in event_dict.keys():
            self.timestamp = event_dict["Timestamp"]
        if "ResourceStatusReason" in event_dict.keys():
            self.status_reason = event_dict["ResourceStatusReason"]
        if "ResourceProperties" in event_dict.keys():
            self.properties = json.loads(event_dict["ResourceProperties"])

    def __str__(self):
        return "{} {} {}".format(self.timestamp, self.logical_id, self.status)

    def __repr__(self):
        return "<Event object {} at {}>".format(self.event_id, hex(id(self)))


class Events(FilterableList):
    pass


class Output:
    def __init__(self, output_dict: dict):
        self.key: str = output_dict["OutputKey"]
        self.value: str = output_dict["OutputValue"]
        self.description: str = ""
        self.export_name: str = ""
        if "Description" in output_dict.keys():
            self.description = output_dict["Description"]
        if "ExportName" in output_dict.keys():
            self.export_name = output_dict["ExportName"]


class Outputs(FilterableList):
    pass
