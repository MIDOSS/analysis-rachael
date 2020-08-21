import numpy 
import yaml
import pathlib
from monte_carlo_utils import get_oil_type_cargo 
from monte_carlo_utils import get_oil_type_cargo_generic_US


#### Decision tree for allocating oil type to tanker traffic
# see google drawing [Tanker_Oil_Attribution](https://docs.google.com/drawings/d/1-4gl2yNNWxqXK-IOr4KNZxO-awBC-bNrjRNrt86fykU/edit) for a visual representation

def get_oil_type_tanker(
    master_file,
    origin, 
    destination, 
    random_generator
):

    ship_type = 'tanker'
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ##  Load file paths and terminal names
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    with open(master_file) as file:
        master = yaml.load(file, Loader=yaml.Loader)
        # master = yaml.safe_load(file)

    # Assign US and CAD origin/destinations from master file
    CAD_origin_destination = master['categories']\
        ['CAD_origin_destination']
    US_origin_destination = master['categories']\
        ['US_origin_destination']

    # Get file paths to fuel-type yaml files
    # US_origin is for US as origin
    # US_combined represents the combined import and export of fuel
    CAD_yaml     = master['files']['CAD_origin']
    WA_in_yaml   = master['files']['WA_destination']
    WA_out_yaml  = master['files']['WA_origin']
    US_yaml      = master['files']['US_origin']
    USall_yaml   = master['files']['US_combined']
    Pacific_yaml = master['files']['Pacific_origin']


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # NOTE: these pairs need to be used together for 
    # "get_oil_type_cargo" (but don't yet have error-checks in place):
    # - "WA_in_yaml" and "destination"
    # - "WA_out_yaml" and "origin"
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    if origin in CAD_origin_destination:
        if origin == 'Westridge Marine Terminal':
            oil_type = get_oil_type_cargo(
                CAD_yaml, origin, 
                ship_type, random_generator
            )
        else:
            if destination in US_origin_destination:
                # we have better information on WA fuel transfers, 
                #so I'm prioritizing this information source
                oil_type = get_oil_type_cargo(
                    WA_in_yaml, destination, 
                    ship_type, random_generator
                )
            else:
                oil_type = get_oil_type_cargo(
                    CAD_yaml, origin, 
                    ship_type, random_generator
                )
    elif origin in US_origin_destination:  
        oil_type = get_oil_type_cargo(
            WA_out_yaml, origin, 
            ship_type, random_generator
        )
    elif destination in US_origin_destination:
        oil_type = get_oil_type_cargo(
            WA_in_yaml, destination, 
            ship_type, random_generator
        )
    elif destination in CAD_origin_destination:
        oil_type = get_oil_type_cargo(
            CAD_yaml, destination, 
            ship_type, random_generator
        )
    elif origin == 'Pacific':
        oil_type = get_oil_type_cargo_generic_US(
            Pacific_yaml,  
            ship_type, random_generator
        )
    elif origin == 'US':
        oil_type = get_oil_type_cargo_generic_US(
            US_yaml,  
            ship_type, random_generator
        )
    else: 
        # Currently, this is a catch for all ship tracks not allocated with origin or destination
        # It's a generic fuel attribution from the combined US import and export
        oil_type = get_oil_type_cargo_generic_US(
            USall_yaml, 
            ship_type, random_generator
        )
        
    return oil_type
