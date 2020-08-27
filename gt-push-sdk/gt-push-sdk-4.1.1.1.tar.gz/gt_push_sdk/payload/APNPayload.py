# -*- coding: utf-8 -*-
import sys
from enum import Enum

__author__ = 'Administrator'

import json

class AlertMsg:
    def __init__(self):
        pass
    
    def getAlertMsg(self):
        pass
    
class DictionaryAlertMsg(AlertMsg):
    def __init__(self):
        self.title = None
        self.body = None
        self.titleLocKey = None
        self.titleLocArgs = list()
        self.actionLocKey = None
        self.locKey = None
        self.locArgs = list()
        self.launchImage = None

        self.subtitle = None
        self.subtitleLocKey = None
        self.subtitleLocArgs = []

        # IOS 12 新增
        self.summaryArg = None
        self.summaryArgCount = - sys.maxsize -1
    
    def getAlertMsg(self):
        alertMap = dict()
        if self.title is not None and self.title is not "":
            alertMap["title"] = self.title
        if self.body is not None and self.body is not "":
            alertMap["body"] = self.body
        if self.titleLocKey is not None and self.titleLocKey is not "":
            alertMap["title-loc-key"] = self.titleLocKey
        if len(self.titleLocArgs) > 0:
            alertMap["title-loc-args"] = self.titleLocArgs
        if self.actionLocKey is not None and self.actionLocKey is not "":
            alertMap["action-loc-key"] = self.actionLocKey
        if self.locKey is not None and self.locKey is not "":
            alertMap["loc-key"] = self.locKey
        if len(self.locArgs) > 0:
            alertMap["loc-args"] = self.locArgs
        if self.launchImage is not None and self.launchImage is not "":
            alertMap["launch-image"] = self.launchImage
        if self.subtitle is not None and len(self.subtitle) > 0:
            alertMap["subtitle"] = self.subtitle
        if self.subtitleLocKey is not None and len(self.subtitleLocKey) > 0:
            alertMap["subtitle-loc-key"] = self.subtitleLocKey
        if len(self.subtitleLocArgs) > 0:
            alertMap["subtitle-loc-args"] = self.subtitleLocArgs
        if self.summaryArg is not None and len(self.summaryArg) > 0:
            alertMap["summary-arg"] = self.summaryArg
        if self.summaryArgCount != - sys.maxsize -1:
            alertMap["summary-arg-count"] = self.summaryArgCount
        return alertMap;
    
class SimpleAlertMsg(AlertMsg):
    def __init__(self):
        self.alertMsg = None
        
    def getAlertMsg(self):
        return self.alertMsg
    
