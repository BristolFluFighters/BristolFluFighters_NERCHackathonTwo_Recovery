"""Module containing helper functions for slicing and grouping the MET Office air quality data."""

import cartopy.crs as ccrs
import cartopy.io.shapereader as shpreader
import matplotlib.pyplot as plt

import iris
import iris.plot as iplt
import iris.quickplot as qplt
import cftime
import datetime

from shapely.geometry import MultiPoint # used for clipping geographic regions

import numpy as np
import pandas as pd
from random import randint

import shape_utils as shape
import atmos_nrt_utils

import os
import requests  # Used to download data

#Generating the MET Office URL for get requests
def metoffice_url_generator(data_type, file_day):
    """
    https://metdatasa.blob.core.windows.net/covid19-response/index.html
    """

    if data_type == "daqi":
        data_extent = 'aqum_daily'
        data_str = data_type + "_mean"
    else:
        data_extent = 'aqum_hourly'
        data_str = data_type
    
    return (
        f"metoffice_{data_extent}/" +
        f"{data_type}/" +
        f"{data_extent}_{data_str}_{file_day}.nc"
    )

#Return file paths from url - download data if not present
def get_data_file_paths(urls: list, url_prefix: str, raw_data_dir: str) -> list:
    """
    Returns a list of strings describing the filepaths to the data files.

    If the data is not found in the raw_data_dir directory then it is downloaded using a get requst.
    """

    file_paths = []
    for url in urls:
        full_url  = os.path.join(url_prefix, url)
        file_name = os.path.basename(full_url)
        file_path = os.path.join(raw_data_dir ,file_name)
        if not os.path.exists(file_path):
            myfile = requests.get(full_url)
            open(file_path, 'wb').write(myfile.content)
        file_paths.append(file_path)

    return file_paths

#Helper function to get the record from the reader
def get_region_record(target, read_obj, attribute='PUAName'):
    '''
    Get the geometries for the specified target.
    
    '''
    result = None
    for record in read_obj.records():
        location = record.attributes[attribute]
        if location == target:
            result = record
            break
    if result is None:
        emsg = f'Could not find region with {attribute} "{target}".'
        raise ValueError(emsg)
    return result

#Create a random ID generator
def rand_id(ids): 
    return ids[randint(0, len(ids))]

#Get a 2D field and coord data
def _get_2d_field_and_dims(cube):
    """Get a 2D horizontal field, and the horizontal coord dims, from an nD cube."""
    cube_x_coord, = cube.coords(axis='X', dim_coords=True)
    cube_y_coord, = cube.coords(axis='Y', dim_coords=True)
    cube_x_coord_name = cube_x_coord.name()
    cube_y_coord_name = cube_y_coord.name()
    cube_x_coord_dim, = cube.coord_dims(cube_x_coord)
    cube_y_coord_dim, = cube.coord_dims(cube_y_coord)
    field_2d = cube.slices([cube_y_coord_name, cube_x_coord_name]).next()
    coord_dims = sorted([cube_y_coord_dim, cube_x_coord_dim])
    return field_2d, coord_dims
    
#Clipping the cubes
def cut_cubes_to_shape(cubes, shape_record):
    # Make sure we always have a CubeList.
    if isinstance(cubes, iris.cube.Cube):
        cubes = iris.cube.CubeList([cubes])

    # Set up the cube-to-shapefile cutter.
    cutter = shape.Shape(shape_record.geometry, shape_record.attributes, cubes[0].coord_system())

    # First extract subcubes to the shapefile's bounding box.
    subcubes = cutter.extract_subcubes(cubes)
    
    # Now mask the subcubes to the shapefile boundary.
    result = []
    for subcube in subcubes:
        field_2d, dims_2d = _get_2d_field_and_dims(subcube)
        mask_2d = cutter.cube_intersection_mask(field_2d)
        full_mask = iris.util.broadcast_to_shape(mask_2d, subcube.shape, dims_2d)
        new_data = np.ma.array(subcube.data, mask=np.logical_not(full_mask))
        new_cube = subcube.copy(data=new_data)
        result.append(new_cube)
    
    return iris.cube.CubeList(result)

#Convert a cube into a pandas.DataFrame
def convert_cube_to_dateframe(cube: "iris.Cube", region_name: str) -> "pandas.DataFrame":
    """
    Converts the iris.Cube object into a pandas.DataFrame.
    """

    time   = cube.coord('time')
    #length = len(time.points)

    date_str = [date.strftime("%d/%m/%Y %H:%M:%S") for date in time.units.num2date(time.points)]

    #data = {
    #    'date': date_str,
    #   'units': [cube.units]*length}
    #
    #data.update({region_name: cube.data})
    
    #return pd.DataFrame(data, columns=list(data.keys()), index=date_str)
    return pd.DataFrame(cube.data, columns=[region_name], index=date_str)

