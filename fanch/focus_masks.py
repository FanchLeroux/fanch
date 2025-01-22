# -*- coding: utf-8 -*-
"""
Created on Wed Dec 25 17:40:44 2024

@author: fleroux
"""

import numpy as np
import matplotlib.pyplot as plt

from copy import deepcopy

from fanch.tools import get_tilt, zeros_padding, get_circular_pupil

from fanch.propagation import get_ffwfs_frame, get_focal_plane_image

#%%

def get_4pywfs_phase_mask(shape, amplitude):
    
    mask = np.empty(shape, dtype=float)
    theta_list = [[np.pi/4, 3*np.pi/4], [7*np.pi/4, 5* np.pi/4]]
    
    for m in range(len(theta_list)):
        for n in range(len(theta_list[0])):
            tilt = get_tilt([0.5*shape[0], 0.5*shape[1]], theta=theta_list[m][n], 
                            amplitude = amplitude)
            mask[m*mask.shape[0]//2:(m+1)*mask.shape[0]//2,\
                 n*mask.shape[0]//2:(n+1)*mask.shape[0]//2] = tilt
            
    return mask

def get_amplitude_bioedge_masks(n_px):
    
    mask1 = np.ones((n_px, n_px))
    mask2 = deepcopy(mask1)
    mask3 = deepcopy(mask1)
    mask4 = deepcopy(mask1)
    
    mask1[n_px//2:,:] = 0
    mask2[:n_px//2,:] = 0
    mask3[:,n_px//2:] = 0
    mask4[:,:n_px//2] = 0
    
    return [mask1, mask2, mask3, mask4]

def pyramid_mask(nx, nFaces, angle=0.35, theta_ref=0):
    """
    Build the pyramid mask
    
    Parameters
    ----------
    nx : number of pixels.
    nFaces : number of faces for the pyramidal mask.
    angle : angle of the pyramid  #TODO: definition? which unit?
    theta_ref : rotation angle of the pyramid faces.
    """
    xx,yy = np.mgrid[0:nx,0:nx] - nx//2
    theta = np.mod(np.arctan2(xx,yy)+np.pi-theta_ref,2*np.pi)
    theta_face = 2*np.pi/nFaces
    msk = np.zeros((nx,nx), dtype=complex)

    for k in range(0,nFaces):
        # Tesselation
        theta_inf = k*theta_face<=theta
        theta_sup = theta<(k+1)*theta_face
        m = theta_inf * theta_sup
        # Tip-Tilt 
        theta_direction = (k+0.5)*theta_face
        c_tip = np.sin(theta_direction+theta_ref)
        c_tilt = np.cos(theta_direction+theta_ref)
        # Complex mask on each face
        msk += m*np.exp(2j*np.pi*angle*(c_tip*xx+c_tilt*yy))
        
    return msk

def eight_faces_four_pupils_pyramid_mask(npx, amplitude=False):
    
    if not amplitude:
        amplitude = 2*np.pi*2**0.5 * npx//2
    
    xx,yy = np.asarray(np.mgrid[0:npx,0:npx] - npx//2, dtype=float)
    xx+=0.5
    yy+=0.5
    theta = np.mod(np.arctan2(xx,yy)+np.pi,2*np.pi)
    theta_face = 2*np.pi/8
    
    masks = np.zeros((npx,npx,8), dtype=float)
    mask = np.zeros((npx,npx), dtype = float)
    
    for k in range(8):
        theta_inf = k*theta_face<=theta
        theta_sup = theta<(k+1)*theta_face
        masks[:,:,k] = theta_inf * theta_sup
        
    for k in range(npx//2):
        masks[k,npx-k-1,2] = 1
        masks[k,npx-k-1,3] = 0
        masks[k+npx//2,k+npx//2,4] = 0
        masks[k+npx//2,k+npx//2,5] = 1
        masks[k+npx//2,npx//2-k-1,6] = 1
        masks[k+npx//2,npx//2-k-1,7] = 0
        
    q1 = get_tilt((npx,npx), theta=np.pi/4, amplitude = amplitude)
    q2 = get_tilt((npx,npx), theta=3*np.pi/4, amplitude = amplitude)
    q3 = get_tilt((npx,npx), theta=5*np.pi/4, amplitude = amplitude)
    q4 = get_tilt((npx,npx), theta=7*np.pi/4, amplitude = amplitude)

    quadrants = [q1,q2,q3,q4]
    
    for k in range(masks.shape[2]):
        mask += masks[:,:,k]*quadrants[np.mod(k,2)+(k>3)*2]

    return mask

#%% 
npx = 32
zeros_padding_factor = 3

pupil = get_circular_pupil(npx)

#% --------------------- PHASOR ------------------

pupil_pad = zeros_padding(pupil, zeros_padding_factor)

phasor = get_tilt(pupil.shape, theta=1.25*np.pi) * pupil
phasor[pupil!=0] = (phasor[pupil!=0] - phasor[pupil!=0].min())\
                   /(phasor[pupil!=0].max()-phasor[pupil!=0].min()) # normalization
phasor = 1/zeros_padding_factor * 2**0.5 * np.pi * phasor

pupil = pupil * np.exp(1j*phasor)
pupil_pad = zeros_padding(pupil, zeros_padding_factor)

mask = eight_faces_four_pupils_pyramid_mask(npx*zeros_padding_factor, 
            amplitude = 2*np.pi * zeros_padding_factor * npx/4 * 2)

focal_plane = get_focal_plane_image(pupil_pad)
wfs_plane = get_ffwfs_frame(pupil_pad, np.exp(1j*mask))

#%%

def romanesco_mask(nx, amplitude, radius, theta_ref=0):
    """
    Build the pyramid mask
    
    Parameters
    ----------
    nx : number of pixels.
    nFaces : number of faces for the pyramidal mask.
    angle : angle of the pyramid  #TODO: definition? which unit?
    theta_ref : rotation angle of the pyramid faces.
    """
    
    nFaces = 8
    theta_list = [np.pi/4, 3*np.pi/4, 7*np.pi/4, 5* np.pi/4]
    quadrant_list = [0,1,0,1,2,3,2,3]
    
    xx,yy = np.mgrid[0:nx,0:nx] - nx//2 +0.5
    theta = np.mod(np.arctan2(xx,yy)+np.pi-theta_ref,2*np.pi)
    theta_face = 2*np.pi/nFaces
    msk = np.zeros((nx,nx), dtype=complex)

    for k in range(0,nFaces):
        # Tesselation
        theta_inf = k*theta_face<=theta
        theta_sup = theta<(k+1)*theta_face
        m = theta_inf * theta_sup
        # Tip-Tilt 
        tilt = get_tilt([nx, nx], theta=theta_list[quadrant_list[k]], 
                        amplitude = amplitude)
        # theta_direction = (k+0.5)*theta_face
        # c_tip = np.sin(theta_direction+theta_ref)
        # c_tilt = np.cos(theta_direction+theta_ref)
        # Complex mask on each face
        msk += m*np.exp(2j*np.pi*tilt)
    
    mask = np.exp(1j*get_4pywfs_phase_mask(2*[nx], amplitude))
    
    radial_coordinates = (xx**2 + yy**2)**0.5

    mask[radial_coordinates<=radius] = msk[radial_coordinates<=radius]
    
    
    return mask
