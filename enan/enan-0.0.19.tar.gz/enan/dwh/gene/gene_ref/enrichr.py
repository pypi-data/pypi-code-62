# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 13:05:34 2019

Data warehouse control class

Analyzer o-- DWHControl <|.. GeneControl <|.. Enrichr

@author: tadahaya
"""
import pandas as pd
import numpy as np
import os
import csv

from ...._utils.converter import SynoDict
from ...._utils import loader as ld
from ...dwh_control import StoredRef

class Enrichr(StoredRef):
    """
    Reference gene set data from Enrichr by Ma'ayan Laboratory
    https://amp.pharm.mssm.edu/Enrichr/
    
    """
    def __init__(self):
        self.ref = dict()
        self.__base = os.path.dirname(__file__) # ~\enapy\dwh\gene\gene_ref
        self.__base_en = self.__base + "\\enrichr"
        self.__library = ""
        self.__species = ""
        self.__dic = SynoDict()
        self.__state = {"database":"enrichr","name":""}
        h_ready,h_not = self.__discriminate(self.__base_en + "\\human")
        m_ready,m_not = self.__discriminate(self.__base_en + "\\mouse")
        self.__available = {"human":h_ready,"mouse":m_ready}
        self.__not = {"human":h_not,"mouse":m_not}
        print("Reference library: Enrichr")
        print("--- all libraries currently available ---")
        print("<< ready-to-use >>")
        print("- human")
        for l in h_ready:
            print(l)
        print("- mouse")
        for l in m_ready:
            print(l)
        print("<< need to be processed >>")
        print("- human")
        for l in h_not:
            print(l)
        print("- mouse")
        for l in m_not:
            print(l)
        print("-----------------------------------------")


    def get_(self):
        return self.ref

    def get_species(self):
        return self.__species

    def load_(self,library="GO_Biological_Process_2018"):
        """
        load a data set from Enrichr library
        
        Parameters
        ----------
        library: str
            indicate the name of library of interest
                    
        """
        print("library='{}'".format(library))
        self.__library = library
        if library in self.__available["human"]:
            url = self.__base_en + "\\human\\{}.pkl".format(library)
            self.ref = ld.read_pickle(url)
            self.__species = "human"
            self.__state["name"] = self.__library
        elif library in self.__available["mouse"]:
            url = self.__base_en + "\\mouse\\{}.pkl".format(library)
            self.ref = ld.read_pickle(url)
            self.__species = "mouse"
            self.__state["name"] = self.__library
        elif library in self.__not["human"]:
            self.__species = "human"
            raise ValueError("prepare reference...")
        elif library in self.__not["mouse"]:
            self.__species = "mouse"
            raise ValueError("prepare reference...")
        else:
            raise ValueError("!! no indicated file. check enrichr directory !!")


    def prep_(self,library="",species="",dic=None):
        """
        prepare a reference data set by converting txt
        
        Parameters
        ----------
        library: str
            indicate the name of library of interest

        dic: SynoDict
            SynoDict object for conversion        
        
        """
        if len(species) > 0:
            self.__species = species
        else:
            raise ValueError("!! No species: indicate species !!")
        print("--- take a long time ---")
        if len(library) > 0:
            self.__library = library
        url = self.__base + "\\enrichr\\{0}\\{1}.txt".format(self.__species,self.__library)
        with open(url,encoding="utf_8") as f:
            reader = csv.reader(f,delimiter='\t')
            data = [row for row in reader]
        terms = []
        ap = terms.append
        members = []
        ap2 = members.append
        for v in data:
            ap(v[0])
            del v[:2]
            temp = set(v) - {""}
            ap2(temp)
        if dic is None:
            p_biomart = self.__base.replace("\\gene_ref","\\gene_dict") + "\\biomart"
            if self.__species=="human":
                self.__dic.read_pickle(p_biomart + "\\mart_export_HGNC.pkl") # hard coding
            elif self.__species=="mouse":
                self.__dic.read_pickle(p_biomart + "\\mart_export_MGI.pkl") # hard coding
            else:
                raise KeyError("!! check species or biomart directory !!")
        else:
            self.__dic = dic
        res = self.__name2id(dict(zip(terms,members)),self.__dic)[0]
        ld.to_pickle(res,url.replace("txt","pkl"))
        self.ref = res
        self.__state["name"] = self.__library
        print(">> completed")


    def __discriminate(self,url):
        """ get filenames """
        n_all = os.listdir(url)
        n_txt = [v.replace(".txt","") for v in n_all if ".txt" in v]
        n_pkl = [v.replace(".pkl","") for v in n_all if ".pkl" in v]
        subtract = [v for v in n_txt if v not in n_pkl]
        return n_pkl,subtract


    def __name2id(self,data,dic):
        """
        convert values of dict according to pre-defined dict
        not found keys are eliminated and returned as a set

        Parameters
        ----------
        data: a dict of {term:sets of group}
        dic: SynoDict or FixedDict

        """
        values = list(data.values())
        keys = list(data.keys())
        new = []
        ap = new.append
        nf = set()
        for v in values:
            temp = dic.enc_set(v) - {""}
            nf = nf | dic.not_found
            ap(temp)                   
        return dict(zip(keys,new)),nf


    def get_state(self):
        return self.__state