# -*- coding: UTF-8 -*-
from ..py_api_b import PyApiB
import scrapy
from ..py_crawl.scrapyItemU import ScrapyItemU
from ..py_db.mongoDBU import MongoDBU
from .chromeU import ChromeU


class ScrapySpiderU(scrapy.Spider, PyApiB):
    """
    scrapy相关封装工具的各个爬虫器
    """
    @staticmethod
    def produce(key=None):
        return PyApiB._produce(key, __class__)

    enable = True
    """
    如果为enable=True,开启这项的spider才会执行
    """
    name = 'SpiderU_default'

    crawlType = 'scrapy'
    """ scrapy默认, chrome：表示启用chrome打开,页面加载完成后，会触发chromeDo进行操作 """

    def chromeDo(self, chromeU: ChromeU, meta=None):
        pass

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.state = 'waitting'

    def toJsonStr(self, data):
        import pyuts
        return pyuts.jsonU().toString(data, indent=None)
    
    def toJson(self, jsonStr):
        import pyuts
        return pyuts.jsonU().fromString(jsonStr)
    
    def meta(self, response, key):
        return response.meta[key]

    def get(self, url, callback, meta=None):
        return scrapy.Request(url=url, callback=callback, meta=meta)

    def saveItem(self, data, item_cls: ScrapyItemU):
        """
        yield self.saveItem(data, xxxxItem)
        """
        from scrapy.loader import ItemLoader
        from scrapy.loader.processors import TakeFirst
        item_loader = ItemLoader(item=item_cls())
        item_loader.default_output_processor = TakeFirst()
        for key in data:
            try:
                item_loader.add_value(key, data[key])
            except BaseException as identifier:
                pass
        return item_loader.load_item()
