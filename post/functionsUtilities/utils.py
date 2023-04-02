'''
collection of utility methods shared across files
'''

import os
import numpy as np

#==============================================================================#
# Serial sampling of blackbox
def serial_sampling(args,params,func):
    results = []; i = 0
    for arg in args:  
        result = func(i, arg, params)
        results.append(result)

        i += 1

    return results

#==============================================================================#
# Parallel sampling of blackbox
def parallel_sampling(args,params,func,num_threads=4):
    from multiprocessing import Pool

    parallel_args = []; i = 0
    for arg in args:
        parallel_args += [(i,arg,params)]
        i += 1
        
    with Pool(num_threads) as pool:
        results = pool.starmap(func, parallel_args)

    return results

#==============================================================================#
# Create empty directory
def check_folder(folder='render/'):
    '''check if folder exists, make if not present'''
    if not os.path.exists(folder):
            os.makedirs(folder)

#==============================================================================#
# SCALING BY A RANGE
def scaling(x,l,u,operation):
    # scaling() scales or unscales the vector x according to the bounds
    # specified by u and l. The flag type indicates whether to scale (1) or
    # unscale (2) x. Vectors must all have the same dimension.
    
    if operation == 1:
        # scale
        x_out=(x-l)/(u-l)
    elif operation == 2:
        # unscale
        x_out = l + x*(u-l)
    
    return x_out

#==============================================================================#
# Load CSV data generated by COVID_SIM_UI or CovidSim
def load_matrix(filename, folder='data_dynamic'):
    '''loads tracking grid coordinates from disk

    Function that loads the tracking grid coordinates from specific files on the disk.
    Loads the state of the grid_coords matrix

    Keyword arguments
    -----------------

    tstep : int
        the timestep that will be saved
    ''' 
    matrix = np.loadtxt('%s/%s.bin' %(folder,filename))
    return matrix