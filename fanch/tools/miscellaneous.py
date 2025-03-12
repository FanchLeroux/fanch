# -*- coding: utf-8 -*-
"""
Created on Tue Dec 24 10:20:26 2024

@author: fleroux
"""

import matplotlib.pyplot as plt
import numpy as np

def warning(string):
    print('\033[1;36m'+'Fanch Warning: \n' + string + '\033[0m')

def get_circular_pupil(npx):
    D = npx + 1
    x = np.linspace(-npx/2,npx/2,npx)
    xx,yy = np.meshgrid(x,x)
    circle = xx**2+yy**2
    pupil  = circle<(D/2)**2
    
    return pupil

def zeros_padding(array, zeros_padding_factor):
    array = np.pad(array, (((zeros_padding_factor-1)*array.shape[0]//2, 
                                     (zeros_padding_factor-1)*array.shape[0]//2),
                                    ((zeros_padding_factor-1)*array.shape[1]//2, 
                                     (zeros_padding_factor-1)*array.shape[1]//2)))
    return array

def get_tilt(shape, theta=0., amplitude=1.):
    [X,Y] = np.meshgrid(np.arange(0, shape[0]), np.arange(0, shape[1]))
    tilt_theta = np.cos(theta) * X + np.sin(theta) * Y
    Y = np.flip(Y, axis=0) # change orientation
    tilt_theta = (tilt_theta - tilt_theta.min())/(tilt_theta.max()- tilt_theta.min())
    
    return amplitude*tilt_theta