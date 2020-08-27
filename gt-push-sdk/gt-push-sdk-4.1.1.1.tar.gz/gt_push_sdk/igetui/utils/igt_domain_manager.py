import gzip
import json
import sys
import threading
import time
import re

import requests

from gt_push_sdk.GtConfig import GtConfig
from gt_push_sdk.RequestException import RequestException, GtHttpException
from gt_push_sdk.igetui.utils.igt_domain_wrapper import OSDomainWrapper

globals = {
    'false': "false",
    'true': "true",
    'null': "null"
}


class PushDomainManager:
    session = requests.session()
    domainMap = dict()
    domainPool = set()
    isRunning = bool()
    __domainMapLock__ = threading.Lock()
    __domainPoolLock__ = threading.Lock()

    def __init__(self):
        self.cycleRunner()
        t = threading.Timer(GtConfig.getHttpInspectInterval(), self.cycleRunner)
        t.setDaemon(True)
        t.start()

    @staticmethod
    def cycleTest():
        try:
            rankMap = PushDomainManager.rankDomain()
            PushDomainManager.updateFastestDomain(rankMap)
        except Exception:
            pass
        finally:
            PushDomainManager.compareAndSet(PushDomainManager.isRunning, True, False)

    @staticmethod
    def cycleRunner():
        try:
            if PushDomainManager.compareAndSet(PushDomainManager.isRunning, False, True):
                PushDomainManager.cycleTest()
        except Exception:
            pass

    @staticmethod
    def rankDomain():
        rankMap = dict()
        if len(PushDomainManager.domainPool) == 0:
            return rankMap
        with PushDomainManager.__domainPoolLock__:
            for url in PushDomainManager.domainPool:
                responseTime = PushDomainManager.getResponseTime(url)
                if responseTime == sys.float_info.max:
                    continue
                rankMap[url] = responseTime

        return rankMap

    @staticmethod
    def getResponseTime(host):
        try:
            start = time.time()
            from GtConfig import GtConfig
            if GtConfig.getHttpProxyIp() is not None:
                # 配置代理如下
                userAndPass = "%s:%s" % (GtConfig.getHttpProxyUserName(), GtConfig.getHttpProxyPasswd())
                ipport = "%s:%s" % (GtConfig.getHttpProxyIp(), GtConfig.getHttpProxyPort())
                http_proxy = "http://" + userAndPass + "@" + ipport + "/"
                https_proxy = "http://" + userAndPass + "@" + ipport + "/"
                proxies = {
                    "http": http_proxy,
                    "https": https_proxy
                }
                ret = PushDomainManager.session.post(host, proxies=proxies, timeout=GtConfig.getHttpConnectionTimeOut(),
                                                     stream=False,
                                                     verify=True)
            else:
                ret = PushDomainManager.session.post(host, timeout=GtConfig.getHttpConnectionTimeOut(), stream=False,
                                                     verify=True)
            pass
            if ret is None or ret.status_code != 200:
                return sys.float_info.max
            end = time.time()
            diff = end - start
            return diff
        except Exception:
            return -1

    @staticmethod
    def updateFastestDomain(rankMap):
        with PushDomainManager.__domainMapLock__:
            for wrapper in PushDomainManager.domainMap.values():
                if len(rankMap) > 0:
                    fastUrl = PushDomainManager.getMinResponseTimeUrl(rankMap, wrapper)
                    if fastUrl is not None and len(fastUrl) > 0:
                        wrapper.setFasterUrl(fastUrl)
                        continue
                    if wrapper.isAssigned and rankMap.__contains__(wrapper.getAssignedUrl()):
                        wrapper.setFasterUrl(wrapper.getAssignedUrl())
                        continue

                if wrapper.isFailCountOverLimit() is False:
                    continue

                PushDomainManager.setOrUpdateFastUrl(wrapper, GtConfig.getDefaultDomainUrl(wrapper.isSSL))
                PushDomainManager.addDomainUrls(wrapper.getDomainUrls())

    @staticmethod
    def getMinResponseTimeUrl(rankMap, wrapper):
        minTime = sys.float_info.max
        fastUrl = ""
        for url in wrapper.getDomainUrls():
            if not rankMap.__contains__(url):
                continue
            if minTime - rankMap.get(url) > 0:
                minTime = rankMap.get(url)
                fastUrl = url
        return fastUrl

    @staticmethod
    def initOSDomain(domainKey, wrapper):
        if not wrapper.isAssigned:
            domainUrls = wrapper.getDomainUrls()
            if domainUrls is None or len(domainUrls) == 0:
                domainUrls = GtConfig.getDefaultDomainUrl(wrapper.isSSL)
            PushDomainManager.setOrUpdateFastUrl(wrapper, domainUrls)
        PushDomainManager.addOSDomainWrapper(domainKey, wrapper)

    @staticmethod
    def setOrUpdateFastUrl(wrapper, domainUrls):
        osPushDomainUrlList = PushDomainManager.getOSPushDomainUrlList(domainUrls, wrapper.getAppKey())
        wrapper.setDomainUrls(osPushDomainUrlList)
        wrapper.setFasterUrl(osPushDomainUrlList[0])
        wrapper.reSetCountinuousFailCount()

    @staticmethod
    def addOSDomainWrapper(domainKey, wrapper):
        if wrapper is None:
            return
        with PushDomainManager.__domainMapLock__:
            PushDomainManager.domainMap[domainKey] = wrapper
        PushDomainManager.addDomainUrls(wrapper.getDomainUrls())

    @staticmethod
    def addDomainUrls(domainUrls):
        if domainUrls is None:
            return
        with PushDomainManager.__domainPoolLock__:
            for domainUrl in domainUrls:
                url_re = re.compile(":(80|443)")
                PushDomainManager.domainPool.add(url_re.sub("", domainUrl))

    @staticmethod
    def getOSPushDomainUrlList(hosts, appKey):
        postData = dict()
        urlList = None
        postData['action'] = 'getOSPushDomailUrlListAction'
        postData['appkey'] = appKey
        ex = None
        for host in hosts:
            try:
                response = PushDomainManager.httpPost(host, postData)
                if response is not None and response['result'] == 'ok':
                    urlList = response['osList']
                    if urlList is not None and len(urlList) > 0:
                        break
            except Exception as e:
                ex = e
        if urlList is None or len(urlList) <= 0:
            raise Exception("Can not get hosts", ex)
        return urlList

    @staticmethod
    def notifyDomainError(domainKey, osList):
        wrapper = domainKey[domainKey]
        if wrapper is None or osList is None or len(osList) <= 0:
            return
        wrapper.setDomainUrls(osList)

    @staticmethod
    def notifyServerError(domainKey):
        wrapper = PushDomainManager.domainMap[domainKey]
        if wrapper is None:
            return
        if wrapper.isNeedTrigger() and PushDomainManager.compareAndSet(PushDomainManager.isRunning, False, True):
            wrapper.updateTriggerTime()
            PushDomainManager.triggerCheck()

    @staticmethod
    def triggerCheck():
        t = threading.Thread(PushDomainManager.cycleTest())
        t.start()

    @staticmethod
    def getFastUrl(domainKey):
        return PushDomainManager.domainMap.get(domainKey).getFasterUrl()

    @staticmethod
    def httpPost(host, params, needGzip=False):
        headers = dict()
        data_json = json.dumps(params)
        headers['Gt-Action'] = params.get("action")
        if needGzip:
            data_json = gzip.compress(bytes(data_json, 'utf-8'))
            headers['Content-Encoding'] = 'gzip'
            headers['Accept-Encoding'] = 'gzip'

        retry_time_limit = GtConfig.getHttpTryCount()
        isFail = True
        tryTime = 0
        res_stream = None

        while isFail and tryTime < retry_time_limit:
            isFail = False
            try:
                if GtConfig.getHttpProxyIp() is not None:
                    # 配置代理如下
                    userAndPass = "%s:%s" % (GtConfig.getHttpProxyUserName(), GtConfig.getHttpProxyPasswd())
                    ipport = "%s:%s" % (GtConfig.getHttpProxyIp(), GtConfig.getHttpProxyPort())
                    http_proxy = "http://" + userAndPass + "@" + ipport + "/"
                    https_proxy = "http://" + userAndPass + "@" + ipport + "/"
                    proxies = {
                        "http": http_proxy,
                        "https": https_proxy
                    }
                    res_stream = PushDomainManager.session.post(host, proxies=proxies, data=data_json, headers=headers,
                                                                timeout=GtConfig.getHttpConnectionTimeOut(),
                                                                verify=True, stream=False)
                else:
                    res_stream = PushDomainManager.session.post(host, data=data_json, headers=headers,
                                                                timeout=GtConfig.getHttpConnectionTimeOut(),
                                                                verify=True, stream=False)
            except Exception as e:
                isFail = True
            tryTime += 1

        if res_stream is None:
            return None
        if res_stream.status_code == 404 or res_stream.status_code == 503:
            if params.__contains__('requestId'):
                raise GtHttpException(params[
                                          'requestId'] + " httpPost:[" + host + "] [" + str(
                    params) + "]: Http Response Error." + str(res_stream.status_code))
            else:
                raise GtHttpException(" httpPost:[" + host + "] [" + str(params) + "]: Http Response Error." + str(
                    res_stream.status_code))
        page_str = res_stream.text
        if needGzip:
            # requests自动解压文件
            # with gzip.GzipFile(fileobj=compressedstream) as f:
            # data = gzip.decompress(res_stream.content)
            return json.loads(page_str)
        else:
            return eval(page_str, globals)

    @staticmethod
    def compareAndSet(boolean, expect, update):
        if boolean == expect:
            boolean = update
            return True
        else:
            return False
