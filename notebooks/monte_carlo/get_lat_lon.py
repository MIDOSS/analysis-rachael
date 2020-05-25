import rasterio as rio
import numpy as np
from numpy.random import choice

def get_lat_lon(geotiff_directory, spill_month, n_locations):
    
    # identify string to use for input file name
    if spill_month==9:
        month_name = 'September' #I'm sure there is a way to do this using Datetime!
    
    # load data
    traffic_reader = rio.open(f'{geotiff_directory}{month_name}_2018_All_Tugs_Hours_Geographic.tif')
    traffic_data = traffic_reader.read(1)
    traffic_data[traffic_data < 0] = 0

    # calculate probability of traffic by VTE in given month
    probability_distribution  = traffic_data/traffic_data.sum()
    [nx,ny] = probability_distribution.shape

    # create a matrix of lat/lon values 
    latlontxt = np.chararray((nx,ny), itemsize = 20)
    for y in range(ny):
        for x in range(nx):
            x2, y2 = traffic_reader.transform * (y,x)
            latlontxt[x,y] = "lat" + str(truncate(x2, 3)) + "lon" + str(truncate(y2, 3))

    # reshape 2D matrix to vector
    latlontxt_1D = latlontxt.reshape(-1)

    # use 'choice' function to randomly select lat/lon location based on vessel time exposure probability
    a = choice(latlontxt.reshape(-1), n_locations , p=probability_distribution.reshape(-1))

    # extract lat/lon value(s)
    lats = np.array([])
    lons = np.array([])
    for i in a:
        lats = np.append(lats, float(i[3:11]))
        lons = np.append(lons, float(i[14:]))
        
    return lats, lons
