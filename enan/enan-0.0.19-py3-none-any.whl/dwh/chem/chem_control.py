# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 13:05:34 2019

Data warehouse control class

Analyzer o-- DWHControl <|.. ChemControl

@author: tadahaya
"""
import pandas as pd
import numpy as np

from ..dwh_control import DWHControl
from .chem_dict import *
from .chem_ref import *

class ChemControl(DWHControl):
    def __init__(self,dic="",ref=""):
        self.__state = {"dict":"","ref":""}
        if dic=="xxxx":
            self.dic = some_dict.SomeDict()
        else:
            self.dic = None
        if ref=="xxxx":
            self.ref = some_ref.SomeReff()
        else:
            self.ref = None
        if self.dic is not None:
            self.__state["dict"] = self.dic.get_state()
        if self.ref is not None:
            self.__state["ref"] = self.ref.get_state()

    # change dict
    def to_somedict(self):
        """ switch to XXXX """
        self.dic = some_dict.SomeDict()

    # change ref
    def to_SomeRef(self):
        """ switch to XXXX """
        self.ref = some_ref.SomeRef()

    # realization
    def load_dict(self,**kwargs): # delegation
        """ load a gene dictionary from data warehouse """
        self.dic.load_(**kwargs)
        self.__state["dict"] = self.dic.get_state()
        
    def get_dict(self): # delegation
        return self.dic.get_()

    def prep_dict(self,**kwargs): # delegation
        """ prepare a gene dictionary from data warehouse """
        self.dic.prep_(**kwargs)

    def load_ref(self,**kwargs): # delegation
        """ load a gene reference from data warehouse """
        self.ref.load_(**kwargs)
        self.__state["ref"] = self.ref.get_state()
        
    def get_ref(self): # delegation
        return self.ref.get_()

    def prep_ref(self,**kwargs): # delegation
        """ prepare a gene reference from data warehouse """
        self.ref.prep_(**kwargs)

    def get_state(self):
        """ get states of objects """
        return self.__state