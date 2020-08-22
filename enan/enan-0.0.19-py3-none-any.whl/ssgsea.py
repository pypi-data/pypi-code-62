# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 13:05:34 2019

ssGSEA class

@author: tadahaya
"""
import pandas as pd
import numpy as np

from tqdm import tqdm

from .dwh.gene.gene_control import GeneControl
from .dwh.chem.chem_control import ChemControl
from .preprocess.preprocessor import PreProcessor
from .analyzer import Analyzer
from .input.input_control import ssGSEADataControl
from .calculator._gsea import Calculator
from .plot._plot import PlotSsGSEA

# abstract class
class ssGSEA(Analyzer):
    def __init__(self):
        self.data = ssGSEADataControl()
        self.__dwh = GeneControl()
        self.__prepro = PreProcessor()
        self.__calc = Calculator()
        self.__plot = PlotSsGSEA()
        self.__whole = set()
        self.__dic = None
        self.__ref = dict()
        self.__obj = set()
        self.__method = ""
        self.alpha = 0.0
        self.__fterm = None
        self.__mode = None
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
    def calc(self,fterm=None,method="standard",alpha=0.25): # realization
        """
        conduct ssGSEA

        Parameters
        -------
        fterm: str or int
            indicate the term of interest or the corresponding No.

        method: str
            indicate a method for calculating the enrichment score
            "starndard": employed in the original paper Barbie, et al, 2009
            "kuiper": Kuiper test statistics, good when up/down genes are mixed, tail sensitive
            "gsva": GSVA like statistics, good when unidirection (ex. up only)

        alpha: float, (0,1]
            indicate weight of center
            0.25 is employed in the original paper (Barbie,et al.,2009)

        Returns res
        -------
        res: df
            gene set enrichment score

        """
        self.__method = method
        self.__alpha = alpha
        self.__fterm = fterm
        if method=="standard":
            self.__calc.to_standard()
            print("Standard method",flush=True)
        elif method=="kuiper":
            self.__calc.to_kuiper()
            print("Kuiper method",flush=True)
        elif method=="gsva":
            self.__calc.to_gsva()
            print("GSVA method",flush=True)
        else:
            raise ValueError("!! Wrong method: choose 'standard', 'kuiper', or 'gsva' !!")
        data = self.__obj.copy()
        col = list(data.columns)
        if fterm is None:
            self.__mode = "exploratory"
            self.__calc.to_expssgsea()
            res = []
            ap = res.append
            for v in tqdm(col):
                ap(self.__calc.calc(obj=data[v],ref=self.__ref,alpha=alpha))
            res = pd.concat(res,axis=1,join="inner")
            res.columns = col
        else:
            self.__mode = "focused"
            self.__calc.to_ssgsea()
            self.__fterm = fterm
            res = self.__calc.calc(obj=data,ref=self.__ref,alpha=alpha,fterm=fterm)
        self.res = res
        return res


    ### visualization ###
    def load_res(self,df):
        """ load result data for visualization """
        self.res = df


    def plot(self,keyword=[],fterm=None,mode=None,**kwargs): # realization
        """
        visualize a result of enrichment analysis

        Parameters
        ----------
        fterm: str
            indicate the group of interest

        mode: str
            indicate ssGSEA mode: 'exploratory' or 'focused'
            if None (default), plot the current result

        keyword: list
            indicate samples to be visualized

        fileout: str
            indicate the path for the output image

        dpi: int
            indicate dpi of the output image
            
        xlabel,ylabel: str
            indicate the name of x and y axes

        title: str
            indicate the title of the plot

        color: str
            indicate the color of swarmplot (if sample size is less than 30)

        palette: list
            indicate color of boxplot

        alpha: float
            indicate transparency of the bars: (0,1)

        size: float
            size of the markers

        fontsize: float
            indicate the fontsize in the plot

        textsize: float
            indicate the fontsize of the texts in the bars

        figsize: tuple
            indicate the size of the plot

        """
        if mode is None: # plot the current result
            if self.__mode=="exploratory":
                # exploratory mode
                if fterm is None:
                    raise ValueError("!! Indicate fterm (focused term) !!")
                else:
                    data = self.res.T[fterm]
                    self.__plot.plot(data=data,keyword=keyword,focus=fterm,**kwargs)
            elif self.__mode=="focused":
                # focused mode
                self.__plot.plot(data=self.res,keyword=keyword,focus=self.__fterm,**kwargs)
            else:
                raise ValueError("!! Indicate mode: 'exploratory' or 'focused' !!")
        elif mode=="exploratory": # plot a loaded result
            # exploratory mode
            if fterm is None:
                raise ValueError("!! Indicate fterm (focused term) !!")
            else:
                data = self.res.T[fterm]
                self.__plot.plot(data=data,keyword=keyword,focus=fterm,**kwargs)
        elif mode=="focused": # plot a loaded result
            # focused mode
            if fterm is None:
                raise ValueError("!! Indicate fterm (focused term) !!")
            else:
                self.__plot.plot(data=self.res,keyword=keyword,focus=fterm,**kwargs)
        else:
            raise ValueError("!! Wrong mode: 'exploratory' or 'focused' !!")
