import hashlib
import json

from requests_mock import Mocker


class AiProxyMock(Mocker):
    def __init__(self, trimap, ghosting, remove_background, **kwargs):
        super().__init__(real_http=True, **kwargs)
        with open(trimap) as t, open(ghosting) as g, open(remove_background) as rb:
            self.trimap = json.load(t)
            self.ghosting = json.load(g)
            self.remove_background = json.load(rb)

    def __enter__(self):
        super().__enter__()
        self.register_uri(
            'POST', 'http://localhost:8283/predict/', json=self.trimap)
        self.register_uri(
            'POST', 'http://localhost:8282/predict/', json=self.ghosting)
        self.register_uri(
            'POST', 'http://localhost:8281/predict/', json=self.remove_background)

        return self


class StorageSidecarMock(Mocker):
    def put_to_storage(self, image: bytes, company_id: str):
        content_hash = self.__create_content_hash__(image)
        self.storage[company_id + "/origin/" + content_hash] = image
        return content_hash

    def get_from_storage(self, content_hash: str, company_id: str):
        return self.storage[company_id + "/origin/" + content_hash]

    def __enter__(self):
        super().__enter__()
        self.storage = {}
        self.register_uri('GET', 'http://localhost:8180/image/',
                          content=self.get_callback)
        self.register_uri(
            'POST', 'http://localhost:8180/image/', json=self.post_callback)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.storage.clear()

    def post_callback(self, request, context):
        content_hash = self.put_to_storage(
            image=request.body, company_id=request.qs['company_id'].pop())
        return {'contentHash': content_hash}

    def get_callback(self, request, context):
        path = request.qs['company_id'].pop() + "/origin/" + \
            request.qs['content_hash'].pop()
        return self.storage.get(path)

    @staticmethod
    def __create_content_hash__(image: bytes) -> str:
        m = hashlib.sha256()
        m.update(image)
        return m.hexdigest().lower()
