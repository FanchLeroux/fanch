# -*- coding: utf-8 -*-
"""
Created on Wed Dec 25 17:40:44 2024

@author: fleroux
"""

import numpy as np

from fanch.tools import get_tilt

def get_4pywfs_phase_mask(shape, amplitude):
    
    mask = np.empty(shape, dtype=float)
    theta_list = [[np.pi/4, 3*np.pi/4], [7*np.pi/4, 5* np.pi/4]]
    
    for m in range(len(theta_list)):
        for n in range(len(theta_list[0])):
            tilt = get_tilt([0.5*shape[0], 0.5*shape[1]], theta=theta_list[m][n], amplitude = amplitude)
            mask[m*mask.shape[0]//2:(m+1)*mask.shape[0]//2, n*mask.shape[0]//2:(n+1)*mask.shape[0]//2] = tilt
            
    return mask