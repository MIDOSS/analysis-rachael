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

First initiate a compute node.  The performance of this code isn't significantly enhanced by more computing power than the following.
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
import sys
import pathlib
import yaml
import numpy
import xarray
import h5netcdf
from datetime import datetime
from glob import glob
import time
import dask


def aggregate_SOILED_beaching(run_list, beach_threshold=15e-3, time_threshold=0.2):
    """I still need to add a header here :-) """
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # dimensions, constants, and dictionaries
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    nruns=len(run_list)
    ny,nx=896, 396
    x, y=numpy.arange(0,nx), numpy.arange(0,ny) 
    # define time thresholds
    one_day=numpy.timedelta64(24,'h')
    three_days=numpy.timedelta64(48,'h')
    seven_days=numpy.timedelta64(168,'h')
    # conversion constants
    nanosecond_to_hour = 1e-9/3600
    # Dictionary for organizing run information
    files=[]
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Create xarrays for aggregating beaching presence
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    
    dims=('nspills','grid_y','grid_x')
    MOHID_In=xarray.Dataset(
        data_vars=dict(
            BeachTime=(dims, numpy.zeros((nruns,ny,nx))),
            BeachVolume=(dims, numpy.zeros((nruns,ny,nx),dtype=float)),
            BeachPresence=(dims, numpy.zeros((nruns,ny,nx),dtype=int)),
            BeachPresence_24h=(dims, numpy.zeros((nruns,ny,nx),dtype=int)),
            BeachPresence_24h_to_72h=(dims, numpy.zeros((nruns,ny,nx),dtype=int)),
            BeachPresence_72h_to_168h=(dims, numpy.zeros((nruns,ny,nx),dtype=int))),
        coords=dict(
            grid_y=range(ny),
            grid_x=range(nx))
    )
    dims=('grid_y','grid_x')
    BeachingOut=xarray.Dataset(
        data_vars=dict(
            MinBeachTime=(dims, numpy.zeros((ny,nx)),
               {"units":"hours",
                "description":("Earliest beaching arrival time at "
                    "locations where beached oil is above "
                    "BeachVolume_threshold and beaching time is greater "
                    f"than {time_threshold} hr (~1 min for 0.02 default)")}), 
            MeanBeachTime=(dims, numpy.zeros((ny,nx)),
                {"units":"hours",
                "description":("The mean across runs of the earliest beaching "
                    " arrival time at locations where beached oil is above "
                    "BeachVolume_threshold")}),
            TotalBeachVolume=(dims, numpy.zeros((ny,nx),dtype=float),
                {"units":"m3/gridcell",
                "description":("Total beaching volume summed over all runs where" 
                    "volume>BeachVolume_threshold in any given, individual "
                    "run")}),
            BeachPresence=(dims, numpy.zeros((ny,nx),dtype=int),
                {"units":"none",
                "description":("An integer value 0<n<=N_spills representing the "
                    "number out of N_spills where oil presence on beaches is "
                    "above the BeachVolume_threshold")}),
            BeachPresence_24h=(dims, numpy.zeros((ny,nx),dtype=int),
                {"units":"none",
                 "description":("An integer value 0<n<=N_spills representing the "
                    " number of N_spills where oil presence on beaches is above "
                    "the BeachVolume_threshold and within the first 24 hours "
                    "of spill")}),
            BeachPresence_24h_to_72h=(dims, numpy.zeros((ny,nx),dtype=int),
                {"units":"none",
                 "description":("An integer value 0<n<=N_spills representing the "
                    "number of N_spills where oil presence on beaches is above "
                    "the BeachVolume_threshold and within [24,72) hours "
                    "after spill")}),
            BeachPresence_72h_to_168h=(dims, numpy.zeros((ny,nx),dtype=int),
                {"units":"none",
                 "description":("An integer value 0<n<=N_spills representing the "
                    "number of N_spills where oil presence on beaches is above "
                    "the BeachVolume_threshold and within [72,168) hours "
                    "after spill")})),
        coords=dict(
            grid_y=range(ny),
            grid_x=range(nx)), 
        attrs=dict(
            BeachVolume_threshold=beach_threshold,
            BeachVolume_threshold_units="m3",
        )
    )
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # loop through runs and aggregate beaching information
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    for run in range(nruns):
        input_file=run_list[run]
        if os.path.isfile(input_file):
            files.append(input_file.split('/')[-1])
            with xarray.open_dataset(input_file) as ds:
                #~~~ Beaching ~~~
                dt=ds.Beaching_Time-ds.Beaching_Time.min()
                # Beaching time (converted from ns to hours)
                MOHID_In.BeachTime[run,:,:]=dt*nanosecond_to_hour
                # Set time to NaT where volume is below threshold 
                MOHID_In['BeachTime']=MOHID_In.BeachTime.where(
                    ds.Beaching_Volume>beach_threshold)
                # Save volume over threshold 
                MOHID_In.BeachVolume[run,:,:]=ds.Beaching_Volume.where(
                    ds.Beaching_Volume>beach_threshold)
                # Beaching presence masks
                dtmask=xarray.DataArray(
                    data=numpy.ones_like(ds.Beaching_Time, dtype=int),
                    coords=ds.Beaching_Time.coords,
                    dims=ds.Beaching_Time.dims,
                )       
                # Presence above threshold
                MOHID_In.BeachPresence[run,:,:]=dtmask.where(
                    ds.Beaching_Volume>beach_threshold)
                MOHID_In.BeachPresence_24h[run,:,:]=(
                    MOHID_In.BeachPresence[run,:,:].where(dt<one_day)) 
                MOHID_In.BeachPresence_24h_to_72h[run,:,:]=(
                    MOHID_In.BeachPresence[run,:,:].where(
                    numpy.logical_and(dt>=one_day, dt<three_days))
                )
                MOHID_In.BeachPresence_72h_to_168h[run,:,:]=(
                    MOHID_In.BeachPresence[run,:,:].where(
                    numpy.logical_and(dt>=three_days, dt<seven_days))
                )
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Flatten MOHID output into 2D arrays by 
    # taking minimum of spill values or adding across spill values 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    nspills=len(files)
    # Beaching xarray for output netcdf
    # By default, .sum() only skips missing values for float dtypes 
    # but it seems to function for timedelta64[ns]
    # keeping `skipna=True` in code for clarity purposes only
    BeachingOut.attrs['Filenames']=files
    BeachingOut.attrs['N_spills']=nspills
    BeachingOut['MinBeachTime']=MOHID_In['BeachTime'].where(
        MOHID_In.BeachTime>time_threshold).min(dim='nspills', skipna=True)
    BeachingOut['MeanBeachTime']=MOHID_In['BeachTime'].mean(dim='nspills', skipna=True)
    BeachingOut['TotalBeachVolume']=MOHID_In['BeachVolume'].sum(
        dim='nspills', skipna=True)
    BeachingOut['BeachPresence']=MOHID_In['BeachPresence'].sum(
        dim='nspills', skipna=True)
    BeachingOut['BeachPresence_24h']=MOHID_In['BeachPresence_24h'].sum(
        dim='nspills', skipna=True)
    BeachingOut['BeachPresence_24h_to_72h']=MOHID_In['BeachPresence_24h_to_72h'].sum(
        dim='nspills', skipna=True)
    BeachingOut['BeachPresence_72h_to_168h']=MOHID_In['BeachPresence_72h_to_168h'].sum(
        dim='nspills', skipna=True)
    
    return BeachingOut

