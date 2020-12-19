import pandas
import numpy

def load_sro(sro_file_wpath, variable_name=''):
    """ Load mass balance results from SOILED model .sro file
    :param str sro_file_wpath: File path and name of the .sro file to 
        read data from.
    :param str variable_name: name(s) of variable to return.  
        All variables returned if left empty
        Names of variables returned if variable_name = 'list'
    :return dataframe of data that is indexed as days since spill 
        but that also includes a datetime column.  
        Using DataFrame format makes for easy plotting:
        cols_plot = ["MEvaporation", "MDispersed"]
        ax = data[cols_plot].plot(linewidth=1.5,marker='x')
        ax.set_ylabel('mass loss')
        ax.set_xlabel('time [days]')
    
    Calling examples:
    [bunker_data] = load_sro(bunker_sro)
    [bunker_data] = load_sro(bunker_sro,["MassOil"])
    [bunker_data] = load_sro(bunker_sro,["MassOil", "VolumeOil"])
    """
    #~~~ Load data and tidy it up ~~~
    data = pandas.read_csv(sro_file_wpath, sep="\s+", skiprows=4)
    # remove first entry of NaN values
    data = data.drop([0], axis=0)
    # tidy up NaN and garbage entries at end of file
    length = len(data)
    data = data.drop([length-3, length-2, length-1, length], axis=0)
    # make time header names more user-friendly for datetime conversion
    # How do I make these times either UTC or identified as PST?
    data["datetime"] = [
        pandas.datetime(numpy.int(YY), numpy.int(MM), numpy.int(DD),
                    numpy.int(hh), numpy.int(mm), numpy.int(ss)
                   ) 
       for YY,MM,DD,hh,mm,ss in zip(
           data["YY"], data["MM"], data["DD"],
           data["hh"], data["mm"], data["ss"]
       )
    ]
    
    header = list(data.columns.values.tolist())    
    data["Seconds"] = [float(time) for time in data["Seconds"]]
    data["days_since_spill"] = [
        float(seconds)/86400 for seconds in data["Seconds"]
    ]
    
    # select specific data to return
    if variable_name:
        if "list" in variable_name:
            return header
        # first make sure that variable is in dataframe 
        # and return all data if even one variable is missing
        for name in variable_name:
            if name not in header:
                print(f'Column with {name} not in dataframe. Returning all data.')
                return data       
        variable_name.append("days_since_spill")
        data_subsample = data[variable_name].copy()
        data_subsample["datetime"] = [
            pandas.datetime(numpy.int(YY), numpy.int(MM), numpy.int(DD),
                        numpy.int(hh), numpy.int(mm), numpy.int(ss)
                       ) 
                       for YY,MM,DD,hh,mm,ss in zip(
                           data["YY"],data["MM"],data["DD"],
                           data["hh"],data["mm"],data["ss"]
                       )
        ]
        data_subsample = data_subsample.set_index("days_since_spill")
        
        return data_subsample
       
    data = data.set_index("days_since_spill")
    data.rename(columns={"Seconds":"seconds_since_spill"})
          
    return data