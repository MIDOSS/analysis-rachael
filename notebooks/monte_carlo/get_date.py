
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# get_date: Returns spill date and time, weighted by monthly vessel traffic
#
# Inputs:
#   start_date, end_date: Datetime values.  
#   vte_probabilyt: Output from get_vte_probability
#   delta_time: input file resolution (1-hour for Salish Sea Cast)
#
# Example call: get_date( datetime(2015, 1, 1, 0, 30), 
#			  datetime(2018, 12, 31, 23, 55),
#			  get_vte_probability( geotiff_directory ),
#                         timedelta(hours = 1)
#			)
# 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import random
import numpy as np
from numpy.random import choice
from datetime import datetime, date, timedelta
from array import *

def get_date( start_date, 
              end_date, 
              vte_probability,
              delta_time
            ):
    
    # Create an array of months to use for random selection
    months = array('i',range(1,13))
    
    # Randomly select month based on weighting by vessel traffic
    n_locations = 1 # we are only selecting 1-value for 1-location 
    month_random = choice( months, 
                       n_locations, 
                       p = vte_probability
                     )

    # Now that month is selected, we need to choose day, year, and time.  
    # We weight day within month, year, and hour equally
    time_period = end_date - start_date
    time_period_inhours = np.int(time_period.total_seconds()/3600)
    date_arr = [start_date + timedelta(hours=i) 
                 for i in range(0,time_period_inhours + 1)]

    # Extract dates in time period for only the month selected as month_random
    date_arr_select = []
    for days in date_arr:
        if days.month == month_random:
            date_arr_select.append(days)

    return random.choice(date_arr_select)
