# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 13:05:34 2019

Data warehouse control class

Analyzer o-- DWHControl

@author: tadahaya
"""

### abstract factory
class DWHControl():
    def __init__(self):
        self.dic = StoredDict()
        self.ref = StoredRef()
        self.__state = dict()

    def load_dict(self,url): # delegation
        """ load a dictionary from data warehouse """
        raise NotImplementedError

    def get_dict(self): # delegation
        raise NotImplementedError

    def prep_dict(self): # delegation
        """ prepare a dictionary object """
        raise NotImplementedError

    def load_ref(self,url): # delegation
        """ load a dictionary from data warehouse """
        raise NotImplementedError

    def get_ref(self): # delegation
        raise NotImplementedError

    def prep_ref(self): # delegation
        """ prepare a reference object """
        raise NotImplementedError

    def get_state(self):
        """ get states of objects """
        raise NotImplementedError


# abstract product 1
class StoredDict():
    def __init__(self):
        self.dic = None

    def load_(self):
        """ load a dictionary from data warehouse """
        raise NotImplementedError

    def get_(self):
        raise NotImplementedError

    def prep_(self):
        """ prepare a dictionary object """
        raise NotImplementedError

    def get_state(self):
        """ get the state of a dictionary object """
        raise NotImplementedError


# abstract product 2
class StoredRef():
    def __init__(self):
        self.ref = None

    def get_(self):
        raise NotImplementedError

    def load_(self):
        """ load a reference from data warehouse """
        raise NotImplementedError

    def prep_(self):
        """ prepare a reference object """
        raise NotImplementedError

    def get_state(self):
        """ get the state of a dictionary object """
        raise NotImplementedError