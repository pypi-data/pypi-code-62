# -*- coding: utf-8 -*-
"""
@author: kebo
@contact: kebo0912@outlook.com

@version: 1.0
@file: dataset_reader.py
@time: 2019/12/18 11:39

这一行开始写关于本文件的说明与解释


"""
from typing import Iterable, Iterator, Callable, List

from leslie.data.instance import Instance
from leslie.common.registrable import Registrable
from leslie.common.checks import ConfigurationError


class DatasetReader(Registrable):
    """
    dataset_reader basic
    """

    def read(self, file_path: str) -> List:
        instances = self._read(file_path=file_path)
        if not isinstance(instances, list):
            instances = [instance for instance in instances]
        if not instances:
            raise ConfigurationError("No instances were read from the given filepath {}. "
                                     "Is the path correct?".format(file_path))
        return instances

    def _read(self, file_path: str) -> Iterable:
        raise NotImplementedError

    def text_to_instance(self, *inputs) -> Instance:
        raise NotImplementedError
