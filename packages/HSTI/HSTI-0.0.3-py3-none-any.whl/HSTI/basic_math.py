import numpy as np
from scipy.ndimage import median_filter
from IPython.display import clear_output


def baseline(data_cube):
    gray_cube = np.mean(data_cube, axis = 2)
    gray_cube = gray_cube[:,:,np.newaxis]
    gray_cube = np.repeat(gray_cube, data_cube.shape[2], axis = 2)

    data_cube = data_cube - gray_cube

    return data_cube

def standardize(data_cube):
    std_cube = np.std(data_cube, axis = 2)
    std_cube = std_cube[:,:,np.newaxis]
    std_cube = np.repeat(std_cube, data_cube.shape[2], axis = 2)
    baselined_cube = baseline(data_cube)

    data_cube = baselined_cube/std_cube

    return data_cube

def normalize_cube(data_cube):
    min_cube = np.min(data_cube, axis = 2)
    min_cube = min_cube[:,:,np.newaxis]
    min_cube = np.repeat(min_cube, data_cube.shape[2], axis = 2)

    data_cube = data_cube - min_cube
    data_cube = data_cube/np.max(data_cube)

    return data_cube

def normalize_pixel(data_cube):
    min_cube = np.min(data_cube, axis = 2)
    min_cube = min_cube[:,:,np.newaxis]
    min_cube = np.repeat(min_cube, data_cube.shape[2], axis = 2)

    data_cube = data_cube - min_cube

    max_cube = np.max(data_cube, axis = 2)
    max_cube = max_cube[:,:,np.newaxis]
    max_cube = np.repeat(max_cube, data_cube.shape[2], axis = 2)

    data_cube = data_cube/max_cube

    return data_cube

def sbtrct_first_band(data_cube):
    first_cube = data_cube[:,:,0]
    first_cube = first_cube[:,:,np.newaxis]
    first_cube = np.repeat(first_cube, data_cube.shape[2], axis = 2)

    data_cube = data_cube - first_cube

    return data_cube


def median_filter_cube(data_cube, kernel_size, verbose = True):
    NoB = data_cube.shape[2]
    for j in range(NoB):
        if verbose:
            clear_output(wait=True)
            print(f"Median filtering, {round(100*(j+1)/NoB,2)} %")
        data_cube[:,:,j] = median_filter(data_cube[:,:,j], size=kernel_size)

    return data_cube
