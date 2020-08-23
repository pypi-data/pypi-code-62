import time
import datetime
from .ysHistData import YsHistData
from datetime import timezone

class YsHist:
    def __init__(self):
        self.data_history = None
        self.ex_timezone = None
        self.currency = None
        self.symbol = None
        self.gmtoffset = 0
        self.instrumentType = None
        self.exchangeTimezoneName = None

    def load(self, history_json):
        if "chart" in history_json and "result" in history_json['chart'] and history_json['chart']['result'] is not None:
            if 'meta' in history_json['chart']['result'][0]:
                self.ex_timezone = history_json['chart']['result'][0]['meta']['exchangeName']
                self.currency = history_json['chart']['result'][0]['meta']['currency']
                self.symbol = history_json['chart']['result'][0]['meta']['symbol']
                self.gmtoffset = history_json['chart']['result'][0]['meta']['gmtoffset']
                self.instrumentType = history_json['chart']['result'][0]['meta']['instrumentType']
                self.exchangeTimezoneName = history_json['chart']['result'][0]['meta']['exchangeTimezoneName']

            if 'timestamp' in history_json['chart']['result'][0]:
                self.data_history = {}
                for i, timestamp in enumerate(history_json['chart']['result'][0]['timestamp']):
                    self.data_history[timestamp] = YsHistData(
                        history_json['chart']['result'][0]['indicators']['quote'][0]['volume'][i],
                        history_json['chart']['result'][0]['indicators']['quote'][0]['low'][i],
                        history_json['chart']['result'][0]['indicators']['quote'][0]['open'][i],
                        history_json['chart']['result'][0]['indicators']['quote'][0]['high'][i],
                        history_json['chart']['result'][0]['indicators']['quote'][0]['close'][i],
                        history_json['chart']['result'][0]['indicators']['adjclose'][0]['adjclose'][i]
                    )

    def atDate(self, date_str):
        try:
            req_dt = datetime.datetime.strptime(date_str, "%d-%m-%Y").replace(tzinfo = timezone.utc)
            req_ts =  int(req_dt.timestamp())
            if self.data_history is not None:
                for stock_ts in self.data_history:
                    stock_dt = datetime.datetime.utcfromtimestamp(stock_ts)
                    if req_dt.year == stock_dt.year and req_dt.month == stock_dt.month and req_dt.day == stock_dt.day:
                        return self.data_history[stock_ts]
                    if stock_ts > req_ts:
                         break

        except ValueError:
            print("Could not convert data to an integer.")

        return None

    def toHistDataList(self):
        return self.data_history

    def toDict(self):
        data_history_dict = {}
        if self.data_history is not None:
            for timestamp in self.data_history:
                data_history_dict[timestamp] = {}
                data_history_dict[timestamp]['volume'] = self.data_history[timestamp].getVolume()
                data_history_dict[timestamp]['low'] = self.data_history[timestamp].getLow()
                data_history_dict[timestamp]['open'] = self.data_history[timestamp].getOpen()
                data_history_dict[timestamp]['high'] = self.data_history[timestamp].getHigh()
                data_history_dict[timestamp]['close'] = self.data_history[timestamp].getClose()
                data_history_dict[timestamp]['adjclose'] = self.data_history[timestamp].getAdjClose()
        return data_history_dict