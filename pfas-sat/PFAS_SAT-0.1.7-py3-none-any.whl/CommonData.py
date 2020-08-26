# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 18:27:22 2020

@author: Mojtaba Sardarmehni
"""
from .InputData import InputData
from pathlib import Path


class CommonData(InputData):
    # waste Materials
    WasteMaterials = ['CompFeed', 'ComRes', 'CompFin', 'Digestate',
                      'MSW', 'C&DWaste', 'MedWaste', 'MRFRes', 'CombRes',
                      'ContamSoil',
                      'ContactWater', 'LF_Leachate',
                      'DewWWTSol', 'DryWWTSol', 'WWTSol',
                      'SCWO_Steam', 'SCWO_Slurry',
                      'SpentGAC', 'ROConc']

    def __init__(self, input_data_path=None):
        if input_data_path:
            self.input_data_path = input_data_path
        else:
            self.input_data_path = Path(__file__).parent/'Data/CommonData.csv'

        # Initialize the superclass
        super().__init__(self.input_data_path)
