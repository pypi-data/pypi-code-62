import os, sys, re, logging
dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(dir_path)
import time
import threading
import psutil
from datetime import datetime
from rtd.client import RTDClient



class StockQuote(RTDClient):

    def __init__(self, classid='xqrtd.rtdservercsc'):
        if not "daqKingCon.exe" in (p.name() for p in psutil.process_iter()):
            raise('請先登入康和金好康')

        super(StockQuote, self).__init__(classid)
        self.connect()
        self.available = threading.Event()
        thread = threading.Thread(target=self.start, kwargs={'sampling' : 0.5})
        thread.start()
        # thread.join()
        self.available.wait()

    def start(self, sampling=0.5):
        self.available.set()

        while True:
            self.UpdateNotify()
            time.sleep(sampling)

    def set_topic(self, commodity, topic):
        self.register_topic('{}.TW-{}'.format(commodity, topic))

if __name__ == "__main__":
    agent = StockQuote()

    agent.set_topic('2330', 'Bid')
    agent.set_topic('2330', 'Ask')
    print("OK")
    while True:
        # This line is critical, it tells the pythoncom subsystem to
        # handle any pending windows messages. We're waiting for an
        # UpdateNotify callback from the RTDServer; if we don't
        # check for messages we'll never be notified of pending
        # RTD updates!
        time.sleep(1)

        # agent.UpdateNotify()
        if agent.update():
            print(agent.get('2330.TW-Bid'), agent.get('2330.TW-Ask'))