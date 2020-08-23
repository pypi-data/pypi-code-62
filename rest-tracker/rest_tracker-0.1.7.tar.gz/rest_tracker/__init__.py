from modutils import BaseSession

class ES_Session(BaseSession):

    def __init__(self, host:str='localhost', port:str='9200'):
        super().__init__()
        self.host = host
        self.port = port
        self.base_url = f'http://{host}:{port}'
        self.initialized = False

    def set_host(self, host:str):
        self.host = host
        self.base_url = f'http://{host}:{self.port}'

    def set_port(self, port: str):
        self.port = port
        self.base_url = f'http://{self.host}:{port}'

    def create_index(self, index: str, mapping: dict):
        print(self.base_url)
        return self.put(f'{self.base_url}/{index}', json=mapping)

    def add_content(self, index:str, doc_type: str, content: dict):
        if self.initialized:
            return self.post(f'{self.base_url}/{index}/{doc_type}', json=content)
        else:
            return {'Error': 'Elasticsearch has not been initialized. '
                             'Please send a POST request to /rest_tracker/init_es to initialize.'}

ELASTIC_SESSION = ES_Session()