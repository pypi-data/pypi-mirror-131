
This package contains functions used in data processing of hyperspectral images
captured using a scanning Fabry-Pérot interferometer (FPI). This includes transmission
simulations of the FPI itself.

## Image handling

### HSTI.import_data_cube(path)

  This function imports the hyperspectral thermal datacube from the raw output of the camera. The path that the function uses as input must be the one containing the 'images' directory.

### HSTI.export_data_cube(cube, folder_name)

  This function takes an HSTI numpy array and exports it as individual .ppm
  images to a folder given by folder_name.

### HSTI.remove_stuck_px(cube)

  This function removes the dead pixels in the bolometer by replacing them with the average of their non-zero neighbors.

### HSTI.remove_outlying_px(cube, cut_off)

  This function removes outlying pixel measurements of values higher than the cut off value.

### HSTI.median_filter_cube(cube, kernel_size)

  This function runs a median filter across the image plane. The size of the kernel must be defined.

## Preprocessing

### HSTI.remove_vignette(cube)

  This function takes a single HSTI as input and returns a new vignetting corrected cube.

### HSTI.debend(cube, central_mirror_sep)

  This function takes a single HSTI as input and returns a new spectral bending corrected cube.

### HSTI.baseline(cube)

  This function subtracts the mean pixel value from every band in the datacube.

### HSTI.standardize(cube)

  This function subtracts the mean pixel value from every band in the datacube and divides all values with the pixel standard deviation.

### HSTI.normalize_cube(cube)

  This function normalises the entire data cube by dividing all bands by the sum of the bands.

### HSTI.normalize_pixel(cube)

  This function normalises the entire data cube by dividing all bands by the sum of the bands in each individual pixel.

### HSTI.sbtrct_first_band(cube)

  This function subtracts the first band from the remaining bands in the datacube, effectively setting the first band to zero.


## Common analysis


### HSTI.fps(points, n_seeds)

  Function which distributes n_seeds (a numper of points) equally within a lists
  of points to obtain furthest point sampling.

  The function takes in a list of points. Every entry in the list contains both the
  x and y coordinate of a given point. It returns the coordinates of the selected
  sample points


### HSTI.voronoi(array_2D, n_seeds)

  This function .

### HSTI.mse(lst1, lst2)

  This function returns the mean square error (MSE) between two lists of same length.


## FPI Simulation

### HSTI.fpi_sim()

  This function .

### HSTI.fpi_sim_matrix()

  This function .

### HSTI.fpi_sim_matrix_angular()

  This function .


# Contact

  for bug reports or other questions please contact mani@newtec.dk or alj@newtec.dk