def aggregate_SOILED_surface(run_list, surface_threshold=3e-3, time_threshold=0.2):
    """I still need to add a header here :-) """
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # dimensions, constants, and dictionaries
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    nruns=len(run_list)
    ny,nx=896, 396
    x, y=numpy.arange(0,nx), numpy.arange(0,ny) 
    # define time thresholds
    one_day=numpy.timedelta64(24,'h')
    three_days=numpy.timedelta64(48,'h')
    seven_days=numpy.timedelta64(168,'h')
    # conversion constants
    nanosecond_to_hour = 1e-9/3600
    # Dictionary for organizing run information
    files=[]
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Create xarrays for aggregating surface presence
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    
    dims=('nspills','grid_y','grid_x')
    MOHID_In=xarray.Dataset(
        data_vars=dict(
            SurfacePresence=(dims, numpy.zeros((nruns,ny,nx),dtype=int)),
            SurfaceVolumeSum=(dims, numpy.zeros((nruns,ny,nx),dtype=float)),
            SurfaceVolumeMax=(dims, numpy.zeros((nruns,ny,nx),dtype=float)),
            SurfaceVolumeSum_24h=(dims, numpy.zeros((nruns,ny,nx),dtype=float)),
            SurfaceVolumeSum_24h_to_72h=(dims, numpy.zeros((nruns,ny,nx),dtype=float)),
            SurfaceVolumeSum_72h_to_168h=(dims, numpy.zeros((nruns,ny,nx),dtype=float))),
        coords=dict(
            grid_y=range(ny),
            grid_x=range(nx))
         )
    dims=('grid_y','grid_x')
    SurfaceOut=xarray.Dataset(
        data_vars=dict(
            SurfacePresence=(dims, numpy.zeros((ny,nx),dtype=int),
                {"units":"none",
                 "description":("An integer value 0<n<=N_spills representing the "
                    "number out of N_spills where oil presence is above the "
                    "SurfaceVolume_threshold")}),
            SurfaceVolume_SumSum=(dims, numpy.zeros((ny,nx),dtype=float),
                {"units":"m3",
                 "description":("Time-integrated values of the "
                    "natural log of surface volume, summed across" 
                    "different spill scenarios.")}),
            SurfaceVolume_SumSum_24h=(dims, numpy.zeros((ny,nx),dtype=float),
                {"units":"m3",
                 "description":("Time-integrated values over the first "
                    "24-hrs after spill scenario of the "
                    "natural log of surface volume, summed across" 
                    "different spill scenarios.")}),
            SurfaceVolume_SumSum_24h_to_72h=(dims, numpy.zeros((ny,nx),dtype=float),
                {"units":"m3",
                 "description":("Time-integrated values between 24 and 72 "
                    "hours after spill scenario of the "
                    "natural log of surface volume, summed across" 
                    "different spill scenarios.")}),
            SurfaceVolume_SumSum_72h_to_168h=(dims, numpy.zeros((ny,nx),dtype=float),
                {"units":"m3",
                 "description":("Time-integrated values between 72 and 168 "
                    "hours after spill scenario of the "
                    "natural log surface volume, summed across" 
                    "different spill scenarios.")}),
            SurfaceVolume_MaxSum=(dims, numpy.zeros((ny,nx),dtype=float),
                {"units":"m3",
                 "description":("Sum of the natural log surface "
                      "volume across different spills where each spill "
                      "instance is represented by the maximum value across "
                      "time of the surface spill volume.")})),
        coords=dict(
            grid_y=range(ny),
            grid_x=range(nx)),
        attrs=dict(
            SurfaceVolume_threshold=surface_threshold,
            SurfaceVolume_threshold_units="m3"),
        )
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # loop through runs and aggregate surface information
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    for run in range(nruns):
        input_file=run_list[run]
        if os.path.isfile(input_file):
            files.append(input_file.split('/')[-1])
            with xarray.open_dataset(input_file) as ds:
                initial_spill_time = ds.Oil_Arrival_Time.min()
                # Select surface volume
                vol3d=ds.OilWaterColumnOilVol_3D.isel({'grid_z': 39})
                # Identify surface presence, over threshold
                sfcmask2d=xarray.DataArray(
                    data=numpy.ones_like(ds.Oil_Arrival_Time, dtype=int),
                    coords=ds.Oil_Arrival_Time.coords,
                    dims=ds.Oil_Arrival_Time.dims,
                )
                MOHID_In.SurfacePresence[run,:,:]=sfcmask2d.where(
                    vol3d.max(dim='time',skipna=True)>surface_threshold
                )
                # Integrated surface volume over time where oiling>threshold
                MOHID_In.SurfaceVolumeSum[run,:,:]=numpy.log(
                    vol3d.where(vol3d>surface_threshold)).sum(
                    dim="time",skipna=True)
                MOHID_In.SurfaceVolumeSum_24h[run,:,:]=numpy.log(
                    vol3d.where(vol3d>surface_threshold)).loc[
                    dict(time=slice(initial_spill_time,initial_spill_time+one_day))
                    ].sum(dim="time",skipna=True)
                MOHID_In.SurfaceVolumeSum_24h_to_72h[run,:,:]=numpy.log(
                    vol3d.where(vol3d>surface_threshold)).loc[dict(time=slice(
                    initial_spill_time+one_day,initial_spill_time+three_days))
                    ].sum(dim="time",skipna=True)
                MOHID_In.SurfaceVolumeSum_72h_to_168h[run,:,:]=numpy.log(
                    vol3d.where(vol3d>surface_threshold)).loc[dict(time=slice(
                    initial_spill_time+three_days,initial_spill_time+seven_days))
                    ].sum(dim="time",skipna=True)
                # think about ln on max...
                MOHID_In.SurfaceVolumeMax[run,:,:]=numpy.log(
                    vol3d.where(vol3d>surface_threshold)).max(
                    dim="time",skipna=True)
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Flatten MOHID output into 2D arrays by 
    # taking minimum of spill values or adding across spill values 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    nspills=len(files)
    # Surface oiling xarray for output netcdf
    SurfaceOut.attrs['Filenames']=files
    SurfaceOut.attrs['N_spills']=nspills
    SurfaceOut['SurfacePresence']=MOHID_In.SurfacePresence.sum(
        dim='nspills', skipna=True) 
    SurfaceOut['SurfaceVolume_SumSum']=MOHID_In.SurfaceVolumeSum.sum(
        dim='nspills', skipna=True)    
    SurfaceOut['SurfaceVolume_SumSum_24h']=MOHID_In.SurfaceVolumeSum_24h.sum(
        dim='nspills', skipna=True)
    SurfaceOut['SurfaceVolume_SumSum_24h_to_72h']=MOHID_In.SurfaceVolumeSum_24h_to_72h.sum(
        dim='nspills', skipna=True)
    SurfaceOut['SurfaceVolume_SumSum_72h_to_168h']=MOHID_In.SurfaceVolumeSum_72h_to_168h.sum(
        dim='nspills', skipna=True)
    SurfaceOut['SurfaceVolume_MaxSum']=MOHID_In.SurfaceVolumeMax.sum(
        dim='nspills', skipna=True)
    
    return SurfaceOut

