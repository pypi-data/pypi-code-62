from google.protobuf.json_format import MessageToJson
import PeriodicPositionProto_pb2
import CellocatorModularType11Proto_pb2
import requests
from datetime import datetime
import json
import base64
import uuid


class MProfiler(object):

    def __init__(self, url, user="", passw=""):
        self._profiler = url
        self._username = user
        self._password = passw

    def get_messages(self):
        url = self._profiler+"/v1/MessageBatch"
        obj = requests.get(url, auth=(self._username, self._password))
        batch = {}
        if obj is not None and obj.status_code == 200:
            res = obj.json()
            events = []
            for message in res["messages"]:
                event = self.choose_template(message["templateId"])
                binary = base64.b64decode(message["body"])
                event.ParseFromString(binary)
                parsed = json.loads(MessageToJson(event, True))
                events.append(parsed)
            batch["events"] = events
            batch["batchId"] = res["batchId"]
            batch["date"] = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        return batch

    def post_message(self, message):
        url = self._profiler+"/v1/messages"
        message["batch_id"] = uuid.uuid1()
        obj = requests.post(url, auth=(self._username, self._password), data=message)
        return obj

    def acknowledge(self, batch):
        url = self._profiler + "/v1/MessageBatch/Ack/"+batch
        obj = requests.post(url, auth=(self._username, self._password))
        if obj.status_code == 200:
            return True
        else:
            return False

    def periodic_position(self, header, position):
        event = PeriodicPositionProto_pb2.PeriodicPosition()
        event.header.TemplateId = 1
        for key in header:
            event.header[key] = header[key]
        for key in position:
            event[key] = position[key]
        return base64.b64encode(event.SerializeToString())

    def choose_template(self, template_id):
        event = None
        if template_id == 1078:
            event = CellocatorModularType11Proto_pb2.CellocatorModularType11()
        else:
            event = PeriodicPositionProto_pb2.PeriodicPosition()
        return event

