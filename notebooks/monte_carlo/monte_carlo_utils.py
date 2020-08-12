import numpy 
import yaml
import pathlib

def make_bins(lower_bound, upper_bound, step_size):
    """ Returns an ascending list of tuples from start to stop, with
        an interval of width and the center point values for intervals
    
        A tuple bins[i], i.e. (bins[i][0], bins[i][1])  with i > 0 
        and i < quantity, satisfies the following conditions:
            (1) bins[i][0] + width == bins[i][1]
            (2) bins[i-1][0] + width == bins[i][0] and
                bins[i-1][1] + width == bins[i][1]
    """
    
    bins = []
    center_points = []
    for low in range(lower_bound, upper_bound, step_size):
        bins.append((low, low + step_size))
        center_points.append(low + step_size/2)
    return bins, center_points

def get_bin(value, bins):
    """ bins is a list of tuples, like [(0,20), (20, 40), (40, 60)],
        binning returns the smallest index i of bins so that
        bin[i][0] <= value < bin[i][1]
    """
    
    for i in range(0, len(bins)):
        if bins[i][0] <= value < bins[i][1]:
            return i
    return -1

def place_into_bins(sorting_data, data_to_bin, bins):
    """ Sorting_data and data_to_bin are 1D arrays of the same length.
        In our case, they are different attributes of vessels identified by MMSI.
        We use the 'sorting_data' attribute to select the bin into which 
        the value(s) of 'data_to_bin' is added.
        The output, binned_data, has the same length as 'bins', which is 
        the output variable of the function 'make_bins'. 
    """
    
    binned_data = numpy.zeros(len(bins))
    index = 0
    for value in sorting_data:
        # accounting for no-data: -99999
        if value > 0:
            bin_index = get_bin(value, bins)  
            binned_data[bin_index] += data_to_bin[index]    
        index += 1
    return binned_data

# 
def clamp(n, minn, maxn):
    """ minn and maxn are scalars that represent min and max capacities
        clamp ensures that capacities are within min/max thresholds
        and sets n to minn or maxn if outside of thresholds, such that
        minn < n < maxn
    """
    if n < minn:
        return minn
    elif n > maxn:
        return maxn
    else:
        return n
    

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Uses data in yaml file to allocate fuel for cases WITH 
# origin/destination

def get_oil_type_cargo(yaml_file, facility, ship_type, random_generator):

    with yaml_file.open("rt") as file:
            
            # load fraction_of_total values for weighting 
            # random generator
            cargo = yaml.safe_load(file)
            ship = cargo[facility][ship_type]
            probability = [ship[fuel]['fraction_of_total'] 
                           for fuel in ship] 
            
            # First case indicates no cargo transfer to/from terminal 
            # (and a mistake in origin/destination analysis).
            # 
            # Second case ensures neccessary conditions for 
            # random_generator
        
            if sum(probability) == 0:
                fuel_type = []
            else:
                try:
                    fuel_type = random_generator.choice(
                              list(ship.keys()), p = probability)
                except ValueError:
                    # I was getting an error when including a '\' at the
                    # end of first line, so I removed it....
                    raise Exception(['Error: fraction of fuel transfers ' 
                                    + f'for {ship_type} servicing {facility} '\
                                    + f'does not sum to 1 in {yaml_file}'])
                
            return fuel_type

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Uses data in yaml file to allocate fuel for cases of generic origin  
# or destination of 'US', 'Pacific', or 'Canada' just ship type. 
# Same as `get_oil_type_cargo but these yaml files lack facility names.  

def get_oil_type_cargo_generic_US(yaml_file, ship_type, random_generator):
   
    with yaml_file.open("rt") as file:
            
            # load fraction_of_total values for weighting random generator
            cargo = yaml.safe_load(file)
            ship = cargo[ship_type]
            probability = [ship[fuel]['fraction_of_total'] for fuel in ship] 
            
            # First case indicates no cargo transfer to/from terminal 
            # (and a mistake in origin/destination analysis).
            # 
            # Second case ensures neccessary conditions for random_generator
        
            if sum(probability) == 0:
                fuel_type = []
            else:
                try:
                    fuel_type = random_generator.choice(
                        list(ship.keys()), p = probability)
                except ValueError:
                    # I was getting an error when including a '\' at the
                    # end of first line, so I removed it....
                    raise Exception('Error: fraction of fuel transfers ' 
                                    f'for {ship_type} servicing {facility} '\
                                    f'does not sum to 1 in {yaml_file}')
                
            return fuel_type