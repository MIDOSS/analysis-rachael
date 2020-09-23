from math import exp 
from monte_carlo_utils import make_bins, get_bin, place_into_bins, clamp
import yaml
import numpy

def get_oil_capacity( 
    oil_attribution_file,
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

        oil_attrs_file [string]: This is the output file from make_oil_attrs.yaml
        vessel_length [meters]: Can be any number representing ship length
        vessel_type [string]: tanker, atb, barge, cargo, cruise,
                              ferry, fishing, smallpass, or other
    """
    with open(oil_attribution_file) as file:
        oil_attrs = yaml.load(file, Loader=yaml.Loader)
     
    if vessel_type not in oil_attrs['categories']['all_vessels']:              
        raise ValueError(["Oops! Vessel type isn't valid." + 
           "Today's flavors are: tanker, atb, barge, cargo, cruise, " +
           "ferry, fishing, smallpass, or other.  So..." +
            "Go fish! (or try 'fishing' instead)"])

    if vessel_length < oil_attrs['vessel_attributes'][vessel_type]['min_length']:
        # set lower bound
        fuel_capacity = oil_attrs['vessel_attributes'][vessel_type]['min_fuel']
        cargo_capacity = oil_attrs['vessel_attributes'][vessel_type]['min_cargo'] if vessel_type in oil_attrs['categories']['tank_vessels'] else 0.0
        
    elif vessel_length > oil_attrs['vessel_attributes'][vessel_type]['max_length']:
        # set upper bound
        fuel_capacity = oil_attrs['vessel_attributes'][vessel_type]['max_fuel']
        cargo_capacity = oil_attrs['vessel_attributes'][vessel_type]['max_cargo'] if vessel_type in oil_attrs['categories']['tank_vessels'] else 0.0
    else:
        
        # ~~~ tankers ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        if vessel_type == "tanker":

            bins = (
                 oil_attrs['vessel_attributes']['tanker']
                ['length_bins']
            )

            if vessel_length >= max(max(bins)):
                cargo_capacity = (
                    oil_attrs['vessel_attributes']['tanker']
                    ['max_cargo'])
                fuel_capacity = (
                    oil_attrs['vessel_attributes']['tanker']
                    ['max_fuel'])

            elif vessel_length < 0:
                cargo_capacity = (
                    oil_attrs['vessel_attributes']['tanker']
                    ['min_cargo']
                )
                fuel_capacity = (
                    oil_attrs['vessel_attributes']['tanker']
                    ['min_fuel']
                )
            else:
                bin_index = get_bin(vessel_length, bins)

                cargo_capacity = (
                    oil_attrs['vessel_attributes']['tanker']
                    ['cargo_capacity'][bin_index]
                )
                fuel_capacity = (
                    oil_attrs['vessel_attributes']['tanker']
                    ['fuel_capacity'][bin_index]
                )


        # ~~~ atbs ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        elif vessel_type == "atb":

            atb_min_cargo = oil_attrs['vessel_attributes']['atb']['min_cargo']
            atb_max_cargo = oil_attrs['vessel_attributes']['atb']['max_cargo']

            if vessel_length > 50:
                # For ATB lengths > 50 m, calculate capacity from linear fit 
                C = oil_attrs['vessel_attributes']['atb']['cargo_fit_coefs']
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
                    oil_attrs['vessel_attributes']['atb']
                    ['cargo_capacity_probability']
                )
                cargo_capacity_bin_centers =  (
                    oil_attrs['vessel_attributes']['atb']
                    ['cargo_capacity_bin_centers'] 
                )
                cargo_capacity = random_generator.choice(
                    cargo_capacity_bin_centers, 
                    p = cargo_weight
                )

            # for all ATBs, estimate fuel capacity by AIS ship track weighting   
            fuel_weight = (
                oil_attrs['vessel_attributes']['atb']
                ['fuel_capacity_probability']
            )
            fuel_capacity_bin_centers =  (
                oil_attrs['vessel_attributes']['atb']
                ['fuel_capacity_bin_centers']
            )
            fuel_capacity = random_generator.choice(
                    fuel_capacity_bin_centers, 
                    p = fuel_weight
            )

        # ~~~ barges ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        elif vessel_type == "barge":

            cargo_weight = (
                oil_attrs['vessel_attributes']['barge']
                ['cargo_capacity_probability']
            )
            cargo_capacity_bin_centers =  (
                oil_attrs['vessel_attributes']['barge']
                ['cargo_capacity_bin_centers'] 
            )
            cargo_capacity = random_generator.choice(
                cargo_capacity_bin_centers, 
                p = cargo_weight
            )

            fuel_weight = (
                oil_attrs['vessel_attributes']['barge']
                ['fuel_capacity_probability']
            )
            fuel_capacity_bin_centers =  (
                oil_attrs['vessel_attributes']['barge']
                ['fuel_capacity_bin_centers']
            )
            fuel_capacity = random_generator.choice(
                    fuel_capacity_bin_centers, 
                    p = fuel_weight
            )

        ###  Fuel capacities below this line are still being evaluated ###
        # ~~~ cargo ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        elif vessel_type == "cargo":

            C =  oil_attrs['vessel_attributes']['cargo']['fuel_fit_coefs'] 
            
            fit_capacity = (
                numpy.exp(C[1])* 
                numpy.exp(C[0]*vessel_length)
            )

            cargo_capacity = 0
            
            # impose fuel capacity limits for this vessel type
            min_fuel = oil_attrs['vessel_attributes']['cargo']['min_fuel']
            max_fuel   = oil_attrs['vessel_attributes']['cargo']['max_fuel']

            fuel_capacity = clamp(
                fit_capacity, 
                min_fuel, 
                max_fuel
            )

        # ~~~ cruise ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        elif vessel_type == "cruise":

            C =  oil_attrs['vessel_attributes']['cruise']['fuel_fit_coefs'] 
            
            fit_capacity = (
                C[1] +
                C[0]*vessel_length
            )
            
            cargo_capacity = 0
            
            # impose fuel capacity limits for this vessel type
            min_fuel = oil_attrs['vessel_attributes']['cruise']['min_fuel']
            max_fuel   = oil_attrs['vessel_attributes']['cruise']['max_fuel']

            fuel_capacity = clamp(
                fit_capacity, 
                min_fuel, 
                max_fuel
            )

        # ~~~ ferry ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        elif vessel_type == "ferry":

            C =  oil_attrs['vessel_attributes']['ferry']['fuel_fit_coefs'] 
            
            fit_capacity = (
                numpy.exp(C[1])* 
                numpy.exp(C[0]*vessel_length)
            )

            cargo_capacity = 0
            
            # impose fuel capacity limits for this vessel type
            min_fuel = oil_attrs['vessel_attributes']['ferry']['min_fuel']
            max_fuel   = oil_attrs['vessel_attributes']['ferry']['max_fuel']

            fuel_capacity = clamp(
                fit_capacity, 
                min_fuel, 
                max_fuel
            )

        # ~~~ fishing ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        elif vessel_type == "fishing":

            C =  oil_attrs['vessel_attributes']['fishing']['fuel_fit_coefs'] 
            
            fit_capacity = (
                C[2] +
                C[1]*vessel_length +
                C[0]*vessel_length**2
            )

            cargo_capacity = 0
                
            # impose fuel capacity limits for this vessel type
            min_fuel = oil_attrs['vessel_attributes']['fishing']['min_fuel']
            max_fuel = oil_attrs['vessel_attributes']['fishing']['max_fuel']

            fuel_capacity = clamp(
                fit_capacity, 
                min_fuel, 
                max_fuel
            )

        # ~~~ small pass ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        elif vessel_type == "smallpass":

            C =  oil_attrs['vessel_attributes']['smallpass']['fuel_fit_coefs'] 
            
            fit_capacity = (
                numpy.exp(C[1])* 
                numpy.exp(C[0]*vessel_length)
            )

            cargo_capacity = 0
                
            # impose fuel capacity limits for this vessel type
            min_fuel = oil_attrs['vessel_attributes']['smallpass']['min_fuel']
            max_fuel = oil_attrs['vessel_attributes']['smallpass']['max_fuel']

            fuel_capacity = clamp(
                fit_capacity, 
                min_fuel, 
                max_fuel
            )

        # ~~~ other ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        elif vessel_type == "other":

            C =  oil_attrs['vessel_attributes']['other']['fuel_fit_coefs'] 
            
            fit_capacity = (
                numpy.exp(C[1])* 
                numpy.exp(C[0]*vessel_length)
            )

            cargo_capacity = 0
                
            # impose fuel capacity limits for this vessel type
            min_fuel = oil_attrs['vessel_attributes']['other']['min_fuel']
            max_fuel = oil_attrs['vessel_attributes']['other']['max_fuel']

            fuel_capacity = clamp(
                fit_capacity, 
                min_fuel, 
                max_fuel
            )
            
    return fuel_capacity, cargo_capacity
