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

def close_the_loop(tel, ngs, atm, dm, wfs, reconstructor, loop_gain, n_iter, 
                   delay=1, seed=0, save_telemetry=False, save_psf=False):
    
    ngs*tel
    tel.computePSF()
    
    # Memory allocation
    
    total = np.zeros(n_iter)     # turbulence phase std [nm]
    residual = np.zeros(n_iter)  # residual phase std [nm]
    strehl = np.zeros(n_iter)    # Strehl Ratio
    
    if save_telemetry:
    
        dm_coefs = np.zeros([dm.nValidAct, n_iter])
        pupil_opd = np.zeros(list(tel.OPD.shape).append(n_iter))
        wfs_frames = np.zeros(list(pyramid.cam.frame.shape).append(n_iter))
        
    if save_psf:
        short_exposure_psf = np.zeros(list(tel.PSF.shape).append(n_iter))
    
    # initialization

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
            
        if save_psf:
            tel.computePSF()
            short_exposure_psf[:,:,k] = tel.PSF
    
    # return
    
    if save_telemetry and save_psf:
        return total, residual, strehl, dm_coefs, pupil_opd, wfs_frames, short_exposure_psf
    elif save_telemetry:
        return total, residual, strehl, dm_coefs, pupil_opd, wfs_frames
    elif save_psf:
        total, residual, strehl, short_exposure_psf
    else:
        return total, residual, strehl
    

def close_the_loop_delay(tel, ngs, atm, dm, wfs, reconstructor, loop_gain, n_iter, 
                   delay=1, seed=0, save_telemetry=False, save_psf=False):
    
    ngs*tel
    tel.computePSF()
    
    # Memory allocation
    
    total = np.zeros(n_iter)     # turbulence phase std [nm]
    residual = np.zeros(n_iter)  # residual phase std [nm]
    strehl = np.zeros(n_iter)    # Strehl Ratio
    
    if save_telemetry:
        dm_coefs = np.zeros([dm.nValidAct, n_iter])
        turbulence_phase_screens = np.zeros([tel.OPD.shape[0],tel.OPD.shape[1]]+[n_iter])
        wfs_frames = np.zeros([wfs.cam.frame.shape[0],wfs.cam.frame.shape[1]]+[n_iter])
        
    if save_psf:
        short_exposure_psf = np.zeros([tel.PSF.shape[0],tel.PSF.shape[1]] + [n_iter])
    
    # initialization
    
    pupil_opd = np.zeros([tel.OPD.shape[0],tel.OPD.shape[1]] + [delay])
    atm.initializeAtmosphere(tel)
    atm.generateNewPhaseScreen(seed = seed)
    tel+atm
    
    if save_telemetry:
        turbulence_phase_screens[:,:,0] = tel.OPD
    
    for n in range(1, delay):
        pupil_opd[:,:,n] = tel.OPD
        atm.update() # pupil_opd[:,:,delay] is the more recent turbulent phase screen

    dm.coefs = 0
    wfs_measure = 0*wfs.signal
    ngs*tel*dm*wfs
    
    # close the loop
    
    for k in range(n_iter):
        
        # get total turbulence std
        atm.update() # this should reset tel.OPD
        
        if save_telemetry:
            turbulence_phase_screens[:,:,0] = tel.OPD
        
        total[k] = np.std(tel.OPD[np.where(tel.pupil==1)])*1e9 # after atm.update(), tel.OPD = turbulent phase screen.
        
        # save current turbulent phase sreen to be corrected after the delay
        np.roll(pupil_opd, -1, axis=0)
        pupil_opd[:,:,-1] = tel.OPD
        
        tel*dm
        
        residual[k]=np.std(tel.OPD[np.where(tel.pupil==1)])*1e9 # [nm]
        strehl[k] = np.exp(-np.var(tel.src.phase[np.where(tel.pupil==1)]))
        
        tel.OPD = pupil_opd[:,:,0] # measuring the oldest OPD available
        tel*dm*wfs
        wfs_measure = wfs.signal
        
        # update dm coeficients
        dm.coefs = dm.coefs - loop_gain * np.matmul(reconstructor, wfs_measure)
                
        if save_telemetry:
            
            dm_coefs[:,k] = dm.coefs
            wfs_frames[:,:,k] = wfs.cam.frame
            
        if save_psf:
            tel.computePSF()
            short_exposure_psf[:,:,k] = tel.PSF
    
    # return
    
    if save_telemetry and save_psf:
        return total, residual, strehl, dm_coefs, pupil_opd, wfs_frames, short_exposure_psf
    elif save_telemetry:
        return total, residual, strehl, dm_coefs, pupil_opd, wfs_frames
    elif save_psf:
        total, residual, strehl, short_exposure_psf
    else:
        return total, residual, strehl
    
def compute_mmse_reconstructor(calibratrion, modal_basis_covariance, noise_level, other_level):
    
    return 1