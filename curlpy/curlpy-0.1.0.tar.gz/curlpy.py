from typing import Dict
from urllib.request import Request, urlopen


class Curlpy:
    def __init__(self, url=""):
        self._url: str = url
        self._method: str = "GET"
        self._headers: Dict[str, str] = dict()
        self._query: Dict[str, str] = dict()

        self.body: str = ""
        self.status: int = -1

    def url(self, url: str):
        self._url = url
        return self

    def request(self, method: str):
        self._method = method
        return self

    def X(self, method: str):
        return self.request(method)

    def get(self):
        return self.request("GET")

    def post(self):
        return self.request("POST")

    def output(self, filename: str, binary=False):
        mode = "w" if not binary else "wb"
        with open(filename, mode=mode) as f:
            f.write(self.body)
        return self

    def o(self, filename: str, binary=False):
        return self.output(filename, binary=binary)

    def header(self, headers: Dict[str, str]):
        self._headers.update(headers)
        return self

    def H(self, headers: Dict[str, str]):
        return self.header(headers)

    def fetch(self):
        req = Request(url=self._url, method=self._method, headers=self._headers,)
        with urlopen(req) as res:
            self.body = res.read()
            self.status = res.getcode()

        return self
