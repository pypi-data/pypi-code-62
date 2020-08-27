# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 18:18:05 2020

@author: msmsa
"""
import pandas as pd
from .Flow import Flow
from .SubProcesses import mix, stabilization
from .StabInput import StabInput
from .ProcessModel import ProcessModel


class Stab(ProcessModel):
    """
    Assumptions:
        1. No volatilization or degradation of PFAS.
        2. Steady state.
        3. Soil and amendments are well mixed.
        4. Annual time horizon.
    """
    ProductsType = []

    def __init__(self, input_data_path=None, CommonDataObjct=None, InventoryObject=None):
        super().__init__(CommonDataObjct, InventoryObject)
        self.InputData = StabInput(input_data_path)

    def calc(self, Inc_flow=None):
        # Initialize the Incoming flow
        if Inc_flow:
            self.Inc_flow = Inc_flow
        else:
            self.Inc_flow = Flow()
            kwargs = {}
            for key, data in self.InputData.IncProp.items():
                kwargs[key] = data['amount']
            kwargs['PFAS_cont'] = {}
            for key, data in self.InputData.IncPFAS.items():
                kwargs['PFAS_cont'][key] = data['amount']
            self.Inc_flow.set_flow(**kwargs)

        # Calculating the mass of additive mixed with the Incoming flow
        additive_mass_mix = self.InputData.Stabil['add_mass_ratio']['amount'] * self.Inc_flow.mass

        # Initializing the additive flow
        self.Add_flow = Flow()
        kwargs = {}
        for key, data in self.InputData.AddProp.items():
            kwargs[key] = data['amount']
        kwargs['mass_flow'] = additive_mass_mix

        kwargs['C_cont'] = 0

        self.Add_flow.set_flow(**kwargs)

        # Mixing the Incoming flow with additive
        self.Mixed_flow = mix(self.Inc_flow, self.Add_flow)

        # Calculating the volume of percipitation (includes RunOff and Leachate)
        Percip_Vol = self.Inc_flow.mass / self.Inc_flow.bulk_dens / self.InputData.Stabil['depth_mix']['amount'] *\
            self.InputData.Percip['ann_precip']['amount'] * 1000  # L/yr
        Leachate_Vol = Percip_Vol * self.InputData.Percip['frac_leach']['amount']  # L/yr
        RunOff_Vol = Percip_Vol * self.InputData.Percip['frac_runoff']['amount']  # L/yr

        # Calculating the PFAS in water and soil partitions
        self.Stabilized, self.Leachate, self.RunOff = stabilization(self.Mixed_flow, self.InputData.SoilLogPartCoef,
                                                                    self.InputData.AddProp['add_liqsol_part_coef']['amount'],
                                                                    additive_mass_mix, Leachate_Vol, RunOff_Vol)

        # add to Inventory
        self.Inventory.add('Leachate', 'Stab', 'Water', self.Leachate)
        self.Inventory.add('RunOff', 'Stab', 'Water', self.RunOff)
        self.Inventory.add('Stabilized', 'Stab', 'Soil', self.Stabilized)

    def products(self):
        Products = {}
        return(Products)

    def setup_MC(self, seed=None):
        self.InputData.setup_MC(seed)

    def MC_Next(self):
        input_list = self.InputData.gen_MC()
        return(input_list)

    def report(self, normalized=False):
        report = pd.DataFrame(index=self.Inc_flow._PFAS_Index)
        if not normalized:
            report['Remaining'] = self.Stabilized.PFAS
            report['Leachate'] = self.Leachate.PFAS
            report['RunOff'] = self.RunOff.PFAS
        else:
            report['Remaining'] = self.Stabilized.PFAS / self.Inc_flow.PFAS
            report['Leachate'] = self.Leachate.PFAS / self.Inc_flow.PFAS
            report['RunOff'] = self.RunOff.PFAS / self.Inc_flow.PFAS
        return(report)
