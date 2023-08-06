This package contains functions used in data processing of hyperspectral images
captured using a scanning Fabry-Pérot interferometer (FPI). This includes transmission
simulations of the FPI itself.


# Package Documentation and Modules:

## Image analysis

### hsti_import

  'import_data_cube(path)'

  This function imports the hyperspectral thermal datacube from the raw output of the camera. The path that the function uses as input must be the one containing the 'images' directory.

### hsti_export

  'export_data_cube(data_cube, folder_name)'

  This function takes an HSTI numpy array and exports it as individual .ppm
  images to a folder given by folder_name.


### remove_bad_px

  'remove_stuck_px(cube)'


  'remove_outlying_px(cube, cut_off)'


### remove_vignetting

  'remove_vignette()'

  the function takes a single HSTI as input and returns a new vignetting corrected cube.


### spectral_debending

  'debend(cube, central_mirror_sep)'

  the function takes a single HSTI as input and returns a new spectral bending corrected cube.


### fill_gaps



### farthest_point_sampling

  'fps(points, n_seeds)'

  Function which distributes n_seeds (a numper of points) equally within a lists
  of points to obtain furthest point sampling.

  The function takes in a list of points. Every entry in the list contains both the
  x and y coordinate of a given point. It returns the coordinates of the selected
  sample points



### voronoi_partitioning



### mse

  'mse(lst1, lst2)'

  the function returns the mean square error (MSE) between two lists of same length.


-------------------
## FPI transmission

### fpi_sim



### fpi_sim_matrix



### fpi_sim_matrix_angular


# Contact

  for bug reports or other questions please contact mani@newtec.dk or alj@newtec.dk
