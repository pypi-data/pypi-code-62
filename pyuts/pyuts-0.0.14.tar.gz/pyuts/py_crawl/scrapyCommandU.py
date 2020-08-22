# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.3 (default, Mar 27 2019, 09:23:15) 
# [Clang 10.0.1 (clang-1001.0.46.3)]
# Embedded file name: /Users/jack/WorkSpace/testCrawl/pyuts/py_crawl/scrapyCommandU.py
# Compiled at: 2020-05-13 13:47:32
# Size of source mod 2**32: 1298 bytes
from ..py_api_b import PyApiB
import scrapy
from scrapy.commands import ScrapyCommand
# from abc import abstractmethod

class ScrapyCommandU(ScrapyCommand, PyApiB):
    """
    scrapy相关命令行操作
    """
    __module__ = __name__
    __qualname__ = 'ScrapyCommandU'

    @staticmethod
    def produce(key=None):
        return PyApiB._produce(key, __class__)

    def start_crawl(self):
        self.crawler_process.start()
        if self.crawler_process.bootstrap_failed:
            self.exitcode = 1

    def finish_crawl(self, result):
        print('Finished crawl all spiders!')
        self.crawler_process.stop()
        self.exitcode = 0

    def getArgsDict(self, args):
        res = {}
        for arg in args:
            vv = arg.split('=')
            res[vv[0]] = vv[1]

        return res

    def getSpiderNames(self):
        return sorted(self.crawler_process.spider_loader.list())

    def run(self, args, opts):
        pass

    def runSpider(self, spider_name, *args, **kwargs):
        """ run spider and return deffer.Then can use self.addCallback(deffer, fun).fun=self.finish_crawl means all crawl finish"""
        print(f"run spider {spider_name}")
        return self.crawler_process.crawl(spider_name, *args, **kwargs)

    def addCallback(self, deffer, fun):
        deffer.addCallback(fun)
# okay decompiling scrapyCommandU.cpython-37.pyc
