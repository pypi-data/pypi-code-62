# -*- coding: utf-8 -*-
"""
Created on Fri Jul 31 20:48:42 2020

@author: msmsa
"""
ProcessModelsMeta = {}

ProcessModelsMeta['LandApp'] = {}
ProcessModelsMeta['LandApp']['Name'] = 'Land Application'
ProcessModelsMeta['LandApp']['File'] = 'LandApp.py'
ProcessModelsMeta['LandApp']['InputType'] = ['CompFin', 'Digestate', 'DryWWTSol']

ProcessModelsMeta['Comp'] = {}
ProcessModelsMeta['Comp']['Name'] = 'Composting'
ProcessModelsMeta['Comp']['File'] = 'Comp.py'
ProcessModelsMeta['Comp']['InputType'] = ['CompFeed', 'DewWWTSol']

ProcessModelsMeta['AD'] = {}
ProcessModelsMeta['AD']['Name'] = 'AD'
ProcessModelsMeta['AD']['File'] = 'AD.py'
ProcessModelsMeta['AD']['InputType'] = ['CompFeed']

ProcessModelsMeta['Landfill'] = {}
ProcessModelsMeta['Landfill']['Name'] = 'Landfill'
ProcessModelsMeta['Landfill']['File'] = 'Landfill.py'
ProcessModelsMeta['Landfill']['InputType'] = ['MSW', 'CompFeed', 'CompFin', 'SpentGAC',
                                              'CombRes', 'DewWWTSol', 'WWTSol']

ProcessModelsMeta['ThermalTreatment'] = {}
ProcessModelsMeta['ThermalTreatment']['Name'] = 'ThermalTreatment'
ProcessModelsMeta['ThermalTreatment']['File'] = 'ThermalTreatment.py'
ProcessModelsMeta['ThermalTreatment']['InputType'] = ['MSW', 'CompFeed', 'SpentGAC',
                                                      'DryWWTSol']

ProcessModelsMeta['WWT'] = {}
ProcessModelsMeta['WWT']['Name'] = 'WWT'
ProcessModelsMeta['WWT']['File'] = 'WWT.py'
ProcessModelsMeta['WWT']['InputType'] = ['ContactWater', 'LFLeachate', 'ContaminatedWater']

ProcessModelsMeta['SCWO'] = {}
ProcessModelsMeta['SCWO']['Name'] = 'SCWO'
ProcessModelsMeta['SCWO']['File'] = 'SCWO.py'
ProcessModelsMeta['SCWO']['InputType'] = ['ContactWater', 'LFLeachate', 'ContaminatedWater']

ProcessModelsMeta['AdvWWT'] = {}
ProcessModelsMeta['AdvWWT']['Name'] = 'AdvWWT'
ProcessModelsMeta['AdvWWT']['File'] = 'AdvWWT.py'
ProcessModelsMeta['AdvWWT']['InputType'] = ['ContactWater', 'LFLeachate', 'ContaminatedWater']

ProcessModelsMeta['Stab'] = {}
ProcessModelsMeta['Stab']['Name'] = 'Stabilization'
ProcessModelsMeta['Stab']['File'] = 'Stab.py'
ProcessModelsMeta['Stab']['InputType'] = ['DewWWTSol', 'ContaminatedSoil']
