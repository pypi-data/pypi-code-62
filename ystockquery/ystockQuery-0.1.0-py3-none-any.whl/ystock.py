import requests
import time
import datetime
import sys
from .ysHist import YsHist
from datetime import timezone

__BASE_URL__ = "https://query2.finance.yahoo.com/v8/finance/chart/"

class Ystock:
    def __init__(self, symbol):
        self.symbol = symbol
        self.base_history_url = __BASE_URL__
        self.data_history = None

    def history(self, period1_str, period2_str):
        try:
            period1 = int(datetime.datetime.strptime(period1_str, "%d-%m-%Y").replace(tzinfo = timezone.utc).timestamp())
            period2 = int(datetime.datetime.strptime(period2_str, "%d-%m-%Y").replace(tzinfo = timezone.utc).timestamp())
            url = self.base_history_url + self.symbol + "?formatted=true&interval=1d&period1=" + str(period1) + "&period2=" + str(period2)
            resp = requests.get(url)
     
            if (resp.status_code == 200):
                self.data_history = YsHist()
                self.data_history.load(resp.json())
            else:
                self.data_history = None

        except ValueError:
            print("Could not convert data to an integer.")

        return self.data_history