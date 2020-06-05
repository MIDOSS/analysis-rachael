import geopandas as gpd
from datetime import datetime, date, timedelta
import numpy as np
from salishsea_tools import geo_tools

def get_length_origin_destination(vessel_type, month):
    
    vessel_type = 'cargo'
    month       = '01'
    search_radius = 0.5 # km
    
    ### the shapefile and directory are hardcoded for now 
    shapedir  = '/Users/rmueller/Data/MIDOSS/cargo_2018_01/'
    shapefile = f'{vessel_type}_2018_{month}.shp'
    
    # load data
    data = gpd.read_file(shapedir + shapefile)
    
    # think about a way of doing this that doesn't require 
    # loading all lat/lon values (with a healthy dose of patience)
    display('this is going to take a minute....')
    lon_array = [data.geometry[i].coords[0][0] for i in range(nrows)]
    lat_array = [data.geometry[i].coords[0][1] for i in range(nrows)]
    
    # identify all the lines within search_radius
    distance = geo_tools.haversine(spill_lon, spill_lat, lon_array, lat_array)
    array_index = np.where(distance < search_radius)
    
    total_seconds  = np.zeros(len(array_index))
    total_distance = np.zeros(len(array_index))
    vte            = np.zeros(len(array_index))

    # loop through values in array_index values to calculate 
    for index in range(len(array_index)):

        # calculate the duration of travel for each poly line segment
        start_date = datetime.strptime(data.ST_DATE[index] , 
                                       '%Y-%m-%d %H:%M:%S'
                                      )
        end_date = datetime.strptime(data.EN_DATE[index] ,
                                     '%Y-%m-%d %H:%M:%S'
                                    )
        delta_time = end_date - start_date
        total_seconds[index] = delta_time.total_seconds()

        # calculate the distance of each poly line
        start_lon = data.geometry[index].coords[0][0]
        start_lat = data.geometry[index].coords[0][1]
        end_lon   = data.geometry[index].coords[1][0]
        end_lat   = data.geometry[index].coords[1][1]

        # calculate the distance in km of vessel line segment
        total_distance[index] = geo_tools.haversine( 
            start_lon, start_lat, end_lon, end_lat 
        )
        vte[index] = total_seconds[index]/total_distance[index]

    # find the index for greatest vte (for cases where there is 
    # more than one polyline)    
    i, = np.where(vte == max(vte))
    the_one = array_index[i.item()]
    
    # now that we have found the one true polyline, lets get its digits!
    length = data.LENGTH[the_one.item()]
    origin = data.FROM_[the_one.item()]
    destination = data.TO[the_one.item()]
    
    # that's a wrap, folks.
    return length, origin, destination