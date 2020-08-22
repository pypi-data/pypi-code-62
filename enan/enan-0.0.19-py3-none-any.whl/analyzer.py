# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 13:05:34 2019

Analyzer class

@author: tadahaya
"""
import pandas as pd
import numpy as np

from .input.input_control import InputControl
from .dwh.dwh_control import DWHControl
from .dwh.gene.gene_control import GeneControl
from .dwh.chem.chem_control import ChemControl
from .preprocess.preprocessor import PreProcessor

# abstract class
class Analyzer():
    def __init__(self):
        self.data = InputControl()
        self.__dwh = DWHControl()
        self.__prepro = PreProcessor()
        self.__calc = None
        self.__plot = None
        self.__whole = set()
        self.__dic = None
        self.__ref = None
        self.__obj = None
        self.res = None

    ### input control ###
    def set_dict(self,dic):
        """ set a dict data instance """
        self.data.set_dict(dic)
        self.__dic = self.data.get_dict()

    def set_whole(self,whole):
        """ set whole features """
        self.data.set_whole(whole)
        self.__whole = self.data.get_whole()

    def set_ref(self,data,conversion=True):
        """ set a reference data instance """
        self.data.set_ref(data=data,conversion=conversion)
        self.__ref = self.data.get_ref()

    def set_obj(self,data,conversion=True):
        """ set an object data instance """
        self.data.set_obj(data=data,conversion=conversion)
        self.__obj = self.data.get_obj()

    def get_dict(self):
        """ get a dict data instance """
        return self.data.get_dict()

    def get_ref(self):
        """ get reference data instance """
        return self.data.get_ref()

    def get_obj(self):
        """ get an object data instance """
        return self.data.get_obj()

    def get_whole(self):
        return self.__whole


    ### data preprocessing ###
    def call_PreProcessor(self):
        """
        generate Preprocessor object
        - dictionary preparation
        - data preprocessing
        
        """
        return self.__prepro


    ### stored data handling ###
    def gene(self,dic="biomart",ref="",species="human"):
        """ switch to GeneControl """
        print("choose below")
        print("- dic: biomart")
        print("- ref: enrichr, msigdb")
        self.__dwh = GeneControl(dic,ref)
        try:
            self.load_dict(species=species)
        except KeyError:
            raise KeyError("!! Wrong key. Choose human, mouse, or rat !!")

    def chem(self,dic="",ref=""):
        """ switch to ChemControl """
        print("choose below")
        print("- dic: XXXX")
        print("- ref: XXXX")
        self.__dwh = ChemControl(dic,ref)

    def load_dict(self,**kwargs):
        """ load a stored dictionary """
        self.__dwh.load_dict(**kwargs)
        dic = self.__dwh.get_dict()
        self.set_dict(dic)
        self.set_whole(set(dic.values))

    def prep_dict(self,**kwargs):
        """ prepare a dict from data warehouse """
        self.__dwh.prep_dict(**kwargs)

    def load_ref(self,**kwargs):
        """ load a stored reference """
        self.__dwh.load_ref(**kwargs)
        ref = self.__dwh.get_ref()
        self.set_ref(ref,conversion=False)
        print(self.__dwh.get_state())

    def prep_ref(self,**kwargs):
        """ prepare a reference from data warehouse """
        self.__dwh.prep_ref(**kwargs)
        ref = self.__dwh.get_ref()
        self.set_ref(ref,conversion=False)
        print(self.__dwh.get_state())


    ### calculator ###
    # abstract method
    def calc(self):
        raise NotImplementedError


    ### visualization ###
    # abstract method
    def plot(self):
        raise NotImplementedError