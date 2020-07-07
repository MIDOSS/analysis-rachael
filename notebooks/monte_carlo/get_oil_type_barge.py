import numpy 
import yaml
import pathlib
from monte_carlo_utils import get_oil_type_cargo 

#### Decision tree for allocating oil type to barge traffic
# see google drawing 
# [Barge_Oil_Attribution](https://docs.google.com/drawings/d/10PM53-UnnILYCAPKU9MxiR-Y4OW0tIMhVzSjaHr-iSc/edit)
# for a visual representation

def get_oil_type_barge(master_dir,
                    master_file,
                    origin, 
                    destination, 
                    random_seed
                    ):

    ship_type = 'barge'
    
    # This will become an output flag for whether tug 
    # is determined to be non-oil cargo and, hence, fuel-spill risk
    # instead of cargo-spill risk
    fuel_flag = 0

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ##  Load file paths and terminal names
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    with open(f'{master_dir}{master_file}') as file:
        master = yaml.safe_load(file)

    # Assign US and CAD origin/destinations from master file
    CAD_origin_destination = master['categories']['CAD_origin_destination']
    US_origin_destination = master['categories']['US_origin_destination']

    # Get file paths to fuel-type yaml files
    # US_origin is for US as origin
    # US_combined represents the combined import and export of fuel
    home = pathlib.Path(master['directories'])
    CAD_yaml     = home/master['files']['CAD_origin']
    WA_in_yaml   = home/master['files']['WA_destination']
    WA_out_yaml  = home/master['files']['WA_origin']
    US_yaml      = home/master['files']['US_origin']
    USall_yaml   = home/master['files']['US_combined']
    Pacific_yaml = home/master['files']['Pacific_origin']


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # these pairs need to be used together for "get_oil_type_cargo" 
    # (but don't yet have error-checks in place):
    # - "WA_in_yaml" and "destination"
    # - "WA_out_yaml" and "origin"
    #
    # ERROR CATCH for case of no fuel transfer for given selection of 
    # yaml file, origin, and ship_type is currently to set flag to fuel
    # spill potential and not cargo spill potential
    #
    # Why? 
    #
    # Because there are lots of tugs that are not associated
    # with oil tank barges.  The way Casey sub-sampled the AIS data for 
    # tank barges was to select all barges that docked at a marine
    # terminal; however, it's possible that the tugs docked at these
    # marine terminals to fuel up instead of tank-up. This traffic may 
    # appear in cases where origin/destination is an oil terminal but 
    # where no oil cargo is transferred.  In these cases, the spill 
    # potential is deemed as a fuel spill potential and fuel_flag is 
    # set to 1.   
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   
    if origin in CAD_origin_destination:        
        if origin == 'Westridge Marine Terminal':
            if destination in CAD_origin_destination:
                fuel_type = 'jet'            
            else:
                fuel_type = get_oil_type_cargo( 
                          CAD_yaml, origin, ship_type, random_seed)
                
                # *** ERROR CATCH ***
                if not fuel_type:
                    fuel_flag = 1
                    fuel_type = []
                # *** END ERROR CATCH ***   
        else:
            if destination in US_origin_destination:
                # we have better information on WA fuel transfers, 
                # so I'm prioritizing this information source
                fuel_type = get_oil_type_cargo(
                          WA_in_yaml, destination, 
                          ship_type, random_seed)
                
                # *** ERROR CATCH ***
                if not fuel_type:
                    fuel_flag = 1
                    fuel_type = []
                # *** END ERROR CATCH *** 
                
            elif destination == 'ESSO Nanaimo Departure Bay':
                fuel_type = get_oil_type_cargo(
                          CAD_yaml, destination, 
                          ship_type, random_seed)
                
                # *** ERROR CATCH ***
                if not fuel_type:
                    fuel_flag = 1
                    fuel_type = []
                # *** END ERROR CATCH ***  
                
            elif destination == 'Suncor Nanaimo':
                fuel_type = get_oil_type_cargo(
                          CAD_yaml, destination, 
                          ship_type, random_seed)
                
                # *** ERROR CATCH ***
                if not fuel_type:
                    fuel_flag = 1
                    fuel_type = []
                # *** END ERROR CATCH *** 
                
            else: 
                fuel_type = get_oil_type_cargo(
                          CAD_yaml, origin, ship_type, random_seed)
                
                # *** ERROR CATCH ***
                if not fuel_type:
                    fuel_flag = 1
                    fuel_type = []
                # *** END ERROR CATCH ***  
                
    elif origin in US_origin_destination:
        fuel_type = get_oil_type_cargo(
                  WA_out_yaml, origin, ship_type, random_seed)
        
        # *** ERROR CATCH ***
        if not fuel_type:
            fuel_flag = 1
            fuel_type = []
        # *** END ERROR CATCH *** 

    elif destination in US_origin_destination:
        fuel_type = get_oil_type_cargo(
                  WA_in_yaml, destination, ship_type, random_seed)
        
        # *** ERROR CATCH ***
        if not fuel_type:
            fuel_flag = 1
            fuel_type = []
        # *** END ERROR CATCH *** 
        
    elif destination in CAD_origin_destination:
        if destination == 'Westridge Marine Terminal':
            # Westridge doesn't receive crude for storage 
            fuel_type = 'jet'
        else:
            fuel_type = get_oil_type_cargo(
                      CAD_yaml, destination, ship_type, random_seed)
            
            # *** ERROR CATCH ***
            if not fuel_type:
                fuel_flag = 1
                fuel_type = []
            # *** END ERROR CATCH *** 

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # All remaining cases are deemed non-tank traffic. Cam and I tried
    # to eliminate as much non-oil-cargo barges as possible by 
    # evaluating each terminal independently and being more restricted
    # with distance from terminal for including tug traffic in origin-
    # destination analysis and excluding tug traffic to/from 
    # lumbar yards (or equivalent) that are often located very close
    # to oil transfer sites and that were included in Casey's pre-
    # selected data.  These tracks are then given the following
    # attribution of origin/destination as generic "Pacific", "US", 
    # and "Canada" to exclude this traffic as oil cargo traffic
    # Here, I flag these ship tracks as non-oil traffic by setting
    # fuel_flag to 1.
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    elif origin == 'Pacific':
        print(origin)
        fuel_flag = 1
        fuel_type = []
#        fuel_type = get_oil_type_fuel(
#                  fuel_yaml, ship_type, random_seed)
    elif origin == 'US':
        fuel_flag = 1
        fuel_type = []
#         fuel_type = get_oil_type_fuel(
#                   fuel_yaml, ship_type, random_seed)
    elif origin == 'Canada':
        fuel_flag = 1
        fuel_type = []
#         fuel_type = get_oil_type_fuel(
#                  fuel_yaml, ship_type, random_seed)
    else:
        fuel_flag = 1
        fuel_type = []
#         fuel_type = get_oil_type_fuel(
#                   fuel_yaml, ship_type, random_seed)
    
             
    return fuel_type, fuel_flag