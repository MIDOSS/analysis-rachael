from math import exp 
from monte_carlo_utils import make_bins, get_bin, place_into_bins, clamp
import yaml

def get_oil_capacity( 
    master_file,
    vessel_length, 
    vessel_type,
    random_generator
):
    """ Returns fuel_capacity [liters] and cargo_capacity [liters] based on vessel
        length and type, with the exception of ATBs and barges.  Tank_capacity 
        is estimated by length for ATBs > 50 m only.  For all other ATB and barge 
        traffic, as well as fuel capacity for ATBs > 50 m, both fuel and cargo 
        capacities are estimated by weighted values based on AIS data for ATB
        ship traffic for which tugs and barges were married by a comination of 
        web research and AIS analysis. We assume that the fuel and cargo 
        capacities for non-ATB tug and tank barges is well represented by the 
        ATB data. 

        master_file [string]: This is the output file from make_master.yaml
        vessel_length [meters]: Can be any number representing ship length
        vessel_type [string]: tanker, atb, barge, cargo, cruise,
                              ferry, fishing, smallpass, or other
    """
    with open(master_file) as file:
        master = yaml.load(file, Loader=yaml.Loader)
     
    if vessel_type not in master['categories']['all_vessels']:              
        raise ValueError(["Oops! Vessel type isn't valid." + 
           "Today's flavors are: tanker, atb, barge, cargo, cruise, " +
           "ferry, fishing, smallpass, or other.  So..." +
            "Go fish! (or try 'fishing' instead)"])

    if vessel_length < 0:
        fuel_capacity = master['vessel_attributes'][vessel_type]['min_fuel']
        cargo_capacity = master['vessel_attributes'][vessel_type]['min_cargo']
    
    else:
        
        # ~~~ tankers ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        if vessel_type == "tanker":

            bins = (
                 master['vessel_attributes']['tanker']
                ['length_bins']
            )

            if vessel_length >= max(max(bins)):
                cargo_capacity = (
                    master['vessel_attributes']['tanker']
                    ['max_cargo'])
                fuel_capacity = (
                    master['vessel_attributes']['tanker']
                    ['max_fuel'])

            elif vessel_length < 0:
                cargo_capacity = (
                    master['vessel_attributes']['tanker']
                    ['min_cargo']
                )
                fuel_capacity = (
                    master['vessel_attributes']['tanker']
                    ['min_fuel']
                )
            else:
                bin_index = get_bin(vessel_length, bins)

                cargo_capacity = (
                    master['vessel_attributes']['tanker']
                    ['cargo_capacity'][bin_index]
                )
                fuel_capacity = (
                    master['vessel_attributes']['tanker']
                    ['fuel_capacity'][bin_index]
                )


        # ~~~ atbs ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        elif vessel_type == "atb":

            atb_min_cargo = master['vessel_attributes']['atb']['min_cargo']
            atb_max_cargo = master['vessel_attributes']['atb']['max_cargo']

            if vessel_length > 50:
                # For ATB lengths > 50 m, calculate capacity from linear fit 
                C = master['vessel_attributes']['atb']['cargo_fit_coefs']
                fit_capacity = ( 
                    C[1] + 
                    C[0]*vessel_length 
                )
                # impose thresholds to yield output capacity
                cargo_capacity = clamp(
                    fit_capacity, 
                    atb_min_cargo, 
                    atb_max_cargo
                )
            else:
                # Use cargo capacity weights by AIS ship track data
                # for lengths < 50 m 
                cargo_weight = (
                    master['vessel_attributes']['atb']
                    ['cargo_capacity_probability']
                )
                cargo_capacity_bin_centers =  (
                    master['vessel_attributes']['atb']
                    ['cargo_capacity_bin_centers'] 
                )
                cargo_capacity = random_generator.choice(
                    cargo_capacity_bin_centers, 
                    p = cargo_weight
                )

            # for all ATBs, estimate fuel capacity by AIS ship track weighting   
            fuel_weight = (
                master['vessel_attributes']['atb']
                ['fuel_capacity_probability']
            )
            fuel_capacity_bin_centers =  (
                master['vessel_attributes']['atb']
                ['fuel_capacity_bin_centers']
            )
            fuel_capacity = random_generator.choice(
                    fuel_capacity_bin_centers, 
                    p = fuel_weight
            )

        # ~~~ barges ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        elif vessel_type == "barge":

            cargo_weight = (
                master['vessel_attributes']['barge']
                ['cargo_capacity_probability']
            )
            cargo_capacity_bin_centers =  (
                master['vessel_attributes']['barge']
                ['cargo_capacity_bin_centers'] 
            )
            cargo_capacity = random_generator.choice(
                cargo_capacity_bin_centers, 
                p = cargo_weight
            )

            fuel_weight = (
                master['vessel_attributes']['barge']
                ['fuel_capacity_probability']
            )
            fuel_capacity_bin_centers =  (
                master['vessel_attributes']['barge']
                ['fuel_capacity_bin_centers']
            )
            fuel_capacity = random_generator.choice(
                    fuel_capacity_bin_centers, 
                    p = fuel_weight
            )

        ###  Fuel capacities below this line are still being evaluated ###
        # ~~~ cargo ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        elif vessel_type == "cargo":

            fuel_capacity = 1e3 * ( 111047 * 
                             exp( 9.32e-03 * vessel_length )) / 264.172
            cargo_capacity = 0
            
            # impose fuel capacity limits for this vessel type
            min_fuel = master['vessel_attributes']['cargo']['min_fuel']
            max_fuel   = master['vessel_attributes']['cargo']['max_fuel']

            fuel_capacity = clamp(
                fuel_capacity, 
                min_fuel, 
                max_fuel
            )

        # ~~~ cruise ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        elif vessel_type == "cruise":

            fuel_capacity =1e3 *  ( 58271 * 
                             exp( 9.97e-03 * vessel_length )) / 264.172
            cargo_capacity = 0
            
            # impose fuel capacity limits for this vessel type
            min_fuel = master['vessel_attributes']['cruise']['min_fuel']
            max_fuel   = master['vessel_attributes']['cruise']['max_fuel']

            fuel_capacity = clamp(
                fuel_capacity, 
                min_fuel, 
                max_fuel
            )

        # ~~~ ferry ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        elif vessel_type == "ferry":

            fuel_capacity = 1e3 * ( 1381 * 
                             exp( 0.0371 * vessel_length )) / 264.172
            cargo_capacity = 0
            
            # impose fuel capacity limits for this vessel type
            min_fuel = master['vessel_attributes']['ferry']['min_fuel']
            max_fuel   = master['vessel_attributes']['ferry']['max_fuel']

            fuel_capacity = clamp(
                fuel_capacity, 
                min_fuel, 
                max_fuel
            )

        # ~~~ fishing ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        elif vessel_type == "fishing":

            fuel_capacity = 1e3 * ( 223 * 
                             exp( 0.598 * vessel_length )) / 264.172
            cargo_capacity = 0
                
            # impose fuel capacity limits for this vessel type
            min_fuel = master['vessel_attributes']['fishing']['min_fuel']
            max_fuel = master['vessel_attributes']['fishing']['max_fuel']

            fuel_capacity = clamp(
                fuel_capacity, 
                min_fuel, 
                max_fuel
            )

        # ~~~ small pass or other ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        elif vessel_type == "smallpass" or vessel_type == "other":

            fuel_capacity = 1e3 * ( 8.05 * vessel_length + 158 ) / 264.172
            cargo_capacity = 0
                
            # impose fuel capacity limits for this vessel type
            min_fuel = master['vessel_attributes']['smallpass']['min_fuel']
            max_fuel = master['vessel_attributes']['smallpass']['max_fuel']

            fuel_capacity = clamp(
                fuel_capacity, 
                min_fuel, 
                max_fuel
            )

    return fuel_capacity, cargo_capacity
