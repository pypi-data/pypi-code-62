import cx_Oracle


class Oracle:
    def __init__(self, layer):
        self.layer = layer

        self.oracle = cx_Oracle
