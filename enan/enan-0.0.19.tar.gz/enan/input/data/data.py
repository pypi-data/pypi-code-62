# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 13:05:34 2019

Data class

Analyzer o-- InputControl *-- Data

@author: tadahaya
"""
import pandas as pd
import numpy as np

from .converter import *
from .adjuster import *

__all__ = ["Data","SeqData","SetData","SetTSData","VectorData"]

# abstract class
class Data():
    def __init__(self):
        self.data = None
        self.not_found = set()
        self.dic = None
        self.whole = set()
        self.__conv = None
        self.__adj = None

    def get(self):
        """ get data """
        return self.data

    def set_whole(self,whole):
        """ set whole """
        self.whole = whole

    def set_dict(self,dic):
        """ set dictionary for ID conversion """
        self.dic = dic

    def load(self,data):
        """ load data """
        raise NotImplementedError

    def name2id(self):
        """ convert name to ID """
        raise NotImplementedError

    def id2name(self):
        """ convert ID to name """
        raise NotImplementedError

    def adjust(self,**kwargs):
        """ adjust data to the indicated whole """
        raise NotImplementedError


# concrete class
class SeqData(Data):
    """ data given as a set """
    def __init__(self):
        super().__init__()
        self.data = {}
        self.__conv = SeqConverter()
        self.__adj = SeqAdjuster()

    def load(self,data):
        """ load data """
        if type(data)!=set:
            raise TypeError("!! data should be a set !!")
        self.data = data

    def name2id(self):
        """ convert name to ID """
        self.data,self.not_found = self.__conv.name2id(self.data,self.dic)

    def id2name(self):
        """ convert ID to name """
        self.data,self.not_found = self.__conv.id2name(self.data,self.dic)

    def adjust(self,**kwargs):
        """ adjust data to the indicated whole """
        self.data = self.__adj.adjust(self.data,self.whole,**kwargs)


# concrete class
class SetData(Data):
    """ data given as a dict of {term:sets of group} """
    def __init__(self):
        super().__init__()
        self.data = dict()
        self.__conv = SetConverter() # private
        self.__adj = SetAdjuster() # private

    def load(self,data):
        """ load data """
        if type(data)!=dict:
            raise TypeError("!! data should be a dict !!")
        self.data = data

    def name2id(self):
        """ convert name to ID """
        self.data,self.not_found = self.__conv.name2id(self.data,self.dic)

    def id2name(self):
        """ convert ID to name """
        self.data,self.not_found = self.__conv.id2name(self.data,self.dic)

    def adjust(self,**kwargs):
        """ adjust data to the indicated whole """
        self.data = self.__adj.adjust(self.data,self.whole,**kwargs)


# concrete class
class SetTSData(Data):
    """ data given as a dict of {term:tuples of up/down tags} """
    def __init__(self):
        super().__init__()
        self.data = dict()
        self.__conv = SetTSConverter() # private
        self.__adj = SetTSAdjuster() # private

    def load(self,data):
        """ load data """
        if type(data)!=dict:
            raise TypeError("!! data should be a dict !!")
        elif type(list(data.values())[0])!=tuple:
            raise TypeError("!! data should be a dict of tuples of up/down tags !!")
        self.data = data

    def name2id(self):
        """ convert name to ID """
        self.data,self.not_found = self.__conv.name2id(self.data,self.dic)

    def id2name(self):
        """ convert ID to name """
        self.data,self.not_found = self.__conv.id2name(self.data,self.dic)

    def adjust(self,**kwargs):
        """ adjust data to the indicated whole """
        self.data = self.__adj.adjust(self.data,self.whole,**kwargs)


# concrete class
class VectorData(Data):
    """ data given as a dataframe """
    def __init__(self):
        super().__init__()
        self.data = pd.DataFrame()
        self.__conv = VectorConverter() # private
        self.__adj = VectorAdjuster() # private

    def load(self,data):
        """ load data """
        if type(data)==pd.core.series.Series:
            self.data = pd.DataFrame(data)
        elif type(data)==pd.core.frame.DataFrame:
            self.data = data
        else:
            raise TypeError("!! data should be a dataframe !!")

    def name2id(self):
        """ convert name to ID """
        self.data,self.not_found = self.__conv.name2id(self.data,self.dic)

    def id2name(self):
        """ convert ID to name """
        self.data,self.not_found = self.__conv.id2name(self.data,self.dic)

    def adjust(self,**kwargs):
        """ adjust data to the indicated whole """
        self.data = self.__adj.adjust(self.data,self.whole,**kwargs)