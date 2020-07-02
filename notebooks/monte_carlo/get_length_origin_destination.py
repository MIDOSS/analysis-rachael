import geopandas 
import datetime 
import numpy 
import salishsea_tools 

def get_length_origin_destination( shapefile_directory, 
                                   vessel_type, 
                                   month, 
                                   spill_lat,
                                   spill_lon,
                                   search_radius,
                                   random_seed=None
                                 ):
    
    # These are the values to use for testing
    # search_radius = 0.5 # km
    # vessel_type = 'cargo'
    # month       = '01'
    # shapefile_directory  = '/Users/rmueller/Data/MIDOSS/{vessel_type}_2018_{month}/'

    ### the shapefile and directory are hardcoded for now 
    
    shapefile = f'{vessel_type}_2018_{month}.shp'
    
    # load data
    data = geopandas.read_file(shapefile_directory + shapefile)
    [nrows,ncols] = data.shape
    
    # think about a way of doing this that doesn't require 
    # loading all lat/lon values (with a healthy dose of patience)
    display('this is going to take a minute....')
    lon_array = [data.geometry[i].coords[0][0] for i in range(nrows)]
    lat_array = [data.geometry[i].coords[0][1] for i in range(nrows)]
    
    # identify all the lines within search_radius
    distance = salishsea_tools.geo_tools(spill_lon, spill_lat, lon_array, lat_array)
    array_index = numpy.where(distance < search_radius)
    
    total_seconds  = numpy.zeros(len(array_index))
    total_distance = numpy.zeros(len(array_index))
    vte            = numpy.zeros(len(array_index))

    # loop through values in array_index values to calculate 
    for index in range(len(array_index)):

        # calculate the duration of travel for each poly line segment
        start_date = datetime.datetime.strptime(data.ST_DATE[index] , 
                                       '%Y-%m-%d %H:%M:%S'
                                      )
        end_date = datetime.datetime.strptime(data.EN_DATE[index] ,
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
        total_distance[index] = salishsea_tools.geo_tools.haversine( 
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
   
    # standardize ATB and tug lengths to represent length of tug and tank barge
    # see [AIS data attribute table](https://docs.google.com/document/d/14hAxrTFpKloy88zRYLL4TiqLwbn8s53MYQeCt6B3MJ4/edit) 
    # for more information
    
    # Initialize PCG-64 random number generator
    random_generator = numpy.random.default_rng(random_seed)
    if vessel_type == 'tug' or vessel_type == 'atb' and length < 100:
        length = random_generator.choice([147, 172, 178, 206, 207])
        
    # that's a wrap, folks.
    return length, origin, destination