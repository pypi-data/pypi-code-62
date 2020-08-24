from scrapy import Request


class UmengRequest(Request):
    def __init__(self, api=None, *args, **kwargs):
        self.api = api
        super().__init__(url="https://developer.umeng.com", *args, **kwargs)

