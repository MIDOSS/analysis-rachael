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
WW3, HRDPS and MOHID models. """
import os
import pathlib
import yaml
import numpy
import xarray
import h5netcdf
from datetime import datetime
from glob import glob
import time


def get_MOHID_netcdf_filenames(results_dir, output_dir):
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
    runsets = sorted(glob(os.path.join(results_dir,"near-BP_*")))
    # get list of runs within each runset
    runs = []
    for runset in runsets:
        runs.extend(sorted(
            glob(os.path.join(runset,'results','near-BP_*')))[:])        
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
    
    # write filenames to .yaml with timestamp in filename
    now = datetime.now()
    dt_string = now.strftime("%d%m%Y_%H:%M:%S")
    out_f = output_dir+f'/MOHID_results_locations_{dt_string}.yaml'
    with open(out_f, 'w') as output_yaml:
        documents = yaml.safe_dump(files, output_yaml)
    
    return files

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
                #~~~ Surface ~~~
                vol3d=ds.OilWaterColumnOilVol_3D.isel({'grid_z': 39})
                # Surface presence masks 
                # sfcmask3d=xarray.DataArray(
                #     data=numpy.ones_like(ds.Thickness_2D, dtype=int),
                #     coords=ds.Thickness_2D.coords,
                #     dims=ds.Thickness_2D.dims,
                # )
                sfcmask2d=xarray.DataArray(
                    data=numpy.ones_like(ds.Oil_Arrival_Time, dtype=int),
                    coords=ds.Oil_Arrival_Time.coords,
                    dims=ds.Oil_Arrival_Time.dims,
                )
                # Locations of surface oiling > threshold
                # sfcmask3d_threshold=sfcmask3d.where(
                #     vol3d>surface_threshold
                # )
                # sfcmask2d_threshold = sfcmask2d.where(
                #     vol3d.max(dim='time')>surface_threshold
                # )
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

#------------------------------------------------------------
# Aggregate! 
#------------------------------------------------------------
##  THE FOLLOWING COULD EVENTUALLY BE PASSED IN AS VARIABLES
#------------------------------------------------------------
startTime = time.time()
input_netcdf_dir=pathlib.Path('/scratch/dlatorne/MIDOSS/runs/monte-carlo')
output_netcdf_dir=pathlib.Path('/scratch/rmueller/MIDOSS/Results') 
yaml_file=pathlib.Path(
     '/home/rmueller/projects/def-allen/rmueller/MIDOSS/Visualization',
     'MOHID_results_locations_07102021_15:52:22.yaml')
group_runs = 10
ngroups = 1   
#------------------------------------------------------------
# Global variables
#------------------------------------------------------------
oil_types = ['akns', 'bunker', 'dilbit', 'jet', 'diesel', 'gas', 'other']
# Specify surface level for depth slice
zlevel = 39
slc = {'grid_z': zlevel}
ny,nx = 896, 396
x, y = numpy.arange(0,nx), numpy.arange(0,ny)
# create threshold for surface and beach volume in m3
surface_threshold = 3e-3
beach_threshold = 15e-3
#------------------------------------------------------------
# Load yaml file name with list of output netcdf files to aggregate
#------------------------------------------------------------
with yaml_file.open("rt") as f:
    run_paths = yaml.safe_load(f)   
n_iter={}
for oil in oil_types:
    n_iter[oil]=max(1,len(run_paths[oil])/group_runs)
#------------------------------------------------------------
# Iterate through oil types and aggregate SOILED model output
# in batches of "group_runs" number of files
#------------------------------------------------------------
for oil in oil_types: # loop through oils
    this_iter = 1
    print(f'*** {oil} (Number of iterations: {n_iter[oil]}) ***')
    # loop through specified number of groups
    while (this_iter <= ngroups) & (n_iter[oil]>=this_iter): 
        print(f'Iteration: {this_iter} ')
        first = (this_iter-1) * group_runs 
        last = this_iter*group_runs - 1
        #sys.stdout.write(f'{oil}_{this_iter}_of_{n_iter[oil]}, files{first}-{last}\n')
        print(f'{oil}_{this_iter}_of_{n_iter[oil]}, files{first}-{last}\n')

        #------------------------------------------------------------
        # Define output netcdf name
        aggregated_beaching_nc = output_netcdf_dir / f'beaching_{oil}_runset{this_iter}.nc'
        aggregated_surface_nc = output_netcdf_dir / f'surface_{oil}_runset{this_iter}.nc'
        aggregated_csv = output_netcdf_dir / f'{oil}_runset{this_iter}_filenames.csv'
        #------------------------------------------------------------
        # # Aggregate model output 
        # beaching,surface = aggregate_SOILED(
        #     run_paths[oil][first:last], 
        #     surface_threshold=3e-3, 
        #     beach_threshold=15e-3)
         # Aggregate beaching model output 
        beaching = aggregate_SOILED_beaching(
            run_paths[oil][first:last], 
            beach_threshold=15e-3)
         # Aggregate surface model output 
        surface = aggregate_SOILED_surface(
            run_paths[oil][first:last], 
            surface_threshold=3e-3)
        # Save output netcdf and a .csv file containing list of runs
        beaching.to_netcdf(aggregated_beaching_nc, engine='h5netcdf')
        surface.to_netcdf(aggregated_surface_nc, engine='h5netcdf')
        #numpy.savetxt(aggregated_csv, files, delimiter =", ", fmt ='% s')
        this_iter += 1
    executionTime = (time.time() - startTime)
    print(f'Execution time in minutes for {oil}: {executionTime/60:.2f}')


