# -*- coding: utf-8 -*-
"""
Created on Wed Mar 12 11:53:58 2025

@author: fleroux
idea from : https://stackoverflow.com/questions/6568007/how-do-i-save-and-restore-multiple-variables-in-python
"""

import pickle
import inspect

import pathlib

from fanch.tools.miscellaneous import warning

def save_vars(filename, var_names):
    '''
    Save several variables to a pickle file
    such that their variable names can be recovered.
    Usage: `save_vars('variables.pkl', ['a', 'b'])`
    '''
    caller_vars = inspect.stack()[1].frame.f_locals
    saved_vars = {var_name: caller_vars[var_name] for var_name in var_names} # to skip missing ones, add `if var_name in caller_vars`
    with open(filename, 'wb') as f:
        pickle.dump(saved_vars, f)

def load_vars(filename, var_names=False):
    '''
    Load variables from a pickle file
    such that their variable names can be recovered,
    and that one can choose which variables to load
    Usage: `load_vars('variables.pkl', ['a', 'b'])`
    '''
    
    filename = pathlib.Path(filename)
    
    caller_vars = inspect.stack()[1].frame.f_locals
    with open(filename, 'rb') as f:
        saved_vars = pickle.load(f)
        
    if var_names:
        for var_name in var_names:
            if var_name in list(saved_vars.keys()):
                caller_vars.update({var_name:saved_vars[var_name]})
            else:
                warning(var_name+' not in '+str(filename.name))
    else:
        caller_vars.update(saved_vars)
        