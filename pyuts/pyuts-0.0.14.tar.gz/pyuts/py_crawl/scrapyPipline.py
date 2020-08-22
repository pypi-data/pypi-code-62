# -*- coding: UTF-8 -*-
import pyuts
from pyuts import MongoDBU


class ScrapyprojectnamePipeline(object):
    """
    scrapyPipline相关封装工具
    """
    
    def __init__(self):
        host = pyuts.envU().get('MONGO_HOST')
        port = pyuts.envU().get('MONGO_PORT')
        user = pyuts.envU().get('MONGO_USER')
        pswd = pyuts.envU().get('MONGO_PSWD')
        # 创建MONGODB数据库链接
        self.client = MongoDBU().init(host, port, user, pswd)

    def process_item(self, item, spider):
        data = dict(item)
        # self.post.insert(data)
        tb_name = item.saveTableName
        if tb_name == None:
            tb_name = item.__class__.__name__
        db_name = item.saveDbName
        if db_name == None:
            from scrapy.utils.project import get_project_settings
            settings = get_project_settings()
            db_name = settings["BOT_NAME"]
        self.client.upsert_one(db_name, tb_name, {'id': data['id']}, data)
        return item

    def open_spider(self, spider):
        spider.myPipline = self
        spider.state = 'running'

    def close_spider(self, spider):
        spider.myPipline = None
        spider.state = 'close'