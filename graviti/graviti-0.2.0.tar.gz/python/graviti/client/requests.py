#!/usr/bin/env python3
#
# Copyright 2020 Graviti. All Rights Reserved.
#

"""This file define class Client and function read_data_from_file.
"""

import logging
from concurrent.futures import FIRST_EXCEPTION, Future, wait  # pylint: disable=unused-import
from typing import Any, Dict, List, Optional

import requests

from .exceptions import GASOSSError, GASRequestError, GASResponseError, GASTensorBayError
from .log import dump_request_and_response

logger = logging.getLogger(__name__)


class Client:  # pylint: disable=too-few-public-methods
    """This is a base class defining the concept of Client,
    which contains functions to send post to content store and labelset store

    :param access_key: user's access key
    :param gateway_url: the gateway url of the gas website
    """

    def __init__(self, access_key: str, gateway_url: str) -> None:
        self._access_key = access_key
        self._gateway_url = gateway_url

    def _dataset_post(self, method: str, post_data: Dict[str, Any]) -> Any:
        url = self._gateway_url + "content-store/" + method
        return post(url, json_data=post_data, access_key=self._access_key)

    def _labelset_post(self, method: str, post_data: Dict[str, Any]) -> Any:
        url = self._gateway_url + "label-store/" + method
        return post(url, json_data=post_data, access_key=self._access_key)


def cancel_all_tasks_when_first_exception(futures: List["Future[Any]"]) -> None:
    """Wait for the futures in the given sequence to complete.
    This function will return if one of below condition happens
    1. All futures finish.
    2. Any future finishes by raising an exception.
    If it returns by condition 2, the remaining tasks will be all canceled
    """
    done, not_done = wait(futures, return_when=FIRST_EXCEPTION)
    for future in not_done:
        future.cancel()
    for future in done:
        future.result()


def post(
    url: str,
    *,
    data: Optional[bytes] = None,
    json_data: Optional[Dict[str, Any]] = None,
    content_type: Optional[str] = None,
    access_key: Optional[str] = None,
) -> Any:
    """Send a POST requests

    :param url: URL for the request
    :param data: bytes data to send in the body of the request
    :param json_data: json data to send in the body of the request
    :param content_type: Content-Type to send in the header of the request
    :param token: X-Token to send in the header of the request
    :raises GASRequestError: When post request failed
    :raises GASResponseError: When response.ok is False
    :raises GASTensorBayError: When response content 'success' is False
    :raises GASOSSError: When response is return by AliyunOSS and content 'status' is not 'OK'
    :return: response of the request
    """
    headers: Dict[str, str] = {}
    if access_key:
        headers["X-Token"] = access_key
    if content_type:
        headers["Content-Type"] = content_type

    try:
        response = requests.post(url, data=data, json=json_data, headers=headers)
    except requests.RequestException as error:
        raise GASRequestError(error)

    return _parser_response(response)


def get(url: str, params: Dict[str, Any]) -> Any:
    """Send a GET requests

    :param url: URL for the request
    :param params: Dictionary to send in the query string for the `Request`
    :raises GASRequestError: When post request failed
    :raises GASResponseError: When response.ok is False
    :raises GASTensorBayError: When response content 'success' is False
    :return: response of the request
    """
    try:
        response = requests.get(url, params=params, headers={"Accept": "application/json"})
    except requests.RequestException as error:
        raise GASRequestError(error)

    return _parser_response(response)


def _parser_response(response: requests.Response) -> Any:
    if not response.ok:
        raise GASResponseError(response)

    content_type = response.headers["Content-Type"]
    if not content_type.startswith("application/json"):
        logger.debug(dump_request_and_response(response))
        return response.content

    result = response.json()

    if response.headers.get("Server", None) == "AliyunOSS":
        if result["status"] != "OK":
            raise GASOSSError(response)
        logger.debug(dump_request_and_response(response))
        return result

    if not result["success"]:
        raise GASTensorBayError(response)

    logger.debug(dump_request_and_response(response))
    return result["data"]
