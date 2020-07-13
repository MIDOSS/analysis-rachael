import numpy 
import yaml
import pathlib

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Uses data in yaml file to allocate fuel for cases WITH 
# origin/destination

def get_oil_type_cargo(yaml_file, facility, ship_type, random_seed):
   
    # Initialize PCG-64 random number generator
    random_generator = numpy.random.default_rng(random_seed)

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
                    raise Exception('Error: fraction of fuel transfers'\ 
                                    f'for {ship} servicing {facility}'\
                                    ' does not sum to 1')
                
            return fuel_type

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Uses data in yaml file to allocate fuel for cases of generic origin  
# or destination of 'US', 'Pacific', or 'Canada' just ship type. 
# Same as `get_oil_type_cargo but these yaml files lack facility names.  

def get_oil_type_cargo_generic_US(yaml_file, ship_type, random_seed):
   
    # Initialize PCG-64 random number generator
    random_generator = numpy.random.default_rng(random_seed)

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
                    raise Exception('Error: fraction of fuel transfers'\ 
                                    f'for {ship} servicing {facility}'\
                                    ' does not sum to 1')
                
            return fuel_type