# -*- coding: utf-8 -*-
"""
Created on Wed Dec 25 17:39:38 2024

@author: fleroux
"""

import numpy as np

from fanch.tools import get_tilt

def get_modulation_phase_screens(pupil, n_modulation_points, modulation_radius):
    
    modulation_phase_screens = np.empty((pupil.shape[0], pupil.shape[1], 
                                         n_modulation_points), dtype=float)
    
    tilt_amplitude = 2.*np.pi * modulation_radius
    
    theta_list = np.arange(0., 2.*np.pi, 2.*np.pi/n_modulation_points)
    
    for k in range(n_modulation_points):
        
        theta = theta_list[k]  
        tilt_theta = get_tilt((pupil.shape[0], pupil.shape[1]), theta)
        tilt_theta[pupil>0] = (tilt_theta[pupil>0] - tilt_theta[pupil>0].min())\
            /(tilt_theta[pupil>0].max()- tilt_theta[pupil>0].min())
        tilt_theta[pupil==0] = 0.
        modulation_phase_screens[:,:,k] = tilt_amplitude*tilt_theta
        
    return modulation_phase_screens