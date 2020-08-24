
from scrapy import signals
from scrapy.http import HtmlResponse
from . import aop
import json


class UmengDownloaderMiddleware:

    def __init__(self, api_key, api_secret, api_server):
        aop.set_default_server(api_server)
        aop.set_default_appinfo(api_key, api_secret)

    @classmethod
    def from_crawler(cls, crawler):
        api_key = crawler.settings.get('UMENG_API_KEY')
        api_secret = crawler.settings.get('UMENG_API_SECRET')
        api_server = crawler.settings.get('UMENG_API_SERVER')

        middleware = cls(
            api_key,
            api_secret,
            api_server
        )

        crawler.signals.connect(middleware.process_closed, signals.spider_closed)

        return middleware

    def process_request(self, request, spider):

        if(hasattr(aop.api, request.api)):
            req = eval('aop.api.' + str(request.api) + '()')
            response = req.get_response(None, **request.meta)
            return HtmlResponse(
                req.get_api_uri(),
                body=str.encode(json.dumps(response)),
                encoding='utf-8',
                request=request
            )
        else:
            return None




    def process_closed(self):
        pass