import json

class BasePacket(object):

    __slots__ = ()

    def to_json(self):
        return json.dumps(self.to_dict())

class CommandPacket(BasePacket):

    __slots__ = ('cmd', 'name', 'id', 'data')

    def __init__(self, cmd=None, name=None, id=None, data=None):

        self.cmd = cmd
        self.name = name
        self.id = id
        self.data = data

    def to_dict(self):
        return dict(
            cmd = self.cmd,
            name = self.name,
            id = self.id,
            data = self.data
        )

    @classmethod
    def from_dict(cls, data):
        return CommandPacket(
            cmd = data.get("cmd"),
            name = data.get("name"),
            id = data.get("id"),
            data = data.get("data")
        )

class ResponsePacket(BasePacket):

    __slots__ = ( 'ok', 'msg', 'devices' )

    def __init__(self, ok=True, msg=None, devices=None):

        self.ok = ok
        self.msg = msg
        self.devices = devices

    def to_dict(self):

        data = dict(
            ok = self.ok
        )

        if self.devices is not None:
            data["devices"] = self.devices
        if self.msg is not None:
            data["msg"] = self.msg

        return data

