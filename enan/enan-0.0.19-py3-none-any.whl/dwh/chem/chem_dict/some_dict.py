# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 13:05:34 2019

Data warehouse control class

Analyzer o-- DWHControl <|.. ChemControl <|.. SomeDict

@author: tadahaya
"""
import pandas as pd
import os

from ...._utils.converter import SynoDict
from ...dwh_control import StoredDict

# concrete class
class SomeDict(StoredDict):
    def __init__(self):
        self.dic = SynoDict()
        self.__base = os.path.dirname(__file__) # ~\enapy\dwh\chem\chem_dict
        self.__state = {"database":"","name":""}

    def get_(self):
        return self.dic

    def load_(self):
        raise NotImplementedError

    def prep_(self):
        raise NotImplementedError

    def get_state(self):
        return self.__state