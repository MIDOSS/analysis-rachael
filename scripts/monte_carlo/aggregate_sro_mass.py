# Copyright 2018-2020 The UBC EOAS MOAD Group
# and The University of British Columbia
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Functions for aggregating the mass values in MOHID model output .sro files using
the SOILED modeling suite, which combines SalishSeaCast, 
WW3, HRDPS and MOHID models. 

The monte carlo runs were completed on Compute Canada's supercomputer, `Graham` and this code is intended to be used on that system.  It requires initialization of a Virtual Environment.  See `/home/rmueller/projects/def-allen/rmueller/graham-python-env.txt`.

First initiate a compute node.  The following allocation is setup to support the use of dask parrallized computing. The design of Graham is to support multiple simultaneous parallel jobs of up to 1024 cores in a fully non-blocking manner.  Nodes range from having 16-64 cores (see [documentation](https://docs.computecanada.ca/wiki/Graham)). `ntasks` correspond to CPU cores, with `cpus-per-task` representing nodes.  The following setup is for 2 CPUs running 16 cores each for a total of 32 CPU cores. 
```
salloc --time=1:00:00 --ntasks=16 --cpus-per-task=2 --mem-per-cpu=1024M --account=rrg-allen
```
Activate `VENV` with:
```
module load python/3.8.2
source ~/venvs/python/bin/activate
```
Deactivate `VENV` with:
```
deactivate
```
If the `python` `VENV` is not yet setup, install it with:
```
module load python/3.8.2
python3 -m virtualenv --no-download ~/venvs/python
source ~/venvs/python/bin/activate
python3 -m pip install --no-index --upgrade pip
python3 -m pip install -r /home/rmueller/projects/def-allen/rmueller/graham-python-env.txt
```

input_yaml: file created by create_SOILED_sro_runlist.ipynb (https://github.com/MIDOSS/analysis-rachael/blob/main/notebooks/monte_carlo/create_SOILED_sro_runlist.ipynb)
output_dir: directory location for ouput yaml `SOILED_massbalance_all_{dt_string}.yaml'
"""

#import sys
#sys.path.insert(1, '../../scripts/')
import numpy 
import pandas 
from pathlib import Path
import datetime
#from midoss_utils import *
import yaml
import time
import glob
# compress helps to extract values from list based on the value in a column
# e.g. dissolution < 0.0
#from itertools import compress


oil_dict = {"akns":"ANS",
            "all":"all",
           "bunker":"Bunker-C",
           "diesel":"Diesel",
           "dilbit":"Dilbit",
           "gas":"Diesel",
           "jet":"Diesel",
           "other":"Bunker-C"}
variables = ['MEvaporated', 'MDispersed', 'MDissolved',
                 'MBio','MassOil','VolOilBeached',
                 'Density','VWaterContent','MWaterContent']
def aggregate_sro_mass_all(file_paths, output_dir):

    # For debugging purposes: Create count dictionary of files opened by oil type
    count = {}
    for oil in ["Bunker-C", "Diesel", "Dilbit", "ANS", "all"]:
        count[oil]=0
    # For debugging purposts: Create list of files with negative dissolution values
    diss_files = []
    # list of variables to save from .sro file
    # variables = ['MEvaporated', 'MDispersed', 'MDissolved',
    #              'MBio','MassOil','VolOilBeached',
    #              'Density','VWaterContent','MWaterContent']
    # initialize dictionary for cataloguing all output 
    all_output={}
    all_output['diss_bool'] = []
    all_output['oil_type']=[]
    all_output['month'] = []
    all_output['days_since_spill']=[]
    all_output['MBeached']=[]
    for var in variables:
        all_output[var]=[]

    ### Save mass balance information from last time step for oil categories
    # - `count`: dictionay with number of entries per grouping ("Bunker-C", "Diesel", "Dilbit", "ANS", "all")
    # - `all_output`: dictionary of mass balance categories and other information for all oil types
    # - `output`: dictionary of mass balance categorized by oil types

    with open(file_paths) as file:
        sro_files = yaml.safe_load(file)
    # load mass balance from .sro files for each oil type
    for fnum,file in enumerate(sro_files["all"]):               
        sro_file = sro_files["all"][fnum]
        # ~~~ Get oil type from Lagrangian file ~~~
        sro_directory = '/'.join(sro_file.split('/')[:-1])
        Lagrangian_fname = glob.glob(sro_directory + '/Lagrangian*')[0].split('/')[-1]
        oilname = Lagrangian_fname.split('_')[1].split('-')[0]
        # ~~~ Load data and tidy it up ~~~
        data = pandas.read_csv(sro_file, sep="\s+", skiprows=4)
        # remove first entry of NaN values
        data = data.drop([0], axis=0)
        length = len(data)
        # Make sure there is data in the file
        if length>4:
            # Add oil type to list of saved attributes
            all_output["oil_type"].append(oilname)
            # tidy up NaN and garbage entries at end of file
            data = data.drop([length-3, length-2, length-1, length], axis=0)
            data_last = data[-1:]
            # Save files with negative Dissolution 
            if (data_last["MDissolved"].item() < 0):
                diss_files.append(sro_file)
                all_output["diss_bool"].append(True)
            else:
                all_output["diss_bool"].append(False)
            # Count files to help debug
            count["all"]+=1
            all_output["month"].append(int(data_last["MM"].item()))
            all_output["days_since_spill"].append(float(data_last["Seconds"])/86400)
            # Catalogue last value for each, selected variable
            for var in variables:
                all_output[var].append(data_last[var].item())
            # calculate MBeached
            all_output["MBeached"].append(
                (data_last["VolOilBeached"]*data_last["Density"]/
                 (1-data_last["VWaterContent"])*
                 (1-data_last["MWaterContent"])
                ).item()
            )           
        else:
            print(sro_file)
            continue
    # write filenames to .yaml with timestamp in filename
    now = datetime.datetime.now()
    dt_string = now.strftime("%d%m%Y_%H:%M:%S")
    out_f_all = output_dir/f'SOILED_massbalance_all_{dt_string}.yaml'
    with open(out_f_all, 'w') as output_yaml:
        documents = yaml.safe_dump(all_output, output_yaml)
    diss_out = output_dir/'files_with_negative_dissolution.yaml'
    # save dictionary to file
    with open(diss_out, 'w') as output_yaml:
        documents = yaml.safe_dump(diss_files, output_yaml)
    # return output
    return output_yaml

def aggregate_sro_mass_byoil(file_paths, output_dir):
    """
        Function for aggregating the mass values in MOHID model output

        input_yaml: file created by create_SOILED_sro_runlist.ipynb (https://github.com/MIDOSS/analysis-rachael/blob/main/notebooks/monte_carlo/create_SOILED_sro_runlist.ipynb)

        output_dir: directory location for ouput yaml `SOILED_massbalance_byoil_{dt_string}.yaml'

    """
    # list of variables to save from .sro file
    # variables = ['MEvaporated', 'MDispersed', 'MDissolved',
    #              'MBio','MassOil','VolOilBeached',
    #              'Density','VWaterContent','MWaterContent']
    # initialize dictionary for cataloguing output by oil types
    output = {}
    for oil in ["Bunker-C", "Diesel", "Dilbit", "ANS"]:
        output[oil]={}
        output[oil]['month']=[]
        output[oil]['days_since_spill']=[]
        output[oil]['MBeached']=[]
        output[oil]['MInitial']=[]
        for var in variables:
                output[oil][var]=[]
    count = {}
    for oil in ["Bunker-C", "Diesel", "Dilbit", "ANS", "all"]:
        count[oil]=0
        
    # open .yaml file with list of file paths
    with open(file_paths) as file:
        sro_files = yaml.safe_load(file)
    # loop through oils and catalogue data
    iter_list = [oiltype for oiltype in [*sro_files] if oiltype != 'all']
    for oil in iter_list:
        print(oil)  
        # load mass balance from .sro files for each oil type
        for fnum,file in enumerate(sro_files[oil]):               
            sro_file = sro_files[oil][fnum]
             #~~~ Load data and tidy it up ~~~
            data = pandas.read_csv(sro_file, sep="\s+", skiprows=4)
            # remove first entry of NaN values
            data = data.drop([0], axis=0)
            length = len(data)
            # Make sure there is data in the file
            if length>4:
                # tidy up NaN and garbage entries at end of file
                data = data.drop([length-3, length-2, length-1, length], axis=0)
                data_last = data[-1:]
                # Count files to help debug
                count[oil_dict[oil]]+=1
                output[oil_dict[oil]]['month'].append(int(data_last["MM"].item()))
                output[oil_dict[oil]]['days_since_spill'].append(float(data_last["Seconds"])/86400)
                # Catalogue last value for each, selected variable
                for var in variables:
                    output[oil_dict[oil]][var].append(data_last[var].item())
                # Save initial spill mass. (Row indexing starts at 1 in these files.) 
                # MassOil = Floating Oil
                # I checked and verified that first value is total spilled mass
                MInitial = data['MassOil'][1].item()
                output[oil_dict[oil]]['MInitial'].append(MInitial)
                # calculate MBeached
                output[oil_dict[oil]]['MBeached'].append(
                    (data_last['VolOilBeached']*data_last['Density']/
                     (1-data_last['VWaterContent'])*
                     (1-data_last['MWaterContent'])).item()
                )
            else:
                print(sro_file)
                continue
    for oil in iter_list: 
        print(f"{oil}: {len(output[oil_dict[oil]]['MBeached'])}")      
    # write filenames to .yaml with timestamp in filename
    now = datetime.datetime.now()
    dt_string = now.strftime("%d%m%Y_%H:%M:%S")
    out_f_oils = output_dir/f'SOILED_massbalance_byoil_{dt_string}.yaml'
    with open(out_f_oils, 'w') as output_yaml:
        documents = yaml.safe_dump(output, output_yaml)
    return output