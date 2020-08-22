# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 13:05:34 2019

FET class

@author: tadahaya
"""
import pandas as pd
import numpy as np

from .dwh.gene.gene_control import GeneControl
from .dwh.chem.chem_control import ChemControl
from .preprocess.preprocessor import PreProcessor
from .analyzer import Analyzer
from .input.input_control import FETDataControl
from .calculator._fet import Calculator
from .plot._plot import PlotFET

# abstract class
class FET(Analyzer):
    def __init__(self):
        self.data = FETDataControl()
        self.__dwh = GeneControl()
        self.__prepro = PreProcessor()
        self.__calc = Calculator()
        self.__plot = PlotFET()
        self.__whole = set()
        self.__dic = None
        self.__ref = dict()
        self.__obj = set()
        self.res = pd.DataFrame()

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
    def gene(self,dic="biomart",ref="enrichr",species="human"):
        """ switch to GeneControl """
        if dic not in ["biomart"]:
            raise KeyError("!! Wrong key for dic. Choose biomart !!")
        if ref not in ["enrichr","msigdb"]:
            raise KeyError("!! Wrong key for ref. Choose enrichr or msigdb !!")
        self.__dwh = GeneControl(dic,ref)
        try:
            self.load_dict(species=species)
        except KeyError:
            raise KeyError("!! Wrong key for species. Choose human, mouse, or rat !!")

    def chem(self,dic="",ref=""):
        """ switch to ChemControl """
        raise NotImplementedError
        if dic not in ["XXXX"]:
            raise KeyError("!! Wrong key for dic. Choose XXXX !!")
        if ref not in ["XXXX"]:
            raise KeyError("!! Wrong key for ref. Choose XXXX !!")
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


    ### calculation ###
    def calc(self,**kwargs): # realization
        """
        calculate Fisher's exact test p value corrected for multiple tests
        
        Parameters
        ----------            
        correction: str
            indicate method for correcting multiple tests
            depend on "statsmodels.stats.multitest.multipletests"
            
        focus: int
            export results by XX th lowest p value
        
        mode: int
            indicate the type of test
            "two-sided", "less", "greater"
            in many case of ontology analysis, "greater" is appropriate
    
        """
        res = self.__calc.calc(obj=self.__obj,ref=self.__ref,whole=self.__whole,**kwargs)
        ol = res["overlap"].values.tolist()
        ol = [self.__dic.dec_set(v) for v in ol]
        res["overlap"] = ol
        self.res = res
        return res


    ### visualization ###
    def load_res(self,df):
        """ load result data for visualization """
        self.res = df


    def plot(self,**kwargs): # realization
        """
        visualize a result of enrichment analysis

        Parameters
        ----------
        focus: int
            determine how many groups are visualized

        fileout: str
            indicate the path for the output image

        dpi: int
            indicate dpi of the output image
            
        thresh: float
            indicate the threshold value of adjusted p value to be colored

        xlabel,ylabel: str
            indicate the name of x and y axes

        title: str
            indicate the title of the plot

        color: str
            indicate the color of the bars

        alpha: float
            indicate transparency of the bars: (0,1)

        height: float
            indicate the height of the bars

        fontsize: float
            indicate the fontsize in the plot

        textsize: float
            indicate the fontsize of the texts in the bars

        figsize: tuple
            indicate the size of the plot

        """
        self.__plot.plot(res=self.res,**kwargs)