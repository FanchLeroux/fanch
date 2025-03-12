# -*- coding: utf-8 -*-
"""
Created on Wed Mar 12 11:53:58 2025

@author: fleroux
"""

import pickle
import inspect

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

def load_vars(filename):
    caller_vars = inspect.stack()[1].frame.f_locals
    with open(filename, 'rb') as f:
        saved_vars = pickle.load(f)
    caller_vars.update(saved_vars)