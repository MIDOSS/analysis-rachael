from math import exp 

def get_oil_capacity( vessel_length, 
                      vessel_type
                    ):
    
    if vessel_type == "tanker":
    
        fuel_capacity = ( 111047 * 
                         exp( 9.32e-03 * vessel_length )) / 264.172

        if vessel_length < 220:  

            tank_capacity = 301 * vessel_length        

        else:

            tank_capacity = 465 * vessel_length

    elif vessel_type == "atb" or vessel_type == "barge":

        fuel_capacity = (10438 + 
                         5182 * vessel_length + 241 * vessel_length**2) / 264.172
        tank_capacity = (232021 * 
                         exp( 0.0246 * vessel_length )) / 264.172

    elif vessel_type == "cargo":

        fuel_capacity = ( 111047 * 
                         exp( 9.32e-03 * vessel_length )) / 264.172
        tank_capacity = 0

    elif vessel_type == "cruise":

        fuel_capacity = ( 58271 * 
                         exp( 9.97e-03 * vessel_length )) / 264.172
        tank_capacity = 0

    elif vessel_type == "ferry":

        fuel_capacity = ( 1381 * 
                         exp( 0.0371 * vessel_length )) / 264.172
        tank_capacity = 0

    elif vessel_type == "fishing":

        fuel_capacity = ( 223 * 
                         exp( 0.598 * vessel_length )) / 264.172
        tank_capacity = 0

    elif vessel_type == "smallpass" or vessel_type == "other":

        fuel_capacity = ( 8.05 * vessel_length + 158 ) / 264.172
        tank_capacity = 0
    else:

        print(["Oops! Vessel type isn't valid." + 
           "Today's flavors are: tanker, atb, barge, cargo, cruise, " +
           "ferry, fishing, smallpass, or other.  Go fish!  (or try 'fishing' instead)"])

        
    fuel_in_liters = 1e3 * fuel_capacity
    tank_in_liters = 1e3 * tank_capacity

    return fuel_in_liters, tank_in_liters
