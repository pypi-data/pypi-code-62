import os, sys, re, logging
dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(dir_path)
import time
import threading
import psutil
from datetime import datetime
from rtd.client import RTDClient


class FuturesQuote(RTDClient):

    def __init__(self, classid='xqrtd.rtdservercsc'):
        if not "daqKingCon.exe" in (p.name() for p in psutil.process_iter()):
            raise('請先登入康和金好康')

        super(FuturesQuote, self).__init__(classid)
        self.connect()
        
        self.quote_topic = []
        self.quote_event = Event()
        self.available = threading.Event()
        thread = threading.Thread(target=self.start, kwargs={'sampling' : 0.5})
        thread.start()
        # thread.join()
        self.available.wait()

    def start(self, sampling=0.5):
        self.available.set()

        while True:
            self.UpdateNotify()

            if agent.update():
                for commodity, topic in self.quote_topic:
                    value = self.get('{}.TF-{}'.format(commodity, topic))
                    self.quote_event.notify(commodity, topic, value)
            time.sleep(sampling)

    def code_convert(self, commodity, commodity_type='F', strike_price=0, expire_date=datetime.now(), after_hour=False):
        if commodity_type=='F':
            topic = "FI{C}{A}{M:02}".format(C=commodity,
                                            A='N' if after_hour else '',
                                            M=expire_date.month)
        else:
            topic = "{C}{A}{M:02}{T:1}{S:05}".format(C=commodity,
                                                     A='N' if after_hour else '',
                                                     T=commodity_type,
                                                     S=strike_price,
                                                     M=expire_date.month)
        return topic

    def set_topic(self, commodity, topic):
        self.quote_topic.append((commodity, topic))
        self.register_topic('{}.TF-{}'.format(commodity, topic))


class Event():
    def __init__(self):
        self.listeners = []

    def __iadd__(self, listener):
        """Shortcut for using += to add a listener."""
        self.listeners.append(listener)
        return self

    def notify(self, *args, **kwargs):
        for listener in self.listeners:
            listener(*args, **kwargs)


def test_get_quote(C, T, V):
    print('[{}][{}] {}'.format(C, T, V))


if __name__ == "__main__":
    agent = FuturesQuote()

    topic1 = agent.code_convert(commodity='TXO', commodity_type='P', strike_price=12500, expire_date=datetime(2020, 10, 18), after_hour=True)
    agent.set_topic(topic1, 'Bid')

    topic2 = agent.code_convert(commodity='TX', commodity_type='F', strike_price=0, expire_date=datetime(2020, 10, 18), after_hour=False)
    agent.set_topic(topic2, 'Ask')
    print("OK")

    agent.quote_event += test_get_quote

    while True:
        # This line is critical, it tells the pythoncom subsystem to
        # handle any pending windows messages. We're waiting for an
        # UpdateNotify callback from the RTDServer; if we don't
        # check for messages we'll never be notified of pending
        # RTD updates!
        time.sleep(1)

        print(datetime.now())