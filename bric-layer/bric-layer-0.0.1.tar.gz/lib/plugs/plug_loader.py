from . import api, blob, ms_teams, oracle, pgsql, power_bi


class Plugs:
    def __init__(self, layer):
        self.api = api.APIConnector(layer)
        self.blob = blob.BlobAPI(layer)
        self.oracle = oracle.Oracle(layer)
        self.pgsql = pgsql.Pgsql(layer)
        self.power_bi = power_bi.PowerBIAPI(layer)
        self.ms_teams = ms_teams.MSTeamsAPI(layer)
