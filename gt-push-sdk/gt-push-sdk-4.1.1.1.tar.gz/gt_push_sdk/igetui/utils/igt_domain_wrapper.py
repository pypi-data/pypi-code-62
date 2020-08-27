import time

from gt_push_sdk.GtConfig import GtConfig


class OSDomainWrapper:
    domainUrls = dict()
    assignedUrl = None
    fasterUrl = None
    continuousFailCount = 0
    lastTriggerTime = 0

    def __init__(self, appKey, isSSL, isAssigned, domainUrl):
        self.appKey = appKey
        self.isSSL = isSSL
        self.isAssigned = isAssigned
        self.addDomainUrls(domainUrl)

    @staticmethod
    def setDomainUrls(domainUrls):
        OSDomainWrapper.domainUrls = domainUrls

    def addDomainUrls(self, domainUrl):
        if domainUrl is None or len(domainUrl) <= 0:
            self.isAssigned = False
        else:
            OSDomainWrapper.domainUrls = []
            OSDomainWrapper.domainUrls.append(domainUrl)
            OSDomainWrapper.assignedUrl = domainUrl
            OSDomainWrapper.fasterUrl = domainUrl

    @staticmethod
    def isFailCountOverLimit():
        OSDomainWrapper.continuousFailCount += 1
        return OSDomainWrapper.continuousFailCount >= GtConfig.getHttpFailCount()

    @staticmethod
    def isNeedTrigger():
        return OSDomainWrapper.isFailCountOverLimit() and (
                time.time() - OSDomainWrapper.lastTriggerTime) > GtConfig.getTriggerInterval()

    @staticmethod
    def updateTriggerTime():
        OSDomainWrapper.lastTriggerTime = time.time()

    @staticmethod
    def reSetCountinuousFailCount():
        OSDomainWrapper.continuousFailCount = 0

    @staticmethod
    def setFasterUrl(fastUrl):
        OSDomainWrapper.fasterUrl = fastUrl

    def getAppKey(self):
        return self.appKey

    @staticmethod
    def getDomainUrls():
        return OSDomainWrapper.domainUrls

    @staticmethod
    def getAssignedUrl():
        return OSDomainWrapper.assignedUrl

    @staticmethod
    def getFasterUrl():
        return OSDomainWrapper.fasterUrl
