import rasterio as rio
import numpy as np
from numpy.random import choice

def get_vessel_type(geotiff_directory, 
                    vessel_types, 
                    ais_data_year, 
                    n_locations, 
                    spill_month, 
                    x_index,
                    y_index
                   ):

    vessel_type = []

    for location in range(n_locations):

        # initialize array used to store vessel time exposure values for each vessel type
        VTE_by_vessel_and_location = []

        # loop through each vessel type and store VTE for each vessel type, at selected location
        for name in vessel_types:

            traffic_reader = rio.open(
                geotiff_directory/
                f'{name}_{ais_data_year}_{spill_month:02.0f}.tif'
            )

            # dataset closes automatically using the method below
            with traffic_reader as dataset:

                # resample data to target shape
                data = dataset.read(1,
                    out_shape=(
                        dataset.count,
                        int(dataset.height),
                        int(dataset.width)
                    ),
                )

                # Set all no-data values to zero
                data[data < 0] = 0

            # Store vessel time exposure [hours/km^2] for each vessel-type in array
            VTE_by_vessel_and_location.append(data[x_index[location],y_index[location]])

        # Calculate relative probability of vessel occurance based on VTE by vessel-type
        probability = VTE_by_vessel_and_location/np.sum(VTE_by_vessel_and_location)

        # Randomly select vessel type based on relative vessel time exposure probability
        vessel_random = choice(vessel_types, 
                              n_locations , 
                              p = probability)

        # populate vessel type selection for each n-locations
        # vessel_type.append(vessel_random)
        vessel_type = vessel_random[0] 
        
    return vessel_type