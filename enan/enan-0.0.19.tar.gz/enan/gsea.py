# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 13:05:34 2019

GSEA class

@author: tadahaya
"""
import pandas as pd
import numpy as np

from .dwh.gene.gene_control import GeneControl
from .dwh.chem.chem_control import ChemControl
from .preprocess.preprocessor import PreProcessor
from .analyzer import Analyzer
from .input.input_control import GSEADataControl
from .calculator._gsea import Calculator
from .plot._plot import PlotGSEA

# abstract class
class GSEA(Analyzer):
    def __init__(self):
        self.data = GSEADataControl()
        self.__dwh = GeneControl()
        self.__prepro = PreProcessor()
        self.__calc = Calculator()
        self.__plot = PlotGSEA()
        self.__whole = set()
        self.__dic = None
        self.__ref = dict()
        self.__obj = set()
        self.__method = ""
        self.alpha = 0.0
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
    def calc(self,method="standard",alpha=0): # realization
        """
        conduct GSEA

        Parameters
        -------
        method: str
            indicate a method for calculating the enrichment score
            "starndard": employed in the original paper Barbie, et al, 2009
            "kuiper": Kuiper test statistics, good when up/down genes are mixed, tail sensitive
            "gsva": GSVA like statistics, good when unidirection (ex. up only)

        alpha: float, (0,1]
            indicate weight of center
            0 means no weight and is employed well

        Returns res
        -------
        res: df
            gene set enrichment score

        """
        self.__method = method
        self.__alpha = alpha
        if method=="standard":
            self.__calc.to_standard()
            print("Standard method")
        elif method=="kuiper":
            self.__calc.to_kuiper()
            print("Kuiper method")
        elif method=="gsva":
            self.__calc.to_gsva()
            print("GSVA method")
        else:
            raise ValueError("!! Wrong method: choose 'standard', 'kuiper', or 'gsva' !!")
        data = self.__obj.copy()
        col = list(data.columns)
        res = []
        ap = res.append
        for v in col:
            ap(self.__calc.calc(obj=data[v],ref=self.__ref,alpha=alpha))
        res = pd.concat(res,axis=1,join="inner")
        res.columns = col
        self.res = res
        return res


    ### visualization ###
    def load_res(self,df):
        """ load result data for visualization """
        self.res = df


    def plot(self,highlight=[],focus=None,ylabel="enrichment score",**kwargs): # realization
        """
        visualize a result of GSEA
        Parameters
        ----------
        focus: str
            indicate the sample name to be visualized

        highlight: list
            indicate the plots to be highlightened

        fileout: str
            indicate the path for the output image

        dpi: int
            indicate dpi of the output image
            
        ylabel: str
            indicate the name of y axis

        title: str
            indicate the title of the plot

        color: str
            indicate the color of the bars
            
        fontsize: float
            indicate the fontsize in the plot

        size: float
            indicate the size of the plot

        figsize: tuple
            indicate the size of the plot
        """
        if focus is None:
            col = list(self.res.columns)
            for v in col:
                self.__plot.plot(data=self.res[v],highlight=highlight,ylabel=ylabel,**kwargs)
        else:
            focused = self.res[focus]
            self.__plot.plot(data=focused,highlight=highlight,ylabel=ylabel,**kwargs)
        

    def plot_running(self,focus=None,fterm="",title="",**kwargs): # realization
        """
        visualize a result of GSEA, running sum plot
        Parameters
        ----------
        focus: str
            indicate the sample name to be visualized

        fterm: str or int
            indicate the term of interest or the corresponding No.

        fileout: str
            indicate the path for the output image

        dpi: int
            indicate dpi of the output image
            
        xlabel,ylabel: str
            indicate the name of x and y axes

        title: str
            indicate the title of the plot

        color: str
            indicate the color of the bars

        fontsize: float
            indicate the fontsize in the plot

        figsize: tuple
            indicate the size of the plot

        """
        if focus is None:
            raise ValueError("!! Indicate focus !!")
        data = self.__obj.copy()
        focused = data[focus]
        res = self.__calc.calc(obj=focused,ref=self.__ref,alpha=self.__alpha)
        es = self.__calc.es
        keys = self.__calc.keys
        if len(es)==0:
            raise ValueError("!! No Enrichment score !!")
        else:
            if type(fterm)==str:
                focus_key = fterm
                try:
                    focus_num = keys.index(fterm)
                except KeyError:
                    print("!! Wrong key: change fterm !!")
            elif type(fterm)==int:
                if len(es) < fterm:
                    raise ValueError("!! focused number is larger than column No. !!")
                focus_num = fterm
                focus_key = keys[fterm]
            else:
                raise TypeError("!! Wrong type: focus should be str or int !!")
        if len(title) > 0:
            self.__plot.plot_running(es=es,focus=focus_num,title=title,**kwargs)
        else:
            self.__plot.plot_running(es=es,focus=focus_num,title=focus_key,**kwargs)
