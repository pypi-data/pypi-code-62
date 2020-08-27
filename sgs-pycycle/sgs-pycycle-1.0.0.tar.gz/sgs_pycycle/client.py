# -*- coding: utf-8 -*-
# SPDX-License-Identifier: BSD-2-Clause-FreeBSD
#
# Copyright (c) 2020, Simeon Simeonov
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHORS ``AS IS'' AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
# OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
# NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
# THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""A pure Python client for the Oslo Bysykkel API"""

import json
import urllib.error
import urllib.request

from sgs_pycycle.models import Station, StationCollection


class ClientConnectionError(Exception):
    """
    Client-connection error exception

    Encapsulates all errors related to network problems, wrong URLs, SSL, etc..
    """


class ClientDataError(Exception):
    """
    Client data error exception

    Reaised when the client is not able to handle the response-data
    """


class ClientError(Exception):
    """
    Client error exception

    Raised when the client detects wrong input or when unexpected condition
    arises
    """


class Client:
    """The Client-class encapsulating the client functionality"""

    def __init__(self, auto_discovery_url, identifier='sgs-pycycle'):
        """
        Constructs a Client object.

        :param auto_discovery_url: The URL of the auto discovery endpoint
        :type auto_discovery_url: str

        :param identifier: The Client-Identifier string required by the API
        :type identifier: str

        :raises sgs_pycycle.ClientError: If the input does not validate
        """
        # Additional values like socket timeout, SSL-context, etc.. can also
        # be provided either through external configuration resource or through
        # parameters (or both).

        # some explicit type checking
        if (
                not isinstance(auto_discovery_url, str) or
                not isinstance(identifier, str)
        ):
            raise ClientError(
                'auto_discovery_url and identifier must be of type str')
        self._auto_discovery_url = auto_discovery_url
        self._identifier = identifier

    def get_station_collection(self):
        """
        Returns StationCollection object corresponding to the API data.

        Once fetched the data can be sorted and manipulated using the
        StationCollection module.

        :raises sgs_pycycle.ClientConnectionError: For connection and network
                                                   related errors

        :raises sgs_pycycle.ClientDataError: For content / payload errors

        :raises sgs_pycycle.ClientError: For all other errors

        :return: The StationCollection object corresponding to the API data
        :rtype: sgs_pycycle.StationCollection
        """
        try:
            # maps the ID to a newly created Station-object
            station_id_mapper = {}

            all_data = self._fetch_all_from_API()
            station_collection = StationCollection()
            # we start by going through all station-status data and
            # creating Station objects
            for sdata in all_data['station_status']['data']['stations']:
                station_id_mapper[sdata['station_id']] = Station(**sdata)
            for sdata in all_data['station_information']['data']['stations']:
                if sdata['station_id'] not in station_id_mapper:
                    raise ClientDataError(f"station_id {sdata['station_id']} "
                                          "not found in station_status")
                station_id_mapper[
                    sdata['station_id']].set_station_information_data(**sdata)
                station_collection.append_station(
                    station_id_mapper[sdata['station_id']])
            return station_collection
        except (ClientConnectionError, ClientDataError, ClientError):
            # re-raise the already identified exceptions
            raise
        except Exception as err:
            raise ClientError(str(err))

    def _fetch_all_endpoints(self):
        """
        Fetches all endpoints and returns a dict corresponding to
        the JSON content returned by the API

        :return: All endpoints found in self._auto_discovery_url
        :rtype: dict
        """
        # It is possible to call this method upon the initialization of the
        # Client-object and make the object cache the reponse for better
        # performance, assuming that auto discovery data is not changed often
        try:
            req = urllib.request.Request(
                self._auto_discovery_url,
                headers={'Client-Identifier': self._identifier})
            response = urllib.request.urlopen(req)
            if response.code != 200:
                raise ClientConnectionError('API did not return 200')
            # API-encoding can be moved to an external configuration resource
            return json.loads(response.read().decode('utf-8'))
        except (urllib.error.HTTPError, urllib.error.URLError) as err:
            raise ClientConnectionError(str(err))
        except json.decoder.JSONDecodeError as err:
            raise ClientDataError(str(err))
        except Exception as err:
            raise ClientError(str(err))

    def _fetch_all_from_API(self):
        """
        Fetches raw (JSON) data from each endpoint presented in the
        self._auto_discovery_url

        :return: Dictionary with endpoint-name as key and payload dict as value
        :rtype: dict
        """
        try:
            endpoint_data = {}
            endpoints_dict = self._fetch_all_endpoints()
            # the 'last_updated' attribute can be used to implement caching
            # instead of fetching all data everytime this method is called
            for endpoint in endpoints_dict['data']['nb']['feeds']:
                req = urllib.request.Request(
                    endpoint['url'],
                    headers={'Client-Identifier': self._identifier})
                response = urllib.request.urlopen(req)
                if response.code != 200:
                    raise ClientConnectionError('API did not return 200')
                endpoint_data[endpoint['name']] = (
                    json.loads(response.read().decode('utf-8')))
            return endpoint_data
        except (ClientConnectionError, ClientDataError, ClientError):
            # re-raise the already identified exceptions
            raise
        except (urllib.error.HTTPError, urllib.error.URLError) as err:
            raise ClientConnectionError(str(err))
        except json.decoder.JSONDecodeError as err:
            raise ClientDataError(str(err))
        except KeyError:
            # JSONPATH library can be used to move the JSON structure into
            # an external configuration resource
            raise ClientDataError(
                'Modified or corrupt JSON structure in auto discovery')
        except Exception as err:
            raise ClientError(str(err))
