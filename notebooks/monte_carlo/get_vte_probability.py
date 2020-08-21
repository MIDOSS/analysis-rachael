# This function returns a 1x12 array of 2018 Vessel Traffic Exposure probabilities by month, calculated as sum_of_monthly_vte / sum_of_vte_over_year

import rasterio as rio
import numpy as np
import pathlib
from array import *

def get_vte_probability( 
    geotiff_directory 
):

    # Load GeoTIFF files for each month and add up VTE
    months = array('i',range(1,13))
    total_vte_by_month = []

    for month in months:

        # The filenames are formated as "all_2018_MM.tif"
        f_name = geotiff_directory/f'all_2018_{month:02.0f}.tif'
        
        # open GeoTIFF file for reading
        traffic_reader = rio.open(f_name)

        # load data in a way that automatically closes file when finished
        with traffic_reader as dataset:

            # resample data to target shape
            data = dataset.read(1)

            # remove no-data values and singular dimension 
            data = np.squeeze(data)
            data[data < 0] = 0

            total_vte_by_month.append(data.sum())

    # calculate VTE probability by month based on total traffic for each month        
    vte_probability = total_vte_by_month / np.sum(total_vte_by_month)

    return vte_probability
