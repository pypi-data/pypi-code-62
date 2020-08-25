import psycopg2


class Pgsql:
    def __init__(self, layer):
        self.layer = layer

        self.Pgsql = psycopg2
