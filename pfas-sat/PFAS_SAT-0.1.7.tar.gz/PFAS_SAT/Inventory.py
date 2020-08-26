# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 22:09:10 2020

@author: msmsa
"""
import pandas as pd


class Inventory:
    def __init__(self):
        self._PFAS_Index = ['PFAS', 'PFOA', 'PFNA', 'PFDA', 'PFUnA', 'PFOS', 'PFDS', 'N_MeFOSAA', 'N_EtFOSAA']
        self._index = ['Flow_name', 'Source', 'Target', 'Unit'] + self._PFAS_Index
        self.Inv = pd.DataFrame(index=self._index)
        self.Col_index = 0

    def add(self, Flow_name, Source, Target, flow):
        data = [Flow_name, Source, Target, 'μg/year'] + list(flow.PFAS.values)
        self.Inv[self.Col_index] = data
        self.Col_index += 1

    def report_Water(self):
        water_inv = self.Inv[self.Inv.columns[self.Inv.loc['Target'] == 'Water']]
        return(water_inv)

    def report_Soil(self):
        soil_inv = self.Inv[self.Inv.columns[self.Inv.loc['Target'] == 'Soil']]
        return(soil_inv)

    def report_Air(self):
        air_inv = self.Inv[self.Inv.columns[self.Inv.loc['Target'] == 'Air']]
        return(air_inv)

    def clear(self):
        self.Inv = pd.DataFrame(index=self._index)
        self.Col_index = 0

    def report(self):
        report = dict()
        report['Water (μg/year)'] = self.report_Water().loc[self._PFAS_Index].sum(axis=1).sum()
        report['Soil (μg/year)'] = self.report_Soil().loc[self._PFAS_Index].sum(axis=1).sum()
        report['Air (μg/year)'] = self.report_Air().loc[self._PFAS_Index].sum(axis=1).sum()
        return(report)
