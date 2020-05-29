from rasterio.enums import Resampling
import rasterio as rio
import numpy as np
from numpy.random import choice

def truncate(f, n):
    '''Truncates/pads a float f to n decimal places without rounding'''
    s = '{}'.format(f)
    if 'e' in s or 'E' in s:
        return '{0:.{1}f}'.format(f, n)
    i, p, d = s.partition('.')
    return '.'.join([i, (d+'0'*n)[:n]])

def get_lat_lon_indices(geotiff_directory, spill_month, n_locations, upsample_factor):    

    print('Randomly selecting spill location from all-traffic GeoTIFF:')
  
    traffic_reader = rio.open(f'{geotiff_directory}all_2018_{spill_month:02.0f}.tif')

    # dataset closes automatically using the method below
    with traffic_reader as dataset:

        # resample data to target shape
        data = dataset.read(1,
            out_shape=(
                dataset.count,
                int(dataset.height * upsample_factor),
                int(dataset.width * upsample_factor)
            ),
            resampling=Resampling.bilinear
        )

        # scale image transform
        transform = dataset.transform * dataset.transform.scale(
            (dataset.width / data.shape[-1]),
            (dataset.height / data.shape[-2])
        )
        
    # remove no-data values and singular dimension 
    data = np.squeeze(data)
    data[data < 0] = 0
    
    # calculate upsampled probability of traffic by VTE in given month
    probability_distribution  = data/data.sum()
    [nx,ny] = probability_distribution.shape

    # create a matrix of lat/lon values 
    print('...Creating 2D array of lat/lon strings (this may take a moment)')
    latlontxt = np.chararray((nx,ny), itemsize = 25)
    for y in range(ny):
        for x in range(nx):
            x2, y2 = traffic_reader.transform * (y,x)
            latlontxt[x,y] = "lat" + str(truncate(x2, 5)) + "lon" + str(truncate(y2, 5))

    # reshape 2D matrix to vector
    latlontxt_1D = latlontxt.reshape(-1)
  
    # use 'choice' function to randomly select lat/lon locations
    print(f'...Selecting {n_locations} location(s)')
    latlontxt_random = choice(latlontxt.reshape(-1), 
                              n_locations , 
                              p = probability_distribution.reshape(-1))

    # extract lat/lon value(s)
    lats = np.array([])
    lons = np.array([])
    x_index = np.array([], dtype = np.int)
    y_index = np.array([], dtype = np.int)
    data_out= np.array([])
    
    print('...Creating vectors of lat/lon pairs and x-index/y-index pairs')
    for latlontxt_str in latlontxt_random:
        
        # create lat/lon vectors
        lats = np.append(lats, float(latlontxt_str[3:12]))
        lons = np.append(lons, float(latlontxt_str[16:]))    
        
        # find x-, y-indices of selected lat/lon pair in 2D latlontxt array
        another_x, another_y = np.where(latlontxt == latlontxt_str)
        
        # create indice vectors
        x_index = np.append(
            x_index, 
            np.int( np.floor(another_x) / upsample_factor) 
        )
        y_index = np.append(
            y_index, 
            np.int(np.floor(another_y) /upsample_factor)
        )
         
        # create data array at x-index, y-index location for QAQC/comparison
        data_out = np.append(
            data_out,
            data[another_x, another_y]
        )
        print("That's a wrap, folks!")
    
    return lats, lons, x_index, y_index, data_out
