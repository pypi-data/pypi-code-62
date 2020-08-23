# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     ProxyScheduler
   Description :
   Author :        JHao
   date：          2019/8/5
-------------------------------------------------
   Change Activity:
                   2019/8/5: ProxyScheduler
-------------------------------------------------
"""
__author__ = 'JHao'

import sys,os
from apscheduler.schedulers.blocking import BlockingScheduler
#print(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from Schedule import doRawProxyCheck, doUsefulProxyCheck
from Manager import ProxyManager
from Util import LogHandler
import logging
logging.disable(logging.ERROR)

class DoFetchProxy(ProxyManager):
    """ fetch proxy"""

    def __init__(self):
        ProxyManager.__init__(self)
        self.log = LogHandler('fetch_proxy')

    def main(self):
        self.log.info("start fetch proxy")
        self.fetch()
        self.log.info("finish fetch proxy")


def rawProxyScheduler():
    DoFetchProxy().main()
    doRawProxyCheck()


def usefulProxyScheduler():
    doUsefulProxyCheck()


def runScheduler():
    rawProxyScheduler()
    usefulProxyScheduler()

    scheduler_log = LogHandler("scheduler_log")
    scheduler = BlockingScheduler(logger=scheduler_log)

    scheduler.add_job(rawProxyScheduler, 'interval', minutes=2, id="raw_proxy_check", name="raw_proxy定时采集")
    scheduler.add_job(usefulProxyScheduler, 'interval', minutes=1, id="useful_proxy_check", name="useful_proxy定时检查")

    scheduler.start()


if __name__ == '__main__':
    runScheduler()
