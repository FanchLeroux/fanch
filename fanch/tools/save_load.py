# -*- coding: utf-8 -*-
"""
Created on Wed Mar 12 11:53:58 2025

@author: fleroux
idea from : https://stackoverflow.com/questions/6568007/how-do-i-save-and-restore-multiple-variables-in-python
"""

import pickle
import inspect

from copy import deepcopy

import dill

import pathlib

from fanch.tools.miscellaneous import warning

def save_vars(filename, var_names=False):
    '''
    Save several variables to a pickle file
    such that their variable names can be recovered.
    Usage: `save_vars('variables.pkl', ['a', 'b'])`
    '''

    if var_names == False:
        objs = deepcopy(locals())
        for obj in objs:
            if obj.startswith('_') or str(type(objs[obj])) == "<class 'module'>"\
                or str(type(objs[obj])) == "<class 'function'>":
                del locals()[obj]
        del obj, objs
        dill.dump_session(filename)
        warning("As var_names was not provided, pkl file was generated with dill.dump_session method")

    else:
        caller_vars = inspect.stack()[1].frame.f_locals
        saved_vars = {var_name: caller_vars[var_name] for var_name in var_names} # to skip missing ones, add `if var_name in caller_vars`
        with open(filename, 'wb') as f:
            dill.dump(saved_vars, f)

def load_vars(filename, var_names=False, load_session=False):
    '''
    Load variables from a pickle file
    such that their variable names can be recovered,
    and that one can choose which variables to load
    Usage: `load_vars('variables.pkl', ['a', 'b'])`
    '''
    
    filename = pathlib.Path(filename)
    
    
        
    if var_names:
        
        caller_vars = inspect.stack()[1].frame.f_locals
        with open(filename, 'rb') as f:
            saved_vars = dill.load(f)
        
        for var_name in var_names:
            if var_name in list(saved_vars.keys()):
                caller_vars.update({var_name:saved_vars[var_name]})
            else:
                warning(var_name+' not in '+str(filename.name))
    
    elif load_session:
        dill.load_session(filename)
    
    else:
        caller_vars = inspect.stack()[1].frame.f_locals
        with open(filename, 'rb') as f:
            saved_vars = dill.load(f)
            caller_vars.update(saved_vars)