def main(yaml_file, oil_type, first, last, output_folder):
    startTime = time.time()
    print(f'{oil_type}, files{first}-{last}\n')
    #------------------------------------------------------------
    # Global/fixed variables
    #------------------------------------------------------------
    # Specify surface level for depth slice
    input_netcdf_dir=pathlib.Path('/scratch/dlatorne/MIDOSS/runs/monte-carlo')
    output_netcdf_dir=pathlib.Path('/scratch/rmueller/MIDOSS/Results',output_folder) 
    # create threshold for surface and beach volume in m3
    surface_threshold = 3e-3
    beach_threshold = 15e-3
    #------------------------------------------------------------
    # Load yaml file name with list of output netcdf files to aggregate
    #------------------------------------------------------------
    with yaml_file.open("rt") as f:
        run_paths = yaml.safe_load(f)   
    #------------------------------------------------------------
    # Define output netcdf name
    #------------------------------------------------------------
    aggregated_beaching_nc = output_netcdf_dir / f'beaching_{oil_type}_{first}-{last}.nc'
    aggregated_surface_nc = output_netcdf_dir / f'surface_{oil_type}_{first}-{last}.nc'    
    #------------------------------------------------------------
    # Aggregate beaching model output 
    #------------------------------------------------------------
    beaching = aggregate_SOILED_beaching(
        run_paths[oil_type][first:last], 
        beach_threshold)
    #------------------------------------------------------------
    # Aggregate surface model output 
    #------------------------------------------------------------
    surface = aggregate_SOILED_surface(
        run_paths[oil_type][first:last], 
        surface_threshold)
    #------------------------------------------------------------
    # Save output netcdf files
    #------------------------------------------------------------
    beaching.to_netcdf(aggregated_beaching_nc, engine='h5netcdf')
    surface.to_netcdf(aggregated_surface_nc, engine='h5netcdf')
   
    executionTime = (time.time() - startTime)
    print(f'Execution time in minutes for {oil_type}_{first}-{last}: {executionTime/60:.2f}')

if __name__ == "__main__":
    args = sys.argv[1:]
    yaml_file = pathlib.Path(args[0])
    oil_type = args[1]
    start = int(args[2])
    end = int(args[3])
    folder_name = args[4]
    main(yaml_file, oil_type, start, end, folder_name)
