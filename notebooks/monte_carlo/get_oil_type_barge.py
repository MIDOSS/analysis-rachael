import numpy 
import yaml
import pathlib
from monte_carlo_utils import get_oil_type_cargo 
from monte_carlo_utils import get_oil_type_cargo_generic_US

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

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Set 'fuel_flag'
    #
    # Fuel_flag is used to flag ship tracks with barge designation 
    # as non-oil cargo traffic with, hence, fuel-spill risk only
    # instead of combined cargo- & fuel-spill risk. 
    #
    # This flag will turn to 1 (fuel-spill risk only) when:
    # 1) Tug is not included in Casey's pre-selected data for tugs that 
    #    travel within a 1km radius of known marine oil terminal and,
    #    as a result, origin/destination has null value
    # 2) Tug is included in Casey's pre-selected data but is not 
    #    joined by our origin-destination analysis and, as a result,
    #    has null values for origin/destination. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   
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

    # get probability of non-allocated track being an oil-barge
    probability_oilcargo = \
        home/\
        master['vessel_attributes']['barge']['probability_oilcargo']

    probability_fuelonly = 1 - probability_oilcargo
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # these pairs need to be used together for "get_oil_type_cargo" 
    # (but don't yet have error-checks in place):
    # - "WA_in_yaml" and "destination"
    # - "WA_out_yaml" and "origin"
    #
    # ERROR CATCH for case of no oil transfer for given selection of 
    # yaml file, origin, and ship_type is currently to set flag to fuel
    # spill potential and not cargo spill potential
    #
    # Why? 
    #
    # Because there are lots of tugs that are not associated
    # with oil tank barges. We do our best to identify oil cargo and 
    # then need to rely on a probability of oil cargo informed by AIS
    # traffic data.
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    if origin in CAD_origin_destination:        
        if origin == 'Westridge Marine Terminal':
            if destination in CAD_origin_destination:
                oil_type = 'jet'            
            else:
                # allocate fuel based on a 'barge' from westridge 
                oil_type = get_oil_type_cargo( 
                          CAD_yaml, origin, ship_type, random_seed)
        else:
            if destination in US_origin_destination:
                # we have better information on WA fuel transfers, 
                # so I'm prioritizing this information source
                
                oil_type = get_oil_type_cargo(
                          WA_in_yaml, destination, 
                          ship_type, random_seed)
                
                # There is a possibility that barge traffic has a CAD
                # origin but the US destination is matched with no fuel
                # transport.  It's not likely; but a possibility. This 
                # is an error catch for if there is no fuel-type 
                # associated with a barge import to WA destination.
                # sum(probability) == 0 will return empty oil type
                
                # *** ERROR CATCH ***
                if not oil_type:
                    fuel_flag = 1
                    oil_type = []
                # *** END ERROR CATCH *** 
                
            elif destination == 'ESSO Nanaimo Departure Bay':
                # These are fixed to have a oil type option for all 
                # vessel types.  No error catch needed. 
                # See CAD_origin.yaml for verification.
                
                oil_type = get_oil_type_cargo(
                          CAD_yaml, destination, 
                          ship_type, random_seed)
                
            elif destination == 'Suncor Nanaimo':
                # Similar to ESSO. No error catch needed. 
                
                oil_type = get_oil_type_cargo(
                          CAD_yaml, destination, 
                          ship_type, random_seed)
                              
            else: 
                # if origin is a CAD terminal with no US oil terminal
                # destination and no destination to a better known
                # CAD terminal then just use the CAD origin allocation
                # An option here is to flag a destination of 'Pacific'
                # or 'US' and use US fuel alloction. I didn't see a 
                # compelling case for adding this complexity, so I kept
                # it simple.  Similar to ESSO, above, no error catch 
                # needed.
                
                oil_type = get_oil_type_cargo(
                          CAD_yaml, origin, ship_type, random_seed)
                
    elif origin in US_origin_destination:
        oil_type = get_oil_type_cargo(
                  WA_out_yaml, origin, ship_type, random_seed)
        
        # *** ERROR CATCH ***
        # As a result of using 2 different data sources (AIS and 
        # Ecology), there is a chance that AIS has origin from a 
        # marine terminal for which no barge transfers are recorded
        # in the DOE database.  For this unlikely but possible case, 
        # I attribute the barge in a way that is consistent with the 
        # DOE database by allocating the barge as a non-oil cargo barge
        # that will pose a fuel-oil spill risk only. 
        if not oil_type:
            fuel_flag = 1
            oil_type = []
        # *** END ERROR CATCH *** 

    elif destination in US_origin_destination:
        oil_type = get_oil_type_cargo(
                  WA_in_yaml, destination, ship_type, random_seed)
        
        # *** ERROR CATCH ***
        # Same explanation as given above, in 
        # 'elif origin in US_origin_destination'
        if not oil_type:
            fuel_flag = 1
            oil_type = []
        # *** END ERROR CATCH *** 
        
    elif destination in CAD_origin_destination:
        if destination == 'Westridge Marine Terminal':
            # Westridge doesn't receive crude for storage 
            oil_type = 'jet'
        else:
            oil_type = get_oil_type_cargo(
                      CAD_yaml, destination, ship_type, random_seed)
 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Remaining cases are those that were not connected to our list of 
    # known oil-transfer facilities.  They are vessels that are included
    # in Casey's pre-selection data (as within 1 km of oil-transfer 
    # facility) but were not within the area that Cam and identified as 
    # being related to oil-terminal traffic. The reason why we did a 
    # selection refinement is because there are many oil terminals
    # that are next to barge transfer sites for lumber, cars, etc, and 
    # with ship tracks included that are obviously related to these
    # other activities and not oil-transfer.  To handle these cases, 
    # we reviewed each site to determine the distance that would 
    # best isolate the oil traffic from this other traffic. However, 
    # any track in Casey's pre-selected data will be joined with our 
    # origin-destination script.  Tracks are not joined (and will 
    # have null values for origin/destination) if adjacent 
    # ship tracks are (a) < 2 km long, (b) over 4 hours apart, (c)
    # requiring > 80 knts to join.  The tracks that are joined 
    # but that lack details of origin-destination fall into the category 
    # ship tracks that may or may not be oil-traffic.  As such, 
    # I first use probability of oil-cargo for tank barge traffic to 
    # weight whether the ship track represents an oil-carge & fuel spill 
    # risk (fuel_flag = 0) or a fuel-spill risk only (fuel_flag = 1).
    # For the cases with fuel_flag == 0, I use origin 
    # as 'US','Pacific' or 'Canada' to specify cargo allocation 
    # NOTE: Currently Canada == US 
    # ALSO NOTE: Once the tracks that are identified as potential 
    # cargo-spill tracks (fuel_flag = 0), they will still be treated 
    # like any other tank traffic with an .8/.2 probility of 
    # cargo/fuel spill.  
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   
    # Initialize PCG-64 random number generator
    random_generator = numpy.random.default_rng(random_seed)
     
    elif origin == 'Pacific':
        fuel_flag = random_generator.choice(
                    [0 1], 
                    p = [probability_oilcargo probability_fuelonly])
        if fuel_flag:
            oil_type = []
        else:
            oil_type = get_oil_type_cargo_generic_US(
                      Pacific_yaml, ship_type, random_seed)
    elif origin == 'US':
        fuel_flag = random_generator.choice(
                    [0 1], 
                    p = [probability_oilcargo probability_fuelonly])
        if fuel_flag:
            oil_type = []
        else:
            oil_type = get_oil_type_cargo_generic_US(
                      US_yaml, ship_type, random_seed)
    elif origin == 'Canada':
        fuel_flag = random_generator.choice(
                    [0 1], 
                    p = [probability_oilcargo probability_fuelonly])
        if fuel_flag:
            oil_type = []
        
        else:
            oil_type = get_oil_type_cargo_generic_US(
                        CAD_yaml, ship_type, random_seed)  
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Remaining cases have null values for origin destination.
    # I first use probability of oil-cargo for tank barge traffic to 
    # weight whether the ship track is an oil-carge & fuel spill risk 
    # (fuel_flag = 0) or a fuel-spill risk only (fuel_flag = 1)
    # For the cases with fuel_flag == 0, I use the US_generic fuel allocation
    # to attribute fuel type, regardless of wether barge is north of the 
    # 49th parallel (i.e. Strait of Georgia) or south of the 49th parallel. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
 
    else:
        fuel_flag = 1
        oil_type = []
#         oil_type = get_oil_type_fuel(
#                   fuel_yaml, ship_type, random_seed)
    
             
    return oil_type, fuel_flag
