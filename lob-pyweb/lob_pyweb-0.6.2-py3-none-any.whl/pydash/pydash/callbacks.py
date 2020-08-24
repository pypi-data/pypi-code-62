import pandas as pd


class Cache(object):
    @staticmethod
    def read_json(f):
        return pd.read_json(f, orient="split")
    
    @staticmethod
    def to_json(frame):
        return frame.to_json(orient="split")
