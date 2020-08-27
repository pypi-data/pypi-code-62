# -*- coding: utf-8 -*-
"""
Created on Fri May  8 00:12:49 2020

@author: msmsa
"""
import PFAS_SAT as ps


def check_processmodel(process_model_cls):
    model = process_model_cls()
    model.calc()
    model.report()
    model.report(normalized=True)
    model.setup_MC()
    model.MC_Next()
    model.calc()
    model.report()


def test_LandApp():
    check_processmodel(ps.LandApp)


def test_Comp():
    check_processmodel(ps.Comp)


def test_Landfill():
    check_processmodel(ps.Landfill)


def test_WWT():
    check_processmodel(ps.WWT)


def test_Stab():
    check_processmodel(ps.Stab)


def test_AdvWWT():
    check_processmodel(ps.AdvWWT)


def test_SCWO():
    check_processmodel(ps.SCWO)


def test_ThermalTreatment():
    check_processmodel(ps.ThermalTreatment)


def test_AD():
    check_processmodel(ps.AD)
