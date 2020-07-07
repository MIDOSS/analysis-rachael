import numpy 
import yaml
import pathlib
from monte_carlo_utils import get_oil_type_cargo 

#### Decision tree for allocating oil type to tanker traffic
# see google drawing [Tanker_Oil_Attribution](https://docs.google.com/drawings/d/1-4gl2yNNWxqXK-IOr4KNZxO-awBC-bNrjRNrt86fykU/edit) for a visual representation

def get_oil_type_tanker(master_dir,
                    master_file,
                    origin, 
                    destination, 
                    random_seed
                    ):

    ship_type = 'tanker'
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ##  Load file paths and terminal names
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
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


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # NOTE: these pairs need to be used together for "get_oil_type_cargo" (but don't yet have error-checks in place):
    # - "WA_in_yaml" and "destination"
    # - "WA_out_yaml" and "origin"
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    if origin in CAD_origin_destination:
        if origin == 'Westridge Marine Terminal':
            fuel_type = get_oil_type_cargo(CAD_yaml, origin, ship_type, random_seed)
        else:
            if destination in US_origin_destination:
                # we have better information on WA fuel transfers, so I'm prioritizing this information source
                fuel_type = get_oil_type_cargo(WA_in_yaml, destination, ship_type, random_seed)
            else:
                fuel_type = get_oil_type_cargo(CAD_yaml, origin, ship_type, random_seed)
    elif origin in US_origin_destination:  
        fuel_type = get_oil_type_cargo(WA_out_yaml, origin, ship_type, random_seed)
    elif destination in US_origin_destination:
        fuel_type = get_oil_type_cargo(WA_in_yaml, destination, ship_type, random_seed)
    elif destination in CAD_origin_destination:
        fuel_type = get_oil_type_cargo(CAD_yaml, destination, ship_type, random_seed)
    elif origin == 'Pacific':
        fuel_type = get_oil_type_cargo(Pacific_yaml, origin, ship_type, random_seed)
    elif origin == 'US':
        fuel_type = get_oil_type_cargo(US_yaml, origin, ship_type, random_seed)
    else: 
        # Currently, this is a catch for all ship tracks not allocated with origin or destination
        # It's a generic fuel attribution from the combined US import and export
        fuel_type = get_oil_type_cargo(USall_yaml, origin, ship_type, random_seed)
        
    return fuel_type