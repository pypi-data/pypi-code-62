# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 13:05:34 2019

Converter

@author: tadahaya
"""

import pandas as pd
import numpy as np
from itertools import chain
from tqdm import trange
import pickle

class SynoDict():
    """
    Dict considering synonyms
    time consuming in dict preparation

    Parameters
    ----------
    reps: list
        representative keys for decoder
        
    synonyms: list
        a list of synonym sets [{},{},...]
        !! nan should be replaced with "" before construction !!
        
    values: list
        list of values

    """
    def __init__(self,keys=[],values=[],synonyms=[],processing=True):
        if processing:
            self.keys = list(map(lambda x: str(x).lower(),keys))
            self.values = list(map(lambda x: int(x),values))
            self.__dec = dict(zip(self.values,self.keys))
            ol = set()
            n = len(synonyms)
            for i in trange(n):
                rem = synonyms.copy()
                tar = rem.pop(i)
                rem = set(chain.from_iterable(rem))
                ol = ol | (tar - rem)
            temp = [v - ol for v in synonyms]
            new = []
            ap = new.append
            for v,w in zip(temp,self.keys):
                ap((set([w]) | set(list(map(lambda x: str(x).lower(),v)))) - set([""]))
            self.synonyms = new
        else:
            self.keys = keys
            self.values = values
            self.__dec = dict(zip(values,keys))
            self.synonyms = synonyms
        self.not_found = set()


    def enc(self,word):
        """ encoder """
        for v,w in zip(self.synonyms,self.values):
            if word in v:                
                return w
        raise KeyError(word)


    def fix(self,obj,substitute=""):
        """
        return fixed dict for converting the indicate list
        
        Parameters
        ----------
        obj: list
            a list of conversion target

        substitute: str
            a word employed for indicating not found keys        

        """
        value = self.enc_list(obj,substitute)
        return dict(zip(obj,value))


    def to_pickle(self,url):
        """ to save Synonym Dict """
        with open(url,"wb") as f:
            pickle.dump([self.keys,self.values,self.synonyms],f)


    def read_pickle(self,url):
        """ to load Synonym Dict """
        with open(url,"rb") as f:
            temp = pickle.load(f)
        self.keys = temp[0]
        self.values = temp[1]
        self.synonyms = temp[2]
        self.__dec = dict(zip(self.values,self.keys))
        self.not_found = set()


    def enc_list(self,target,substitute=""):
        """
        convert a list according to pre-defined dict

        Parameters
        ----------
        target: list

        substitute: str
            a word employed for indicating not found keys        
        
        """
        target = list(map(lambda x: x.lower(),target))
        res = []
        ap = res.append
        nf = []
        ap2 = nf.append
        for v in target:
            try:
                ap(self.enc(v))
            except KeyError:
                ap(substitute)
                ap2(v)
        self.not_found = set(nf)
        return res


    def dec_list(self,target,substitute=""):
        """ decoder for list """
        res = []
        ap = res.append
        nf = []
        ap2 = nf.append
        for v in target:
            try:
                ap(self.__dec[v])
            except KeyError:
                ap(substitute)
                ap2(v)
        self.not_found = set(nf)
        return res


    def enc_set(self,target):
        """
        convert a set according to pre-defined dict

        Parameters
        ----------
        target: set

        substitute: str
            a word employed for indicating not found keys        
        
        """
        target = list(map(lambda x: x.lower(),target))
        res = set()
        ad = res.add
        nf = set()
        ad2 = nf.add
        for v in target:
            try:
                ad(self.enc(v))
            except KeyError:
                ad2(v)
        self.not_found = nf
        return res


    def dec_set(self,target,substitute=""):
        """ decoder for set """
        res = set()
        ad = res.add
        nf = set()
        ad2 = nf.add
        for v in target:
            try:
                ad(self.__dec[v])
            except KeyError:
                ad2(v)
        self.not_found = nf
        return res


class FixedDict(SynoDict):
    """ handling conversion between names and IDs """
    def __init__(self,keys,values,synonyms,processing=False):
        super().__init__(keys,values,synonyms,processing)
        self.enc = dict(zip(self.keys,self.values))


    def enc_list(self,target,substitute=""):
        """
        convert a list according to pre-defined dict

        Parameters
        ----------
        target: list

        substitute: str
            a word employed for indicating not found keys        
        
        """
        target = list(map(lambda x: x.lower(),target))
        res = []
        ap = res.append
        nf = []
        for v in target:
            try:
                ap(self.enc[v])
            except KeyError:
                ap(substitute)
                nf.append(v)
        self.not_found = set(nf)
        return res


    def dec_list(self,target,substitute=""):
        """ decoder for list """
        res = []
        ap = res.append
        nf = []
        for v in target:
            try:
                ap(self.__dec[v])
            except KeyError:
                ap(substitute)
                nf.append(v)
        self.not_found = set(nf)
        return res


    def enc_set(self,target,substitute=""):
        """
        convert a set according to pre-defined dict

        Parameters
        ----------
        target: set

        substitute: str
            a word employed for indicating not found keys        
        
        """
        target = list(target)
        res = self.enc_list(target,substitute)
        return set(res)


    def dec_set(self,target,substitute=""):
        """ decoder for set """
        target = list(target)
        res = self.dec_list(target,substitute)
        return set(res)