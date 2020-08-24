#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Robin 'r0w' Weiland"
__date__ = "2020-08-15"
__version__ = "0.0.7"

__all__ = ('API',)

from api_bridge.methods import Method
from api_bridge.container import Container
from api_bridge.url import valid_url
from api_bridge.exceptions import APIException, RequestException, ValidationException, URLException

from requests import request, Response
from operator import gt

from typing import Optional, Union, Callable, Dict, Tuple, Any


class API:
    url: str
    method: Method
    result_filter: Optional[Callable[[Dict[str, Any]], Dict[str, Any]]]
    callback: Optional[Callable[[Dict[str, Any]], Dict[str, Any]]]
    validate: Optional[Callable[[Dict[str, Any]], bool]]
    post_data: Optional[Dict[str, Any]]

    response: Optional[Response]

    def __init__(self,
                 url: str,
                 method: Method = Method.GET,
                 result_filter: Optional[Callable[[Dict[str, Any]], Dict[str, Any]]] = None,
                 validate: Optional[Callable[[Dict[str, Any]], bool]] = None,
                 post_data: Optional[Dict[str, Any]] = None):
        if not valid_url(url): raise URLException(f'"{url}" is invalid!')
        self.url = url
        self.method = method
        self.result_filter = result_filter
        self.validate = validate
        self.post_data = post_data

        self.response = None

    def __bool__(self) -> bool: return self.response is not None and self.response.ok

    def __str__(self) -> str: return f'API[{self.url}]'

    def __repr__(self) -> str: return str(self)

    def __gt__(self, other: Union['API', Container]) -> Union['API', Container]:
        self.request()
        other(self.result_filter(self.json()) if self.result_filter else self.json())
        return other

    def __rshift__(self, other: Union['API', Container]) -> Union['API', Container]: return self > other

    def __and__(self, other: Union['API', Container]) -> Union['API', Container]: return self > other

    def __call__(self, filter_data=None) -> None:
        if filter_data is not None:
            self.url = self.url.format(**filter_data)
        self.request()

    def json(self) -> Dict[str, Any]:
        if self.response is not None: return self.response.json()
        else: raise APIException('Request not done yet!')

    def request(self) -> None:
        try: self.response = request(method=str(self.method), url=self.url, data=self.post_data or dict())
        except Exception as exc: raise RequestException(f'{self.method}-request for {self.url} failed [{exc}]!')
        else:
            if not self.response.ok or (self.validate is not None and not self.validate(self.json())):
                raise ValidationException(f'Response code from "{self.url}" was not ok or validation '
                                          f'"{self.validate.__name__ if self.validate is not None else None}" failed!')

    @staticmethod
    def chain(*apis: 'API') -> Container:
        current: API = apis[0]
        for api in apis[1:]:
            current = gt(current, api)
        return current > Container()

    def __class_getitem__(cls, apis: Tuple['API', ...]) -> Container:
        return cls.chain(*apis)


if __name__ == '__main__': pass
