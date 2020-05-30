## NOTE: This function is only designed to return one date.  The 'n_locations' input doesn't yet do anything

import random
from array import *
import rasterio as rio
from numpy.random import choice
import numpy as np
from datetime import datetime, date, timedelta

def get_date( start_date, 
             end_date, 
             geotiff_directory,
             n_locations,
             delta_time
            ):
    
    # Load GeoTIFF files for each month and add up VTE
    months = array('i',range(1,13))
    total_vte_by_month = []

    for month in months:

        # The filenames are formated as "all_2018_MM.tif"
        f_name = f'{geotiff_directory}all_2018_{month:02.0f}.tif'

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

    # Randomly select month based on weighting by vessel traffic
    month_random = choice( months, 
                       n_locations , 
                       p = vte_probability
                     )

    # Now that month is selected, we need to choose day, year, and time.  We weight these all the same
    time_period = end_date - start_date
    time_period_inhours = np.int(time_period.total_seconds()/3600)
    date_arr = [start_date + timedelta(hours=i) for i in range(0,time_period_inhours+1)]

    # Extract dates in time period for only the month selected as month_random
    date_arr_select = []
    for days in date_arr:
        if days.month == month_random:
            date_arr_select.append(days)

    return random.choice(date_arr_select)
