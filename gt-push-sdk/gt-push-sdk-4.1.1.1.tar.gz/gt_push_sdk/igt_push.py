# -*- coding: utf-8 -*-
from gt_push_sdk.igetui.utils.igt_domain_manager import PushDomainManager
from gt_push_sdk.igetui.utils.igt_domain_wrapper import OSDomainWrapper

__author__ = 'wei'

import io
import gzip
import hashlib
# import urllib2
import threading

import requests

from .BatchImpl import *
from .RequestException import RequestException, GtHttpException
from gt_push_sdk.igetui.igt_message import *
from gt_push_sdk.igetui.utils.igt_lang_utils import LangUtils

globals = {
    'false': "false",
    'true': "true",
    'null': "null"
}


class IGeTui:
    serviceMap = dict()
    session = requests.session()
    pushMap = dict()
    push = None
    __pushMapLock__ = threading.Lock()

    def __init__(self, host, appKey, masterSecret, ssl=None):
        self.appKey = appKey
        self.masterSecret = masterSecret
        key = host + "|" + appKey + "|" + str(ssl if ssl is not None else False)
        self.domainKey = key
        if not IGeTui.pushMap.__contains__(key):
            with IGeTui.__pushMapLock__:
                if not IGeTui.pushMap.__contains__(key):
                    IGeTui.pushMap[key] = GtPush(host, appKey, masterSecret, key, ssl)
        IGeTui.push = IGeTui.pushMap.get(key)

    def cycleInspect(self):
        if len(IGeTui.serviceMap[self.appKey]) == 0:
            raise ValueError("can't get fastest host from empty list")
        else:
            t = threading.Timer(GtConfig.getHttpInspectInterval(), self.getFastUrl)
            t.setDaemon(True)
            t.start()

    def connect(self):
        timestamp = self.getCurrentTime()
        sign = self.getSign(self.appKey, timestamp, self.masterSecret)
        params = dict()
        params['action'] = 'connect'
        params['appkey'] = self.appKey
        params['timeStamp'] = timestamp
        params['sign'] = sign
        params['version'] = GtConfig.getSDKVersion()

        rep = IGeTui.push.domainManager.httpPost(IGeTui.push.domainManager.getFastUrl(self.domainKey), params)

        if 'success' == (rep['result']):
            if 'authtoken' in rep:
                IGeTui.push.authToken = rep['authtoken']
            return True

        raise Exception(str(rep) + "appKey or masterSecret is auth failed.")

    def getBatch(self):
        return BatchImpl(self, self.appKey, self)

    def pushMessageToSingle(self, message, target, requestId=None):
        params = dict()
        if requestId is None:
            requestId = str(uuid.uuid1())
        params['requestId'] = requestId
        params['action'] = "pushMessageToSingleAction"
        params['appkey'] = self.appKey
        transparent = message.data.getTransparent()
        params['clientData'] = str(base64.b64encode(transparent.SerializeToString()), encoding='utf-8')
        params['transmissionContent'] = message.data.transmissionContent
        params['isOffline'] = message.isOffline
        params['offlineExpireTime'] = message.offlineExpireTime
        # 增加pushNetWorkType参数(0:不限;1:wifi;2:4G/3G/2G)
        params["pushNetWorkType"] = message.pushNetWorkType
        params['appId'] = target.appId
        params['clientId'] = target.clientId
        params['alias'] = target.alias
        params['type'] = 2  # default is message
        params['pushType'] = message.data.pushType

        return self.httpPostFast(params)

    def pushAPNMessageToSingle(self, appId, deviceToken, message):
        if deviceToken is None or len(deviceToken) != 64:
            raise Exception("deviceToken " + deviceToken + " length must be 64.")
        params = dict()
        params['action'] = "apnPushToSingleAction"
        params['appId'] = appId
        params['appkey'] = self.appKey
        params['DT'] = deviceToken
        params['PI'] = base64.encodestring(message.data.pushInfo.SerializeToString())

        return self.httpPostFast(params)

    def pushMessageToApp(self, message, taskGroupName=None):
        params = dict()
        contentId = self.getContentId(message, taskGroupName)
        params['action'] = "pushMessageToAppAction"
        params['appkey'] = self.appKey
        params['contentId'] = contentId
        params['type'] = 2
        return self.httpPostFast(params)

    def pushMessageToAppWithContentId(self, contentId):
        params = dict()
        params['action'] = "pushMessageToAppAction"
        params['appkey'] = self.appKey
        params['contentId'] = contentId
        params['type'] = 2
        return self.httpPostFast(params)

    def pushMessageToList(self, contentId, targets):
        params = dict()
        params['action'] = 'pushMessageToListAction'
        params['appkey'] = self.appKey
        params['contentId'] = contentId
        needDetails = GtConfig.isPushListNeedDetails()
        params['needDetails'] = GtConfig.isPushListNeedDetails()
        isasync = GtConfig.isPushListAsync()
        params["async"] = isasync

        if isasync and not needDetails:
            limit = GtConfig.getAsyncListLimit()
        else:
            limit = GtConfig.getSyncListLimit()

        if len(targets) > limit:
            raise AssertionError("target size:" + str(len(targets)) + " beyond the limit:" + str(limit))

        clientIdList = []
        aliasList = []
        appId = ''
        for target in targets:
            clientId = target.clientId.strip()
            alias = target.alias.strip()
            if clientId != '':
                clientIdList.append(clientId)
            elif alias != '':
                aliasList.append(alias)

            if appId == '':
                appId = target.appId.strip()

        params['appId'] = appId
        params['clientIdList'] = clientIdList
        params['aliasList'] = aliasList
        params['type'] = 2
        return self.httpPostFast(params, True)

    def pushAPNMessageToList(self, appId, contentId, deviceTokenList):
        for deviceToken in deviceTokenList:
            if deviceToken is None or len(deviceToken) != 64:
                raise Exception("deviceToken " + deviceToken + " length must be 64.")

        params = dict()
        params['action'] = "apnPushToListAction"
        params['appkey'] = self.appKey
        params['appId'] = appId
        params['contentId'] = contentId
        params['DTL'] = deviceTokenList
        params['needDetails'] = GtConfig.isPushListNeedDetails()
        params['async'] = GtConfig.isPushListAsync()

        return self.httpPostFast(params)

    def close(self):
        params = dict()
        params['action'] = 'close'
        params['appkey'] = self.appKey
        params['version'] = GtConfig.getSDKVersion()
        params['authToken'] = IGeTui.push.authToken
        self.httpPostFast(params)

    def stop(self, contentId):
        params = dict()
        params['action'] = 'stopTaskAction'
        params['appkey'] = self.appKey
        params['contentId'] = contentId

        ret = self.httpPostFast(params)
        if ret["result"] == 'ok':
            return True
        return False

    def getClientIdStatus(self, appId, clientId):
        params = dict()
        params['action'] = 'getClientIdStatusAction'
        params['appkey'] = self.appKey
        params['appId'] = appId
        params['clientId'] = clientId

        return self.httpPostFast(params)

    def bindAlias(self, appId, alias, clientId):
        params = dict()
        params['action'] = 'alias_bind'
        params['appkey'] = self.appKey
        params['appid'] = appId
        params['alias'] = alias
        params['cid'] = clientId

        return self.httpPostFast(params)

    def bindAliasBatch(self, appId, targetList):
        params = dict()
        aliasList = []
        for target in targetList:
            user = dict()
            user['cid'] = target.clientId
            user['alias'] = target.alias
            aliasList.append(user)

        params['action'] = 'alias_bind_list'
        params['appkey'] = self.appKey
        params['appid'] = appId
        params['aliaslist'] = aliasList

        return self.httpPostFast(params)

    def queryClientId(self, appId, alias):
        params = dict()
        params['action'] = "alias_query"
        params['appkey'] = self.appKey
        params['appid'] = appId
        params['alias'] = alias

        return self.httpPostFast(params)

    def queryAlias(self, appId, clientId):
        params = dict()
        params['action'] = "alias_query"
        params['appkey'] = self.appKey
        params['appid'] = appId
        params['cid'] = clientId

        return self.httpPostFast(params)

    def unBindAlias(self, appId, alias, clientId=None):
        params = dict()
        params['action'] = "alias_unbind"
        params['appkey'] = self.appKey
        params['appid'] = appId
        params['alias'] = alias

        if clientId is not None and clientId.strip() != "":
            params['cid'] = clientId
        return self.httpPostFast(params)

    def unBindAliasAll(self, appId, alias):
        return self.unBindAlias(appId, alias, None)

    def getContentId(self, message, taskGroupName=None):
        params = dict()

        if taskGroupName is not None and taskGroupName.strip() != "":
            if len(taskGroupName) > 40:
                raise Exception("TaskGroupName is OverLimit 40")
            params['taskGroupName'] = taskGroupName

        params['action'] = "getContentIdAction"
        params['appkey'] = self.appKey
        transparent = message.data.getTransparent()
        params['clientData'] = str(base64.b64encode(transparent.SerializeToString()), encoding='utf-8')
        params['transmissionContent'] = message.data.transmissionContent
        params["isOffline"] = message.isOffline
        params["offlineExpireTime"] = message.offlineExpireTime
        # 增加pushNetWorkType参数(0:不限;1:wifi;2:4G/3G/2G)
        params["pushNetWorkType"] = message.pushNetWorkType
        params["pushType"] = message.data.pushType
        params['type'] = 2

        if isinstance(message, IGtListMessage):
            params['contentType'] = 1
        elif isinstance(message, IGtAppMessage):
            personaTags = []
            if message.getConditions() is None:
                params['phoneTypeList'] = message.getPhoneTypeList()
                params['provinceList'] = message.getProvinceList()
                params['tagList'] = message.getTagList()

            else:
                conditions = message.getConditions().getCondition()
                params['conditions'] = conditions

            params['speed'] = message.speed
            params['contentType'] = 2
            params['appIdList'] = message.appIdList
            if message.getPushTime() is not None and message.getPushTime() is not "":
                params['pushTime'] = message.getPushTime()

        ret = self.httpPostFast(params)
        if "ok" == ret.get('result'):
            return ret['contentId']
        else:
            raise Exception("获取 contentId 失败：" + ret)

    def getAPNContentId(self, appId, message):
        params = dict()
        params['action'] = "apnGetContentIdAction"
        params['appkey'] = self.appKey
        params['appId'] = appId
        params['PI'] = str(base64.b64encode(message.data.pushInfo.SerializeToString()), 'utf-8')
        params['isOffline'] = message.isOffline
        params['offlineExpireTime'] = message.offlineExpireTime
        params['pushNetWorkType'] = message.pushNetWorkType

        ret = self.httpPostFast(params)
        if "ok" == ret.get('result'):
            return ret['contentId']
        else:
            raise Exception("获取 contentId 失败：" + ret)

    def cancelContentId(self, contentId):
        params = dict()
        params['action'] = 'cancleContentIdAction'
        params['appkey'] = self.appKey
        params['contentId'] = contentId
        ret = self.httpPostFast(params)
        return True if ret.get('result') == 'ok' else False

    def getCurrentTime(self):
        return int(time.time() * 1000)

    def getSign(self, appKey, timeStamp, masterSecret):
        rawValue = appKey + str(timeStamp) + masterSecret
        return hashlib.md5(rawValue.encode()).hexdigest()

    def httpPostFast(self, params, needGzip=False):
        try:
            return self.httpPostJson(PushDomainManager.getFastUrl(self.domainKey), params, needGzip)
        except Exception as e:
            return "error: " + str(e)

    def httpPostJson(self, host, params, needGzip=False):
        params['version'] = GtConfig.getSDKVersion()
        params['authToken'] = IGeTui.push.authToken
        try:
            ret = IGeTui.push.domainManager.httpPost(host, params, needGzip)
        except GtHttpException as e:
            IGeTui.push.domainManager.notifyServerError(self.domainKey)
            raise RuntimeError("connect error", e)
        if ret is None or ret == '':
            if params.get('requestId') is not None:
                raise RequestException(params['requestId'])
            return ret
        if 'sign_error' == ret['result']:
            try:
                if self.connect():
                    params['authToken'] = IGeTui.push.authToken
                    ret = IGeTui.push.domainManager.httpPost(host, params, needGzip)
            except GtHttpException as e:
                IGeTui.push.domainManager.notifyServerError(self.domainKey)
                raise RuntimeError("connect error", e)
        elif 'domain_error' == ret['result']:
            if ret['osList'] is None:
                raise RuntimeError("connect error")
            osList = ret['osList']
            IGeTui.push.domainManager.notifyDomainError(self.domainKey, osList)
            try:
                ret = IGeTui.push.domainManager.httpPost(osList[0], params, needGzip)
            except GtHttpException as e:
                IGeTui.push.domainManager.notifyServerError(self.domainKey)
                raise RuntimeError("connect error", e)
        return ret

    def getPushResult(self, taskId):
        params = dict()
        params["action"] = "getPushMsgResult"
        params["appkey"] = self.appKey
        params["taskId"] = taskId

        return self.httpPostFast(params)

    def getPushResultByGroupName(self, appId, groupName):
        params = dict()
        params["action"] = "getPushResultByGroupName"
        params["appkey"] = self.appKey
        params["appId"] = appId
        params["groupName"] = groupName

        return self.httpPostFast(params)

    def getLast24HoursOnlineUserStatistics(self, appId):
        params = dict()
        params["action"] = "getLast24HoursOnlineUser"
        params["appkey"] = self.appKey
        params["appId"] = appId
        return self.httpPostFast(params)

    def getUserTags(self, appId, clientId):
        params = dict()
        params["action"] = "getUserTags"
        params["appkey"] = self.appKey
        params["appId"] = appId
        params["clientId"] = clientId
        return self.httpPostFast(params)

    def getPersonaTags(self, appId):
        params = dict()
        params["action"] = "getPersonaTags"
        params["appkey"] = self.appKey
        params["appId"] = appId
        return self.httpPostFast(params)

    def queryUserCount(self, appId, conditions):
        params = dict()
        params["action"] = "queryUserCount"
        params["appId"] = appId
        params["appkey"] = self.appKey
        # token
        if conditions is not None:
            params["conditions"] = conditions.getCondition()
        return self.httpPostFast(params)

    def setClientTag(self, appId, clientId, tags):
        params = dict()
        params["action"] = "setTagAction"
        params["appkey"] = self.appKey
        params["appId"] = appId
        params["clientId"] = clientId
        params["tagList"] = tags
        return self.httpPostFast(params)

    def queryAppPushDataByDate(self, appId, date):
        if LangUtils.validateDate(date) == False:
            raise ValueError("DateError|" + date)
        params = dict()
        params["action"] = "queryAppPushData"
        params["appkey"] = self.appKey
        params["appId"] = appId
        params["date"] = date
        return self.httpPostFast(params)

    def queryAppUserDataByDate(self, appId, date):
        if LangUtils.validateDate(date) == False:
            raise ValueError("DateError|" + date)
        params = dict()
        params["action"] = "queryAppUserData"
        params["appkey"] = self.appKey
        params["appId"] = appId
        params["date"] = date
        return self.httpPostFast(params)

    def blackCidList(self, appId, cidList, optType):
        params = dict()
        limit = GtConfig.getMaxLenOfBlackCidList()
        if limit < len(cidList):
            raise OverflowError("cid size:" + len(cidList) + " beyond the limit:" + limit)
        params["action"] = "blackCidAction"
        params["appkey"] = self.appKey
        params["appId"] = appId
        params["cidList"] = cidList
        params["optType"] = optType
        return self.httpPostFast(params)

    def addCidListToBlk(self, appId, cidList):
        return self.blackCidList(appId, cidList, 1)

    def restoreCidListFromBlk(self, appId, cidList):
        return self.blackCidList(appId, cidList, 2)

    def setBadgeForCID(self, badge, appid, cidList):
        return self.setBadge(badge, appid, list(), cidList)

    def setBadgeForDeviceToken(self, badge, appid, deviceTokenList):
        return self.setBadge(badge, appid, deviceTokenList, list())

    def setBadge(self, badge, appid, deviceTokenList, cidList):
        params = dict()
        params["action"] = "setBadgeAction"
        params["appkey"] = self.appKey
        params["badge"] = badge
        params["appid"] = appid
        params["deviceToken"] = deviceTokenList
        params["cid"] = cidList
        return self.httpPostFast(params)

    def getPushResultByTaskidList(self, taskIdList):
        return self.getPushActionResultByTaskids(taskIdList, None)

    def getPushActionResultByTaskids(self, taskIdList, actionIdList):
        params = dict()
        params["action"] = "getPushMsgResultByTaskidList"
        params["appkey"] = self.appKey
        params["taskIdList"] = taskIdList
        params["actionIdList"] = actionIdList
        return self.httpPostFast(params)

    def changeClientTag(self, appId, tag, operation, cids):
        params = dict()
        params["action"] = "changeTagAction"
        params["appkey"] = self.appKey
        params["appId"] = appId
        params["operation"] = operation
        params["tag"] = tag
        params["cids"] = cids

        return self.httpPostFast(params)

    def pushTagMessage(self, message, requestId):
        if requestId is None or requestId.strip() is "":
            requestId = str(uuid.uuid1())
        params = dict()
        params["action"] = "pushMessageByTagAction"
        params["appkey"] = self.appKey
        transparent = message.data.getTransparent()
        params['clientData'] = str(base64.b64encode(transparent.SerializeToString()), encoding='utf-8')
        params['transmissionContent'] = message.data.transmissionContent
        params['isOffline'] = message.isOffline
        params['offlineExpireTime'] = message.offlineExpireTime
        params['isOffline'] = message.isOffline
        # 增加pushNetWorkType参数(0:不限;1:wifi;2:4G/3G/2G)
        params["pushNetWorkType"] = message.pushNetWorkType
        params["appIdList"] = message.appIdList
        params["speed"] = message.speed
        params["requestId"] = requestId
        params["tag"] = message.tag
        return self.httpPostFast(params)

    def pushTagMessageRetry(self, message):
        return self.pushTagMessage(message, None)

    def getScheduleTask(self, taskId, appId):
        params = dict()
        params["action"] = "getScheduleTaskAction"
        params["appId"] = appId
        params["appkey"] = self.appKey
        params["taskId"] = taskId
        return self.httpPostFast(params)

    def delScheduleTask(self, taskId, appId):
        params = dict()
        params["action"] = "delScheduleTaskAction"
        params["appId"] = appId
        params["appkey"] = self.appKey
        params["taskId"] = taskId
        return self.httpPostFast(params)

    def bindCidPn(self, appId, cidAndPn):
        params = dict()
        params["action"] = "bind_cid_pn"
        params["appId"] = appId
        params["appkey"] = self.appKey
        params["cidpnlist"] = cidAndPn
        return self.httpPostFast(params)

    def unbindCidPn(self, appId, cid):
        params = dict()
        params["action"] = "unbind_cid_pn"
        params["appId"] = appId
        params["appkey"] = self.appKey
        params["cids"] = cid
        return self.httpPostFast(params)

    def queryCidPn(self, appId, cid):
        params = dict()
        params["action"] = "query_cid_pn"
        params["appId"] = appId
        params["appkey"] = self.appKey
        params["cids"] = cid
        return self.httpPostFast(params)

    def stopSendSms(self, appId, taskId):
        params = dict()
        params["action"] = "stop_sms"
        params["appId"] = appId
        params["appkey"] = self.appKey
        params["taskId"] = taskId
        return self.httpPostFast(params)

    def getUserCountByTags(self, appId, tagList):
        params = dict()
        params["action"] = "getUserCountByTags"
        params["appkey"] = self.appKey
        params["appId"] = appId
        params["tagList"] = tagList
        limit = GtConfig.getTagListLimit()
        if len(tagList) > limit:
            raise Exception("tagList size:" + len(tagList) + "beyond the limit" + limit)
        return self.httpPostFast(params)

    def getAuthToken(self):
        return IGeTui.push.authToken


class GtPush:

    def __init__(self, host, appKey, masterSecret, key, ssl):
        if host is not None:
            host = host.strip()

        if ssl is None and host is not None and host != '' and host.lower().startswith('https:'):
            ssl = True
        self.authToken = ""
        self.useSSL = (ssl if ssl is not None else False)
        wrapper = OSDomainWrapper(appKey, self.useSSL, GtConfig.getHostNeedAssigned(), host)
        self.domainManager = PushDomainManager()
        PushDomainManager.initOSDomain(key, wrapper)
