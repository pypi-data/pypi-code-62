"""class to handle Redis api for python client"""
import requests
from src.models.time_unit_enum import TimeUnitEnum
from src.utils.url_builder import UrlBuilder
from src import config


class RedisUtils:
    r"""Create a client to handle redis api.
    :param application_prefix: application prefix SG, PL, DT, CD, SG, CC, etc.
    from src import RedisUtils
    redis_client = RedisUtils(application_prefix="your_application_prefix,
                              application_name="your application name",
                              environment="your_environment",
                              vpce_id="you vpce_id")
    you can pass these parameters through environment variables"""

    def __init__(self, **kwargs):
        self.application_prefix = kwargs.get('application_prefix', None)
        self.application_name = kwargs.get('application_name', None)
        environment = kwargs.get('environment', None)
        self.vpce_id = kwargs.get('vpce_id', None)
        self.api_key = kwargs.get('api_key', None)
        old_account = kwargs.get('old_account')
        self.url_builder = UrlBuilder(environment=environment,
                                      vpce_id=self.vpce_id,
                                      old_account=old_account)
        self.api_key = self.api_key or config.API_KEY
        self.default_headers = self.__generate_default_headers()
        self.http_client = requests

    def set_key(self, **kwargs) -> bool:
        r""" save a key in redis and return a boolean if it was possible or not to save a key.
        usage:
            redis_response = redis_client.set_key(key="your redis key, must be str"
                                                  time="your time, must be int",
                                                  time_unit="your unit time, must be str or TimeUnitEnum",
                                                  data="your data to save, must be str")"""
        method = 'post'
        key = kwargs.get('key', None)
        time = kwargs.get('time', 15)
        time_unit = kwargs.get('time_unit', TimeUnitEnum.MINUTES)
        data = kwargs.get('body')
        parsed_time = self.__handle_time(time)
        parsed_time_unit = self.__handle_time_unit(time_unit).value
        headers = self.default_headers
        headers['time'] = str(parsed_time)
        headers['time-unit'] = str(parsed_time_unit)
        url = self.url_builder.get_url_for_set_key(key)
        response = self.__make_http_call(endpoint=url,
                                         headers=headers,
                                         method=method,
                                         body=data)
        response_status_code = response.status_code
        response_as_string = response.text
        print('status code of response: {} response body: {}'.format(response_status_code,
                                                                     response_as_string))
        return response_status_code == 200

    def get_key(self, key: str) -> str:
        r""" get a key saved in redis and return str if it was possible to get a key else return None.
                usage:
                    redis_response = redis_client.get_key("your key, must be str")"""
        method = 'get'
        url = self.url_builder.get_url_for_get_key(key)
        response = self.__make_http_call(url=url, method=method)
        response_status_code = response.status_code
        response_as_text = response.text
        print('Response status code: {}, and body: {}'.format(response_status_code,
                                                              response_as_text))
        return response_as_text if response_status_code == 200 else None

    def get_hash_key(self, key: str, hash_key: str) -> str:
        r""" get a key saved in redis and return str if it was possible get key
            else return None"
                        usage:
                            redis_response = redis_client.get_hash_key("your key, must be str",
                                                                       "your hash key, must be str")"""
        method = 'get'
        url = self.url_builder.get_url_for_hash_key(key, hash_key)
        response = self.__make_http_call(url=url, method=method)
        response_status_code = response.status_code
        response_as_text = response.text
        print('Response status code: {}, and body: {}'.format(response_status_code, response_as_text))
        return response_as_text if response_status_code == 200 else None

    def set_hash_key(self, **kwargs) -> bool:
        r""" save a hash key in redis and return a boolean if it was possible or not to save a key.
                usage:
                    redis_response = redis_client.set_key(key="your redis key, must be str",
                                                          hash_key="your hash key to save",
                                                          time="your time, must be int",
                                                          time_unit="your unit time, must be str or TimeUnitEnum",
                                                          data="your data to save, must be str")"""
        method = 'post'
        body = kwargs.get('data')
        key = kwargs.get('key')
        hash_key = kwargs.get('hash_key')
        time = kwargs.get('time')
        time_unit = kwargs.get('time_unit')
        parsed_time = self.__handle_time(time)
        parsed_time_unit = self.__handle_time_unit(time_unit)
        url = self.url_builder.get_url_for_hash_key(key, hash_key)
        headers = self.default_headers
        headers.__setitem__('time', str(parsed_time))
        headers.__setitem__('time-unit', str(parsed_time_unit.value))
        response = self.__make_http_call(url=url,
                                         method=method,
                                         body='"{}"'.format(body),
                                         headers=headers)
        response_status_code = response.status_code
        response_as_text = response.text
        print('Response status code: {}, and body: {}'.format(response_status_code, response_as_text))
        return response_status_code == 200

    def __make_http_call(self, **kwargs) -> requests.api:
        method = kwargs.get('method', None)
        url = kwargs.get('url', None)
        action = getattr(self.http_client, method, None)
        body = kwargs.get('body', None)
        headers = kwargs.get('headers', self.default_headers)
        return action(url=url, headers=headers, data=body)

    @staticmethod
    def __handle_time(time: int) -> int:
        if isinstance(time, int):
            return time
        if isinstance(time, str):
            local_time = int(time, 10)
            return local_time
        raise ValueError('Time must be a int you provided {} and type {}'.format(time, type(time)))

    @staticmethod
    def __handle_time_unit(time_unit) -> TimeUnitEnum:
        if isinstance(time_unit, TimeUnitEnum):
            return time_unit
        if isinstance(time_unit, str):
            if TimeUnitEnum.has_value(time_unit):
                return TimeUnitEnum[time_unit.upper()]
        raise ValueError('{} is not a valid time unit'.format(time_unit))

    def __generate_default_headers(self) -> dict:
        default_headers = {}
        default_headers.__setitem__('Content-Type', 'application/json')
        default_headers.__setitem__('x-name', self.application_name)
        default_headers.__setitem__('x-prefix', self.application_prefix)
        default_headers.__setitem__('x-api-key', self.api_key)
        return default_headers
