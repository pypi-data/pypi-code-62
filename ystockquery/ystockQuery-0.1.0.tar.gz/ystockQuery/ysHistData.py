class YsHistData:
    def __init__(self, s_volume, s_low, s_open, s_high, s_close, s_adjclose):
        self.s_volume = s_volume
        self.s_low =  s_low
        self.s_open = s_open
        self.s_high = s_high
        self.s_close = s_close
        self.s_adjclose = s_adjclose

    def getVolume(self):
        return self.s_volume

    def getLow(self):
        return self.s_low

    def getOpen(self):
        return self.s_open
    
    def getHigh(self):
        return self.s_high

    def getClose(self):
        return self.s_close
    
    def getAdjClose(self):
        return self.s_adjclose

