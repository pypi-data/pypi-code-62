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
"""
A pure Python object-mapper for the Oslo Bysykkel API

This module provides some classes that create a nice abstraction layer
from the JSON content presented by the API. Hence making it easier and more
intuitive to manipulate the data fetched from the API.
"""


class Station:
    """
    Station-class that represents a single station and its information
    as presented by the API.

    The Station contains the merged information from both:
    https://gbfs.urbansharing.com/oslobysykkel.no/station_information.json
    https://gbfs.urbansharing.com/oslobysykkel.no/station_status.json

    It is in a way a complete station.
    """
    def __init__(self, **kwargs):
        """
        Constructs a new StationStatus object from
        the station_status JSON attributes
        """
        self._kwargs = kwargs
        # sanity check that checkes if all needed attributes are really set
        # can be implemented here

        # the station-information data corresponding to this object is to be
        # set later

    def __str__(self):
        """A printable str representation of the object"""
        return (f'{self.station_id} - {self.name} - '
                f'{self.num_docks_available} - {self.num_bikes_available}')

    # all properties / attributes are read-only
    def __getattr__(self, name):
        """Fetches all the attributes set in self._kwargs"""
        if name not in self._kwargs:
            raise AttributeError
        return self._kwargs[name]

    def __getitem__(self, key):
        """Implements evaluation of self[key]"""
        return self._kwargs[key]

    @classmethod
    def from_dict(cls, dict_obj):
        """
        Returns a Station object from the dict-object.

        :param dict_obj: The dict object
        :type dict_obj: dict

        :return: A new Station-object
        :rtype: Station
        """
        return cls(**dict_obj)

    def set_station_information_data(self, **kwargs):
        """
        Sets / updates the station information contents.

        Can be called many times.
        """
        # sanity check may be performed here in the future
        self._kwargs.update(kwargs)


class StationCollection:
    """
    Station collection-class that represents all stations as presented by
    the API.

    Instance(s) of this class serve as container object for the Station
    objects.
    """
    def __init__(self):
        """Constructs a StationCollection-object"""
        self._station_list = []
        # a station_id to Station-object mapper (dict) can be used in the
        # future if one desires faster lookup for individual stations

    def __iter__(self):
        """Iterator implementation"""
        return iter(self._station_list)

    def __len__(self):
        """Len implementation"""
        return len(self._station_list)

    def sort_by_key(self, key):
        """
        Sorts the collection (all Station objects) *in place* by `key`.

        This method does not return any value, but rather changes the state
        of the collection and the order of the Station objects.

        :param key: The key to sort by
        :type key: str
        """
        self._station_list.sort(key=lambda s: s[key])

    @property
    def stations(self):
        """stations-property"""
        # the reference can be used by the caller to modify the list
        # return tuple(self._station_list) or a new list if that is a problem
        return self._station_list

    def append_station(self, station_obj):
        """
        Appends a single station into the collection.

        :param station_obj: The Station-object to be appended
        :type station_obj: Station
        """
        # sanity and type checks can be performed here
        self._station_list.append(station_obj)
