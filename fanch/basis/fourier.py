# -*- coding: utf-8 -*-
"""
Created on Tue Dec 24 10:08:04 2024

@author: fleroux
"""

import numpy as np
import matplotlib.pyplot as plt

def sort_real_fourier_basis(basis_map):
    
    n_px = basis_map.shape[2]
    my_list = []
    
    for nu_x in np.arange(-n_px//2 + 1, n_px//2 + 1):
        for nu_y in np.arange(0, n_px//2 + 1):
            if (nu_x == 0 and nu_y == 0) or (nu_x == 0 and nu_y == n_px//2)\
            or (nu_x == n_px//2 and nu_y == n_px//2) or (nu_x == n_px//2 and nu_y == 0):
                my_list.append([(nu_x**2 + nu_y**2)**0.5, basis_map[:,:,nu_x,nu_y,0].tolist()])
            elif (nu_y != 0 or nu_x >= 0) and  (nu_y != n_px//2 or nu_x >= 0):
                my_list.append([(nu_x**2 + nu_y**2)**0.5, basis_map[:,:,nu_x,nu_y,0].tolist()])
                my_list.append([(nu_x**2 + nu_y**2)**0.5, basis_map[:,:,nu_x,nu_y,1].tolist()])
    
    my_list.sort()
    
    basis = np.empty((basis_map.shape[0], basis_map.shape[1], len(my_list)))
    basis.fill(np.nan)
    
    for k in range(len(my_list)):
        basis[:,:,k] = np.array(my_list[k][1])
            
    return basis

def compute_real_fourier_basis(n_px:int, *, return_map = False):
    
    basis_map = np.empty((n_px, n_px, n_px, n_px//2+1, 2), dtype=float)
    basis_map.fill(np.nan)
    
    [X,Y] = np.meshgrid(np.arange(-n_px//2 + 1, n_px//2 + 1), np.flip(np.arange(-n_px//2 + 1, n_px//2 + 1)))
    
    for nu_x in np.arange(-n_px//2 + 1, n_px//2 + 1):
        for nu_y in np.arange(0, n_px//2 + 1):
            
            if (nu_x == 0 and nu_y == 0) or (nu_x == 0 and nu_y == n_px//2)\
            or (nu_x == n_px//2 and nu_y == n_px//2) or (nu_x == n_px//2 and nu_y == 0):
                
                basis_map[:,:,nu_x, nu_y, 0] = 1./n_px * np.cos(2.*np.pi/n_px * (nu_x * X + nu_y * Y))
                
            elif (nu_y != 0 or nu_x >= 0) and  (nu_y != n_px//2 or nu_x >= 0):
                
                basis_map[:,:,nu_x, nu_y, 0] = 2**0.5/n_px * np.cos(2.*np.pi/n_px * (nu_x * X + nu_y * Y))
                basis_map[:,:,nu_x, nu_y, 1] = 2**0.5/n_px * np.sin(2.*np.pi/n_px * (nu_x * X + nu_y * Y))
    
                
    if return_map:
        return basis_map
    else:
        return sort_real_fourier_basis(basis_map)

def extract_subset(complete_real_fourier_basis, new_n_px):
    return np.roll(complete_real_fourier_basis
                   [:,:,np.arange(-new_n_px//2+1,new_n_px//2+1),0:new_n_px//2+1,:]
                   , -new_n_px//2 + 1, axis = 2)

def extract_horizontal_frequencies(basis_map):
    
    horizontal_frequencies = basis_map[:,:,:,0,0]
    return horizontal_frequencies

def extract_vertical_frequencies(basis_map):
    
    vertical_frequencies = basis_map[:,:,0,:,0]
    return vertical_frequencies

def extract_diagonal_frequencies(basis_map, complete = 0):
    
    diagonal_frequencies = np.empty((basis_map.shape[0], basis_map.shape[1], basis_map.shape[3]))
    diagonal_frequencies.fill(np.nan)
    
    for k in range(basis_map.shape[3]):
        diagonal_frequencies[:,:,k] = basis_map[:,:,k,k,0]
    
    if complete:
        diagonal_frequencies = np.empty((basis_map.shape[0], basis_map.shape[1], 2*basis_map.shape[3]-2))
        diagonal_frequencies.fill(np.nan)
        index = 0
        for k in range(basis_map.shape[3]):
            diagonal_frequencies[:,:,index] = basis_map[:,:,k,k,0]
            if k != basis_map.shape[3]-1 and k !=0:
                diagonal_frequencies[:,:,index+1] = basis_map[:,:,k,k,1]
                index += 2
            else:
                index += 1
    
    return np.array(diagonal_frequencies)