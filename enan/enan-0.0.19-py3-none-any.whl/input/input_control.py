# -*- coding: utf-8 -*-
"""
Created on Sat May 30 13:05:34 2020

Data Control class

Analyzer o-- InputControl

@author: tadahaya
"""
import pandas as pd
import numpy as np

from .._utils.converter import SynoDict,FixedDict
from .data.data import *

# abstract factory
class InputControl():
    def __init__(self):
        self.obj = Data()
        self.ref = Data()
        self.dic = SynoDict()
        self.whole = set()

    def set_whole(self,whole):
        """ set whole features """
        self.whole = whole
        self.obj.set_whole(self.whole)
        self.ref.set_whole(self.whole)

    def set_dict(self,dic):
        """ set SynoDict or FixedDict """
        self.dic = dic
        self.obj.set_dict(self.dic)
        self.ref.set_dict(self.dic)
        whole = set(self.dic.values)
        self.set_whole(whole)

    def set_obj(self,data,conversion=True):
        """ create object Data instance for analysis """
        if len(self.whole)==0:
            raise ValueError("!! No Dict: set_dict() before set_obj() !!")
        self.obj.load(data)
        if conversion:
            self.obj.name2id()
        self.obj.adjust()

    def set_ref(self,data,conversion=True):
        """ create reference Data instance for analysis """
        if len(self.whole)==0:
            raise ValueError("!! No Dict: set_dict() before set_ref() !!")
        self.ref.load(data)
        if conversion:
            self.ref.name2id()
        self.ref.adjust()

    def get_obj(self):
        """ get object data instance """
        return self.obj.get()

    def get_ref(self):
        """ get reference data instance """
        return self.ref.get()

    def get_dict(self):
        """ get dict """
        return self.dic

    def get_whole(self):
        """ get whole """
        return self.whole


# concrete class
class FETDataControl(InputControl):
    def __init__(self):
        super().__init__()
        self.obj = SeqData()
        self.ref = SetData()


# concrete class
class BTDataControl(InputControl):
    def __init__(self):
        super().__init__()
        self.obj = SeqData()
        self.ref = SetData()


# concrete class
class GSEADataControl(InputControl):
    def __init__(self):
        super().__init__()
        self.obj = VectorData()
        self.ref = SetData()


# concrete class
class ssGSEADataControl(InputControl):
    def __init__(self):
        super().__init__()
        self.obj = VectorData()
        self.ref = SetData()


# concrete class
class ConnectivityDataControl(InputControl):
    def __init__(self):
        super().__init__()
        self.obj = VectorData()
        self.ref = SetTSData()