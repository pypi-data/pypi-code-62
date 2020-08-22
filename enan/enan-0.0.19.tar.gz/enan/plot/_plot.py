# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 13:05:34 2019

module for plot

@author: tadahaya

"""

import pandas as pd
import numpy as np
from scipy.stats import rankdata
import matplotlib.pyplot as plt
import seaborn as sns
import csv
from pathlib import Path

# abstract class
class Plot():
    def __init__(self):
        pass

    def plot(self):
        raise NotImplementedError        


# concrete class
class PlotFET(Plot):
    def plot(self,res,focus=5,fileout="",dpi=100,thresh=0.05,xlabel="-logP",ylabel="",title="",
                        color="royalblue",alpha=0.5,height=0.8,fontsize=12,textsize=12,figsize=()):
        """
        visualize a result of enrichment analysis

        Parameters
        ----------
        res: dataframe
            a result file of enrichment analysis
            
        """
        if len(res) < focus:
            focus = len(res)
        res = res.sort_values(by="p value")
        res = res.iloc[:focus,:]
        res2 = res[res["adjusted p value"] < thresh]
        val = -np.log10(res["adjusted p value"])
        val = [v for v in val[::-1]]
        val2 = -np.log10(res2["adjusted p value"])
        val2 = val2.tolist() + [np.nan]*(len(res) - len(res2))
        val2 = [v for v in val2[::-1]]
        name = list(res.index)
        name = [v.replace("_"," ") for v in name[::-1]]
        X = list(range(focus))
        if len(figsize) > 0:
            fig = plt.figure(figsize=figsize)
        else:
            fig = plt.figure()
        ax = fig.add_subplot(111)
        if len(xlabel) > 0:
            ax.set_xlabel(xlabel,fontsize=fontsize)
        if len(ylabel) > 0:
            ax.set_ylabel(ylabel,fontsize=fontsize)
        if len(title) > 0:
            ax.set_title(title,fontsize=fontsize)
        ax.tick_params(labelsize=fontsize)
        ax.set_yticks([])
        ax.spines["right"].set_color("none")
        ax.spines["bottom"].set_color("none")
        ax.spines["top"].set_color("none")
        ax.barh(X,val,color="lightgrey",alpha=alpha,height=height)
        ax.barh(X,val2,color=color,height=height,alpha=alpha)
        for v,w in zip(name,X):
            ax.text(0.02,w,v,ha="left",va="center",fontsize=textsize)
        if len(fileout) > 0:
            plt.savefig(fileout,bbox_inches="tight",dpi=dpi)
        plt.tight_layout()
        plt.show()


# concrete class
class PlotGSEA(Plot):
    def plot(self,data,highlight=[],color="goldenrod",label="",ylabel="",
             title="",fileout="",dpi=100,fontsize=14,size=40,figsize=()):
        """
        visualize a result of enrichment analysis
        
        Parameters
        ----------
        es: 2d array
            enrichment scores of each location (feature x tag/sample)
        focus: int
            indicate the No. of the column of interest
            
        """
        data = data.sort_values(ascending=False)
        idx = list(data.index)
        x = np.arange(1,len(data) + 1,1)
        y_f = data.loc[highlight]
        x_f = [idx.index(v) + 1 for v in list(y_f.index)]
        if figsize!=():
            g = plt.figure(figsize=figsize)
        else:
            g = plt.figure()
        ax = g.add_subplot(1,1,1)
        if len(title) > 0:
            ax.set_title(title,fontsize=fontsize)
        ax.scatter(x,data.values,color="lightgrey",s=size)
        ax.scatter(x_f,y_f,color=color,label=label,s=size)
        ax.set_ylabel(ylabel,fontsize=fontsize)
        if len(label) > 0:
            ax.legend(loc="best",fontsize=fontsize)
        if len(fileout) > 0:
            plt.savefig(fileout,bbox_inches="tight",dpi=dpi)
        ax.tick_params(labelsize=fontsize)
        plt.tight_layout()
        plt.show()


    def plot_running(self,es,focus=None,fileout="",dpi=100,xlabel="",ylabel="",title="",
                        color="navy",fontsize=12,figsize=()):
        """
        visualize a result of enrichment analysis
        
        Parameters
        ----------
        es: 2d array
            enrichment scores of each location (feature x tag/sample)
        focus: int
            indicate the No. of the column of interest
            
        """
        y = es.T[focus]
        x = np.arange(1,len(y) + 1,1)
        xmin = np.min(x)
        xmax = np.max(x)
        if figsize!=():
            fig = plt.figure(figsize=figsize)
        else:
            fig = plt.figure()
        ax = plt.subplot(1,1,1)
        if len(xlabel) > 0:
            ax.set_xlabel(xlabel,fontsize=fontsize)
        else:
            ax.set_xlabel("rank in ordered gene list",fontsize=fontsize)
        if len(ylabel) > 0:
            ax.set_ylabel(ylabel,fontsize=fontsize)
        else:
            ax.set_ylabel("enrichment score",fontsize=fontsize)
        if len(title) > 0:
            ax.set_title(title,fontsize=fontsize)
        else:
            ax.set_title(focus,fontsize=fontsize)
        ax.tick_params(labelsize=fontsize)
        ax.plot(x,y,color=color)
        ax.hlines([0],xmin,xmax,"grey",linestyles='dashed')
        ax.set_xlim(xmin,xmax)
        if len(fileout) > 0:
            plt.savefig(fileout,bbox_inches="tight",dpi=dpi)
        plt.tight_layout()
        plt.show()


# concrete class
class PlotSsGSEA(Plot):
    def plot(self,data,keyword=[],focus=None,order=[],fileout="",dpi=100,xlabel="",
             ylabel="",title="",color="goldenrod",
             palette=["lightyellow","mediumseagreen"],size=8,fontsize=12,figsize=()):
        """
        visualize a result of enrichment analysis
        
        Parameters
        ----------
        es: 2d array
            enrichment scores of each location (feature x tag/sample)
            
        focus: int
            indicate the No. of the column of interest
            
        """
        data = self._preprocess(data,keyword)
        if len(order)==0:
            order = keyword
        if figsize!=():
            fig = plt.figure(figsize=figsize)
        else:
            fig = plt.figure()
        ax = plt.subplot(1,1,1)
        sns.set(style="ticks",palette="pastel")
        if data.shape[0] < 30:
            sns.boxplot(x="indicator",y="value",palette=palette,data=data,order=order,
                        meanline=True,showmeans=True,
                        boxprops={"facecolor":"whitesmoke","color":"whitesmoke"},
                        meanprops={"color":"grey","linestyle":"solid"},
                        medianprops={"color":"whitesmoke"},
                        whiskerprops={"color":"whitesmoke"},
                        capprops={"color":"whitesmoke"},
                        flierprops={"markeredgecolor":"whitesmoke"})
            sns.swarmplot(x="indicator",y="value",color=color,data=data,
                          size=size,order=order)
        else:
            sns.boxplot(x="indicator",y="value",palette=palette,
                        data=data,order=order)
        sns.despine(offset=10,trim=True)
        if len(xlabel) > 0:
            ax.set_xlabel(xlabel,fontsize=fontsize)
        else:
            ax.set_xlabel("")
        if len(ylabel) > 0:
            ax.set_ylabel(ylabel,fontsize=fontsize)
        else:
            ax.set_ylabel("enrichment score",fontsize=fontsize)
        if len(title) > 0:
            ax.set_title(title,fontsize=fontsize)
        ax.tick_params(labelsize=fontsize)
        if len(fileout) > 0:
            plt.savefig(fileout,bbox_inches="tight",dpi=dpi)
        plt.tight_layout()
        plt.show()

    
    def _preprocess(self,data0,keyword=[]):
        """ preprocessing for ssGSEA plots """
        data = data0.copy()
        data = pd.DataFrame(data)
        data.columns = ["value"]
        sample_name = list(data.index)
        if len(keyword)==0:
            raise ValueError("ERROR: give keywords!!")
        elif len(keyword)==1:
            col_ind = ["control" if keyword[0] not in v else keyword[0] for v in sample_name]
        else:
            col_ind = []
            ap = col_ind.append
            for v in sample_name:
                flag = 0
                for w in keyword:
                    if w in v:
                        ap(w)
                        flag += 1
                        break
                if flag==0:
                    ap("notfound")
        data["indicator"] = col_ind
        data = data[data["indicator"]!="notfound"]
        return data