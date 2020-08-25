#!/usr/bin/env python3
#
# Copyright 2020 Graviti. All Rights Reserved.
#

"""This file defines class Frame."""

from typing import Any, Dict, Iterator, List, MutableMapping, Optional

from .data import Data


class Frame(MutableMapping[str, Data]):
    """This class defines the concept of frame, which represents a list of Data with sensor info.

    :param loads: [
        data_dict{...}, <must contains sensor info>
        data_dict{...},
        ...
        ...
    [
    """

    def __init__(self, *, loads: Optional[List[Dict[str, Any]]] = None) -> None:
        self._data: Dict[str, Data] = {}

        if loads:
            for data_dict in loads:
                self._data[data_dict["sensor"]] = Data(loads=data_dict)

    def dumps(self) -> List[Dict[str, Any]]:
        """dump a Frame into a list"""

        data_list: List[Dict[str, Any]] = []
        for key, value in self._data.items():
            data_dict = value.dumps()
            data_dict["sensor"] = key
            data_list.append(data_dict)
        return data_list

    def __getitem__(self, key: str) -> Data:
        return self._data.__getitem__(key)

    def __setitem__(self, key: str, value: Data) -> None:
        self._data.__setitem__(key, value)

    def __delitem__(self, key: str) -> None:
        self._data.__delitem__(key)

    def __len__(self) -> int:
        return self._data.__len__()

    def __iter__(self) -> Iterator[str]:
        return self._data.__iter__()

    def __str__(self) -> str:
        str_list = [f"{self.__class__.__name__}{{"]
        for key, value in self._data.items():
            str_list.append(f'  "{key}": {value},')
        str_list.append("}")

        return "\n".join(str_list)

    def __repr__(self) -> str:
        return self.__str__()
