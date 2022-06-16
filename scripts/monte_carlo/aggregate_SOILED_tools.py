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
"""Functions for aggregating the model output of the 
Monte Carlo output from the SOILED modeling suite, which combines SalishSeaCast, 
WW3, HRDPS and MOHID models. 

The monte carlo runs were completed on Compute Canada's supercomputer, `Graham` and this code is intended to be used on that system.  It requires initialization of a Virtual Environment.  See `/home/rmueller/projects/def-allen/rmueller/graham-python-env.txt`.

First initiate a compute node.  The following allocation is setup for light computing with 2 CPUs and 1 CPU core per CPU. 
```
salloc --time=1:00:00 --ntasks=1 --cpus-per-task=2 --mem-per-cpu=1024M --account=rrg-allen
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
"""
import os
import pathlib
import yaml
import numpy
import xarray
import h5netcdf
from datetime import datetime
from glob import glob
import time


def get_SOILED_netcdf_filenames(
    results_dir="/scratch/dlatorne/MIDOSS/runs/monte-carlo", 
    runset_tag="*_near-BP_spill-hr*", 
    output_dir ="/scratch/rmueller/MIDOSS/Results"):
    """Get lists of filepaths and filenames for netcdf files of model output, 
    grouped by oil types. NOTE: jet and gas are run as diesel; other is run 
    as bunker.  
    
    :param str results_dir: File path for root directory of run sets. 
    On Graham, the filepath is `/scratch/dlatorne/MIDOSS/runs/monte-carlo`
    
    :param str output_dir: File path for storing MOHID_results_locations_{date}.yaml,
    which contains file paths for completed runs, sorted by oil type.  
    
    :return: Dataframe of file paths and names, sorted by oil types, namely: 
    akns, bunker, dilbit, jet, diesel, gas and other.  Note: jet and gas are 
    run as diesel; other is run as bunker.  
    :rtype: :py:class:`pandas.DataFrame`
    """
    oil_types = [
        'akns', 
        'bunker', 
        'dilbit', 
        'jet', 
        'diesel', 
        'gas', 
        'other'
    ]
    # get list of runsets
    runsets = sorted(glob(os.path.join(results_dir,runset_tag)))
    # get list of runs within each runset
    runs = []
    for runset in runsets:
        runs.extend(sorted(
            glob(os.path.join(runset,'results',runset_tag)))[:])        
    # get complete list of netcdf files
    netcdf_files = []
    for run in runs:
        netcdf_files.extend(sorted(
            glob(os.path.join(run,'Lagrangian*.nc')))[:])
    # sort filenames by oil type.  
    file_boolean = {}
    files = {}
    files['all'] = []
    for oil in oil_types:
        file_boolean[oil] = [oil in file for file in netcdf_files]
        files[oil]=[file for i,file in enumerate(netcdf_files) \
            if file_boolean[oil][i]]
        files['all'].extend(files[oil])
    files['all'].sort()
    # write filenames to .yaml with timestamp in filename
    now = datetime.now()
    dt_string = now.strftime("%d%m%Y_%H:%M:%S")
    out_f = output_dir+f'/MOHID_results_locations_{dt_string}.yaml'
    with open(out_f, 'w') as output_yaml:
        documents = yaml.safe_dump(files, output_yaml)
    
    return files

