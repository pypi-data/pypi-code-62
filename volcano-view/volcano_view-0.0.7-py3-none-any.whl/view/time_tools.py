import time


class Timer:
    def __init__(self):
        self.time_ = time.perf_counter()

    def set_now(self):
        self.time_ = time.perf_counter()

    def secs(self):
        rval = time.perf_counter() - self.time_
        return int(rval*100)/100 if rval >= 0.0 else 0.0
