
class Client:
    def __init__(self, client_id, client_filter):
        self.client_id, self.client_filter = client_id, client_filter


class ClientFilter:
    def __init__(self, client):
        self.client = client