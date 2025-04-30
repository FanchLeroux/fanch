# -*- coding: utf-8 -*-
"""
Created on Tue Apr 29 14:31:54 2025

@author: fleroux
"""

import numpy as np


def clean_wfs(wfs):
    
    if wfs.modulation == 0.:
    
        del wfs.maps
        del wfs.phaseBuffModulation
        del wfs.phaseBuffModulationLowres
        del wfs.phaseBuffModulationLowres_CPU
    
    return wfs

def close_the_loop(tel, ngs, atm, dm, wfs, reconstructor, loop_gain, n_iter, delay=1, seed=0, save_telemetry=False):
    
    # Memory allocation
    
    total = np.zeros(n_iter)     # turbulence phase std [nm]
    residual = np.zeros(n_iter)  # residual phase std [nm]
    strehl = np.zeros(n_iter)    # Strehl Ratio
    
    if save_telemetry:
    
        dm_coefs = np.zeros([dm.nValidAct, n_iter])
        pupil_opd = np.zeros(list(tel.OPD.shape).append(n_iter))
        wfs_frames = np.zeros(list(pyramid.cam.frame.shape).append(n_iter))
    
    # initialization
    
    ngs*tel
    tel.computePSF()

    atm.initializeAtmosphere(tel)
    atm.generateNewPhaseScreen(seed = seed)
    tel+atm

    dm.coefs = 0
    wfs_measure = 0*wfs.signal

    ngs*tel*dm*wfs
    
    # close the loop
    
    for k in range(n_iter):
        
        atm.update()
        phase_turb = tel.src.phase
        
        tel*dm*wfs
        
        wfs_measure = wfs.signal # tune delay (1 frames here)
        
        dm.coefs = dm.coefs - loop_gain * np.matmul(reconstructor, wfs_measure)
        
        # wfs_measure = wfs.signal # tune delay (2 frames here)
                
        total[k] = np.std(tel.OPD[np.where(tel.pupil==1)])*1e9 # [nm]
        residual[k]=np.std(tel.OPD[np.where(tel.pupil>0)])*1e9 # [nm]
        strehl[k] = np.exp(-np.var(tel.src.phase[np.where(tel.pupil==1)]))
        
        if save_telemetry:
            
            dm_coefs[:,k] = dm.coefs
            pupil_opd[:,:,k] = tel.OPD
            wfs_frames[:,:,k] = pyramid.cam.frame
    
    if save_telemetry:
        return total, residual, strehl, dm_coefs, pupil_opd, wfs_frames
    
    else:
        return total, residual, strehl
    