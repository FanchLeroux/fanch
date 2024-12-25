# -*- coding: utf-8 -*-
"""
Created on Wed Dec 25 17:37:19 2024

@author: fleroux
"""

import numpy as np

def get_focal_plane_image(complex_amplitude):
    return np.abs(np.fft.fftshift(np.fft.fft2(complex_amplitude)))**2

def get_ffwfs_frame(complex_amplitude, mask_complex_amplitude):
    focal_plane_complex_amplitude = np.fft.fftshift(np.fft.fft2(complex_amplitude))\
        *mask_complex_amplitude
    return np.abs(np.fft.fft2(np.fft.ifftshift(focal_plane_complex_amplitude)))**2