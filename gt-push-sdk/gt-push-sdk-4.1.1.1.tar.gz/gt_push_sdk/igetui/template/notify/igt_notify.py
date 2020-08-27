from enum import Enum

class Notify():
    def __init__(self):
        self.title = None
        self.content = None
        self.payload = None
        self.type = None
        self.url=None
        self.intent=None
        self.extKVList = []

    def setTitle(self, title):
        self.title = title
    def getTitle(self):
        return self.title
    def setContent(self, content):
        self.content = content
    def getContent(self):
        return self.content
    def setPayload(self, payload):
        self.payload = payload
    def getPayload(self):
        return self.payload
    def setType(self, type):
        self.type = type
    def getType(self):
        return self.type
    def setUrl(self, url):
        self.url = url
    def getUrl(self):
        return self.url
    def setIntent(self, intent):
        self.intent = intent
    def getIntent(self):
        return self.intent
    def getExtKv(self):
        return self.extKVList
    def addExtKVToAll(self, key ,value):
        self.extKVList.append(ExtKV.setExtKv(ExtKV(), key, value, PLATFORM_CONSTRAINS.ALL.name))
    def addHWExtKV(self, key ,value):
        self.extKVList.append(ExtKV.setExtKv(ExtKV(), key, value, PLATFORM_CONSTRAINS.HW.name))
    def addXMExtKV(self, key ,value):
        self.extKVList.append(ExtKV.setExtKv(ExtKV(), key, value, PLATFORM_CONSTRAINS.XM.name))
    def addMZExtKV(self, key ,value):
        self.extKVList.append(ExtKV.setExtKv(ExtKV(), key, value, PLATFORM_CONSTRAINS.MZ.name))
    def addOPExtKV(self, key ,value):
        self.extKVList.append(ExtKV.setExtKv(ExtKV(), key, value, PLATFORM_CONSTRAINS.OP.name))
    def addVVExtKV(self, key ,value):
        self.extKVList.append(ExtKV.setExtKv(ExtKV(), key, value, PLATFORM_CONSTRAINS.VV.name))
    def addFCMExtKV(self, key ,value):
        self.extKVList.append(ExtKV.setExtKv(ExtKV(), key, value, PLATFORM_CONSTRAINS.FCM.name))



class ExtKV():
    def __init__(self):
        self.key = ""
        self.value = ""
        self.constains = PLATFORM_CONSTRAINS.ALL.name

    def setExtKv(self,key,value,constrains):
        self.key = key
        self.value = value
        self.constains = constrains

        return self


class PLATFORM_CONSTRAINS(Enum):
    HW = 0
    XM = 1
    MZ = 2
    OP = 3
    VV = 4
    FCM = 5
    ALL = 6
