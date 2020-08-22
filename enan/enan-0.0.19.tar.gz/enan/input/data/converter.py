# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 13:05:34 2019

Converter class

Analyzer o-- InputControl o-- Data o-- Converter

@author: tadahaya
"""
import pandas as pd

__all__ = ["SeqConverter","SetConverter","SetTSConverter","VectorConverter"]

# delegation
class SeqConverter():
    def __init__(self):
        pass

    def name2id(self,seq,dic):
        """
        convert a list according to pre-defined dict
        not found keys are eliminated and returned as a set

        Parameters
        ----------
        seq: set or list
        dic: SynoDict or FixedDict

        """
        new = dic.enc_set(seq)
        not_found = dic.not_found
        return new,not_found


    def id2name(self,seq,dic):
        """
        convert a list according to pre-defined dict
        not found keys are eliminated and returned as a set

        Parameters
        ----------
        seq: set or list
        dic: SynoDict or FixedDict

        """
        new = dic.dec_set(seq)
        not_found = dic.not_found
        return new,not_found


class SetConverter():
    def __init__(self):
        pass

    def name2id(self,data,dic):
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


    def id2name(self,data,dic):
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
            temp = dic.enc_set(v,substitute="") - {""}
            nf = nf | dic.not_found
            ap(temp)                   
        return dict(zip(keys,new)),nf


class SetTSConverter():
    def __init__(self):
        pass

    def name2id(self,data,dic):
        """
        convert values of dict according to pre-defined dict
        not found keys are eliminated and returned as a set

        Parameters
        ----------
        data: a dict of {term:tuples of up/down tags}
        dic: SynoDict or FixedDict

        """
        values = list(data.values())
        keys = list(data.keys())
        new = []
        ap = new.append
        nf = set()
        for v in values:
            up = dic.enc_set(v[0]) - {""}
            nf = nf | dic.not_found
            dn = dic.enc_set(v[1]) - {""}
            nf = nf | dic.not_found
            ap((up,dn))
        return dict(zip(keys,new)),nf


    def id2name(self,data,dic):
        """
        convert values of dict according to pre-defined dict
        not found keys are eliminated and returned as a set

        Parameters
        ----------
        data: a dict of {term:tuples of up/down tags}
        dic: SynoDict or FixedDict

        """
        values = list(data.values())
        keys = list(data.keys())
        new = []
        ap = new.append
        nf = set()
        for v in values:
            up = dic.dec_set(v[0]) - {""}
            nf = nf | dic.not_found
            dn = dic.dec_set(v[1]) - {""}
            nf = nf | dic.not_found
            ap((up,dn))
        return dict(zip(keys,new)),nf


class VectorConverter():
    def __init__(self):
        pass

    def name2id(self,data,dic):
        """
        convert index of dataframe according to pre-defined dict
        not found keys are eliminated and returned as a set

        Parameters
        ----------
        data: dataframe
        dic: SynoDict or FixedDict

        """
        before = list(data.index)
        new = dic.enc_list(before,substitute="")
        df2 = data.copy()
        df2.index = new
        df2.drop([""],inplace=True)
        return df2,dic.not_found


    def id2name_vec(self,data,dic):
        """
        convert index of dataframe according to pre-defined dict
        not found keys are eliminated and returned as a set

        Parameters
        ----------
        data: dataframe
        dic: SynoDict or FixedDict

        """
        before = list(data.index)
        new = dic.dec_list(before,substitute="")
        df2 = data.copy()
        df2.index = new
        df2.drop([""],inplace=True)
        return df2,dic.not_found