class APNPayload:
        
    PAYLOAD_MAX_BYTES = 3072

    def __init__(self):
        self.APN_SOUND_SILENCE = "default"
        self.alertMsg = None
        self.badge = -1
        self.sound_str = "default"
        self.contentAvailable = 0
        self.category = None
        self.apnsCollapseId = None
        self.customMsg = dict()
        self.autoBadge = None
        self.voicePlayType = 0
        self.voicePlayMessage = ""

        # IOS 12 新增
        self.threadId = None
        self.sound_d = Sound_Dictionary()

        # 多媒体参数
        self.multiMedia = []

    def getPayload(self):
        try:
            apsMap = dict()
            if self.alertMsg is not None and isinstance(self.alertMsg, AlertMsg):
                msg = self.alertMsg.getAlertMsg();
                if msg is not None and len(msg) > 0 :
                    apsMap["alert"] = self.alertMsg.getAlertMsg()
            if self.autoBadge is not None:
                apsMap["autoBadge"]=self.autoBadge
            elif self.badge >= 0:
                apsMap["badge"] = self.badge
            if self.APN_SOUND_SILENCE != self.sound_str:
                if self.sound_str is not None and self.sound_str is not "":
                    apsMap["sound"] = self.sound
                else:
                    apsMap["sound"] = "default"
            # IOS 12 的 sound_d 覆盖旧的 sound
            if self.sound_d is not None and len(Sound_Dictionary.getAsMap(self.sound_d)) > 0:
                sound = dict()
                sound["name"] = self.sound_d.name
                sound["volume"] = self.sound_d.volume
                sound["critical"] = self.sound_d.critical
                apsMap["sound"] = sound
            if len(apsMap) <= 0:
                raise Exception("format error")
            if self.contentAvailable > 0:
                apsMap["content-available"] = self.contentAvailable
            if self.category is not None and self.category is not "":
                apsMap["category"] = self.category
            if self.apnsCollapseId is not None and len(self.apnsCollapseId) > 0:
                apsMap["apns-collapse-id"] = self.apnsCollapseId
            if self.threadId is not None and len(self.threadId) > 0:
                apsMap["thread-id"] = self.threadId
            tmp = dict()
            for key, value in self.customMsg.items():
                tmp[key] = value
            tmp["aps"] = apsMap

            if self.voicePlayType is 1:
                tmp['_gvp_t_'] = 1
            elif self.voicePlayType is 2 and self.voicePlayMessage is not "":
                tmp['_gvp_t_'] = 2
                tmp['_gvp_m_'] = self.voicePlayMessage
            if self.multiMedia is not None and len(self.multiMedia) > 0:
                tmp["_grinfo_"] = self.checkMultiMedias()
            return json.dumps(tmp)
        except Exception as e:
            raise Exception("create apn payload error", e)

    def addCustomMsg(self, key, value):
        if key is not None and key is not "" and value is not None:
            self.customMsg[key] = value

    def checkMultiMedias(self):
        if len(self.multiMedia) > 3:
            raise RuntimeError("MultiMedias size overlimit")
        needGeneRid = False
        rids = set()
        for media in self.multiMedia:
            if hasattr(media, "resId") is False or media.resId is None:
                needGeneRid = True
            else:
                rids.add(media.resId)

            if media.resType == 0 or media.resUrl is None:
                raise RuntimeError("MultiMedia resType and resUrl can't be null")

        if len(rids) != len(self.multiMedia):
            needGeneRid = True

        index = 0
        if needGeneRid:
            for media in self.multiMedia:
                index += 1
                media.resId = "grid" + str(index)

        return self.dumpMultiMedias()

    def dumpMultiMedias(self):
        res = []
        for media in self.multiMedia:
            res.append(media.encoder())
        return res


class Sound_Dictionary:
    def __init__(self):
        self.critical = - sys.maxsize -1
        self.name = None
        self.volume = sys.float_info.min

    def setCritical(self, critical):
        self.critical = critical
    def setName(self, name):
        self.name = name
    # 保留一位小数
    def setVolume(self,volume):
        if volume > 1.0 or volume < 0.0:
            raise RuntimeError("volume of sound_d should between 0.0 and 1.0")
        self.volume = round(volume,1)
    def getAsMap(self):
        soundMap = dict()

        if self.name is not None and len(self.name) > 0:
            soundMap['name'] = self.name
        if self.critical != - sys.maxsize -1:
            soundMap['critical'] = self.critical
        if self.volume != sys.float_info.min:
            soundMap['volume'] = self.volume
        return soundMap


class MultiMedia:
    def __int__(self):
        self.resId = None
        self.resUrl = None
        self.resType = 0
        self.isOnlyWifi = 0

    def setOnlyWifi(self, onlyWifi):
        self.isOnlyWifi = 1 if onlyWifi else 0

    def setResType(self, mediaType):
        self.resType = mediaType.value

    def encoder(self):
        res_dict = dict()
        if self.resId is not None:
            res_dict['resId'] = self.resId
        if self.resType != 0:
            res_dict['resType'] = self.resType
        if self.resUrl is not None:
            res_dict['resUrl'] = self.resUrl
        res_dict['isOnlyWifi'] = self.isOnlyWifi
        return res_dict


class MediaType(Enum):
    pic = 1
    audio = 2
    video = 3
