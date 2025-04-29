# -*- coding: utf-8 -*-
"""
Created on Tue Apr 29 14:31:54 2025

@author: fleroux
"""

def clean_wfs(wfs):
    
    if wfs.modulation == 0.:
    
        del wfs.maps
        del wfs.phaseBuffModulation
        del wfs.phaseBuffModulationLowres
        del wfs.phaseBuffModulationLowres_CPU
    
    return wfs