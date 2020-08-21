import numpy 
import yaml
import pathlib
from monte_carlo_utils import get_oil_type_cargo 
from monte_carlo_utils import get_oil_type_cargo_generic_US

#### Decision tree for allocating oil type to atb traffic
# see google drawing [atb oil attribution](https://docs.google.com/drawings/d/1Aigd2wccnl6-pQVo4KLN0xq1is6poD9z5JnFVb-fduE/edit)
#

def get_oil_type_atb(
    master_file,
    origin, 
    destination, 
    random_generator
):

    ship_type = 'atb'
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Unlike traditional tank barges, the vessels with 'atb'
    # designation are known oil-cargo vessels.  We used three 
    # different data sources to verify: AIS, Dept of Ecology's 
    # fuel transfer records and Charlie Costanzo's ATB list. 
    # details of traffic can be seen in this google spreadsheet:
    # https://docs.google.com/spreadsheets/d/1dlT0JydkFG43LorqgtHle5IN6caRYjf_3qLrUYqANDY/edit#gid=1593104354
    #
    # Because of this pre-identification and selection method,
    # we can assume that all atbs are oil-cargo atbs and that 
    # the absence of origin-destination information is due to 
    # issues in linking ship tracks and not ambiguity about 
    # whether traffic is oil-cargo traffic.
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ##  Load file paths and terminal names
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    with open(f'{master_dir}{master_file}') as file:
        master = yaml.safe_load(file)

    # Assign US and CAD origin/destinations from master file
    CAD_origin_destination = master['categories']\
        ['CAD_origin_destination']
    US_origin_destination = master['categories']\
        ['US_origin_destination']

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
    # NOTE: these pairs need to be used together for "get_oil_type_cargo" 
    #   (but don't yet have error-checks in place):
    # - "WA_in_yaml" and "destination"
    # - "WA_out_yaml" and "origin"
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    if origin in CAD_origin_destination:
        if origin == 'Westridge Marine Terminal':
            if destination == 'U.S. Oil & Refining':
                oil_type = get_oil_type_cargo(
                    CAD_yaml, origin, 
                    ship_type, random_generator
                )
            elif destination in US_origin_destination:
                oil_type = get_oil_type_cargo(
                    CAD_yaml, origin, 
                    ship_type, random_generator
                )
            elif destination in CAD_origin_destination:
                # assume export within CAD is from Jet fuel storage tanks 
                # as there is a pipeline to Parkland for crude oil
                oil_type = 'jet'
            else:
                oil_type = get_oil_type_cargo(
                    CAD_yaml, origin, 
                    ship_type, random_generator
                )
        else:
            if destination in US_origin_destination:
                # we have better information on WA fuel transfers, 
                # so I prioritize this information source
                oil_type = get_oil_type_cargo(
                    WA_in_yaml, destination, 
                    ship_type, random_generator
                )
            elif destination == 'ESSO Nanaimo Departure Bay':
                oil_type = get_oil_type_cargo(
                    CAD_yaml, destination, 
                    ship_type, random_generator
                )
                    
            elif destination == 'Suncor Nanaimo':
                oil_type = get_oil_type_cargo(
                    CAD_yaml, destination, 
                    ship_type, random_generator
                )
            else: 
                oil_type = get_oil_type_cargo(
                    CAD_yaml, origin, 
                    ship_type, random_generator
                )
    elif origin in US_origin_destination:
        if destination == 'Westridge Marine Terminal':
            # Westridge stores jet fuel from US for re-distribution 
            oil_type = 'jet'
        else:
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
        if destination == 'Westridge Marine Terminal':
            # Westridge doesn't receive crude for storage 
            oil_type = 'jet'
        else:
            oil_type = get_oil_type_cargo(
                CAD_yaml, destination, 
                ship_type, random_generator
            )
    elif origin == 'Pacific':
        oil_type = get_oil_type_cargo(
            Pacific_yaml, origin, 
            ship_type, random_generator
        )
    elif origin == 'US':
        oil_type = get_oil_type_cargo(
            US_yaml, origin, 
            ship_type, random_generator
        )
    else:
        # For all other traffic, use a generic fuel attribution from the combined
        # US import and export
        oil_type = get_oil_type_cargo_generic_US(
            USall_yaml, 
            ship_type, 
            random_generator
        )
        
        
    return oil_type
