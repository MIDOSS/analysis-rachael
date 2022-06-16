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
from datetime import date
from glob import glob
import time


# Uncomment @profile if you want to use memory-profiler for stdout on 
# memory usage
#@profile
def aggregate_SOILED(run_list, beach_threshold=5e-3, time_threshold=0.2,
    sfc_vol_threshold=3e-3, sfc_conc_threshold=0, sfc_diss_threshold=0):
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
    spill_volume=numpy.zeros(nruns)
    latitude=numpy.zeros(nruns)
    longitude=numpy.zeros(nruns)
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
            BeachPresence_72h_to_168h=(dims, numpy.zeros((nruns,ny,nx),dtype=int)),
            SurfacePresence=(dims, numpy.zeros((nruns,ny,nx),dtype=int)),
            SurfacePresence_24h=(dims, numpy.zeros((nruns,ny,nx),dtype=int)),
            SurfacePresence_24h_to_72h=(dims, numpy.zeros((nruns,ny,nx),dtype=int)),
            SurfacePresence_72h_to_168h=(dims, numpy.zeros((nruns,ny,nx),dtype=int)),
            SurfaceVolumeSum=(dims, numpy.zeros((nruns,ny,nx),dtype=float)),
            SurfaceVolumeMax=(dims, numpy.zeros((nruns,ny,nx),dtype=float)),
            SurfaceVolumeSum_24h=(dims, numpy.zeros((nruns,ny,nx),dtype=float)),
            SurfaceVolumeSum_24h_to_72h=(dims, numpy.zeros((nruns,ny,nx),dtype=float)),
            SurfaceVolumeSum_72h_to_168h=(dims, numpy.zeros((nruns,ny,nx),dtype=float)),
            SurfaceConcentrationSum=(dims, numpy.zeros((nruns,ny,nx),dtype=float))
        ),
        coords=dict(
            grid_y=range(ny),
            grid_x=range(nx))
    )
    
    dims=('grid_y','grid_x')
    # ~~~~~~~~~~~~~~
    # Beaching 
    # ~~~~~~~~~~~~~~ 
    BeachingOut=xarray.Dataset(
        data_vars=dict(
            BeachTime_Min=(dims, numpy.zeros((ny,nx)),
               {"units":"hours",
                "description":("Earliest beaching arrival time at "
                    "locations where beached oil is above "
                    "BeachVolume_threshold and beaching time is greater "
                    f"than {time_threshold} hr (~1 min for 0.02 default)")}), 
            BeachTime_Sum=(dims, numpy.zeros((ny,nx)),
                {"units":"hours",
                "description":("The sum across runs of the earliest beaching "
                    " arrival time at locations where beached oil is above "
                    "BeachVolume_threshold")}),
            TotalBeachVolume=(dims, numpy.zeros((ny,nx),dtype=float),
                {"units":"m3/gridcell",
                "description":("Total beaching volume summed over all runs where" 
                    "volume>BeachVolume_threshold in any given, individual "
                    "run")}),
            TotalBeachVolume_ln=(dims, numpy.zeros((ny,nx),dtype=float),
                {"units":"m3/gridcell",
                "description":("Natural log of time-integrated beaching volume "
                    "summed over all runs where time-integrated volume is greater "
                    "than BeachVolume_threshold in any given, individual run")}),
            BeachPresence=(dims, numpy.zeros((ny,nx),dtype=int),
                {"units":"",
                 "flag_values":"0,1",
                 "flag_meaning":"oil absent, oil present",
                 "description":("An integer value 0<n<=N_spills representing the "
                    "number out of N_spills where oil presence on beaches is "
                    "above the BeachVolume_threshold")}),
            BeachPresence_24h=(dims, numpy.zeros((ny,nx),dtype=int),
                {"units":"",
                 "flag_values":"0,1",
                 "flag_meaning":"oil absent, oil present",
                 "description":("An integer value 0<n<=N_spills representing the "
                    " number of N_spills where oil presence on beaches is above "
                    "the BeachVolume_threshold and within the first 24 hours "
                    "of spill")}),
            BeachPresence_24h_to_72h=(dims, numpy.zeros((ny,nx),dtype=int),
                {"units":"",
                 "flag_values":"0,1",
                 "flag_meaning":"oil absent, oil present",
                 "description":("An integer value 0<n<=N_spills representing the "
                    "number of N_spills where oil presence on beaches is above "
                    "the BeachVolume_threshold and within [24,72) hours "
                    "after spill")}),
            BeachPresence_72h_to_168h=(dims, numpy.zeros((ny,nx),dtype=int),
                {"units":"none",
                 "flag_values":"0,1",
                 "flag_meaning":"oil absent, oil present",
                 "description":("An integer value 0<n<=N_spills representing the "
                    "number of N_spills where oil presence on beaches is above "
                    "the BeachVolume_threshold and within [72,168) hours "
                    "after spill")})),
        coords=dict(
            grid_y=range(ny),
            grid_x=range(nx)), 
        attrs=dict(
            BeachVolume_threshold=beach_threshold,
            BeachVolume_threshold_units="m3",),
    )
    # ~~~~~~~~~~~~~~
    # Surface 
    # ~~~~~~~~~~~~~~ 
    SurfaceOut=xarray.Dataset(
        data_vars=dict(
            SurfacePresence=(dims, numpy.zeros((ny,nx),dtype=int),
                {"units":"",
                 "description":("An integer value 0<n<=N_spills representing the "
                    "number out of N_spills where oil presence is above the "
                    "SurfaceVolume_threshold."),
                 "flag_values":'0,1',
                 "flag_meaning":'oil absent, oil present'}),
            SurfacePresence_24h=(dims, numpy.zeros((ny,nx),dtype=int),
                {"units":"",
                 "description":("An integer value 0<n<=N_spills representing the "
                    "number out of N_spills where oil presence is above the "
                    "SurfaceVolume_threshold and within first 24 hrs after initial"
                    " spill time for individual spill scenario."),
                 "flag_values":'0,1',
                 "flag_meaning":'oil absent, oil present'}),
            SurfacePresence_24h_to_72h=(dims, numpy.zeros((ny,nx),dtype=int),
                {"units":"",
                 "description":("An integer value 0<n<=N_spills representing "
                    "the number out of N_spills where oil presence is above "
                    "the SurfaceVolume_threshold and within 24-72 hrs of "
                    "initial spill time for individual spill scenario."),
                 "flag_values":'0,1',
                 "flag_meaning":'oil absent, oil present'}),
            SurfacePresence_72h_to_168h=(dims, numpy.zeros((ny,nx),dtype=int),
                {"units":"",
                 "description":("An integer value 0<n<=N_spills representing the "
                    "number out of N_spills where oil presence is above the "
                    "SurfaceVolume_threshold and within 72-168 hrs of initial "
                    "spill time for individual spill scenario."),
                 "flag_values":'0,1',
                 "flag_meaning":'oil absent, oil present'}),
            SurfaceVolume_SumSum=(dims, numpy.zeros((ny,nx),dtype=float),
                {"units":"m3",
                 "description":("Time-integrated values of the "
                    "surface volume, summed across "
                    "different spill scenarios.")}),
            SurfaceConcentration_SumSum=(dims, numpy.zeros((ny,nx),dtype=float),
                {"units":"Kg/m3",
                 "description":("Time-integrated values of the "
                    "surface-level concentration, summed across " 
                    "different spill scenarios.")}),
            SurfaceVolume_SumSum_24h=(dims, numpy.zeros((ny,nx),dtype=float),
                {"units":"m3",
                 "description":("Time-integrated values over the first "
                    "24-hrs after spill scenario, summed across " 
                    "different spill scenarios.")}),
            SurfaceVolume_SumSum_24h_to_72h=(dims, numpy.zeros((ny,nx),dtype=float),
                {"units":"m3",
                 "description":("Time-integrated values between 24 and 72 "
                    "hours after spill scenario, summed across " 
                    "different spill scenarios.")}),
            SurfaceVolume_SumSum_72h_to_168h=(dims, numpy.zeros((ny,nx),dtype=float),
                {"units":"m3",
                 "description":("Time-integrated values between 72 and 168 "
                    "hours after spill scenario, summed across " 
                    "different spill scenarios.")}),
            SurfaceVolume_MaxSum=(dims, numpy.zeros((ny,nx),dtype=float),
                {"units":"m3",
                 "description":("Sum of volume across different spills "
                      "where each spill instance is represented by the "
                      "maximum value across time of the surface spill volume.")}),
            SurfaceConcentration_SumSum_ln=(dims, numpy.zeros((ny,nx),dtype=float),
                {"units":"Kg/m3",
                 "description":("Natural log of the time-integrated "
                    "surface-level concentration, summed across" 
                    "different spill scenarios.")}),
            SurfaceVolume_SumSum_ln=(dims, numpy.zeros((ny,nx),dtype=float),
                {"units":"m3",
                 "description":("Natural log of the time-integrated "
                    "surface volume, summed across" 
                    "different spill scenarios.")}),
            SurfaceVolume_SumSum_24h_ln=(dims, numpy.zeros((ny,nx),dtype=float),
                {"units":"m3",
                 "description":("Natural log of the time-integrated "
                    "surface volume within the first "
                    "24-hrs after spill scenario, summed across" 
                    "different spill scenarios.")}),
            SurfaceVolume_SumSum_24h_to_72h_ln=(dims, numpy.zeros((ny,nx),dtype=float),
                {"units":"m3",
                 "description":("Natural log of the time-integrated "
                    "surface volume values between 24 and 72 "
                    "hours after spill scenario, summed across" 
                    "different spill scenarios.")}),
            SurfaceVolume_SumSum_72h_to_168h_ln=(dims, numpy.zeros((ny,nx),dtype=float),
                {"units":"m3",
                 "description":("Natural log of the time-integrated "
                    "surface volume values between 72 and 168 "
                    "hours after spill scenario, summed across" 
                    "different spill scenarios.")}),
            SurfaceVolume_MaxSum_ln=(dims, numpy.zeros((ny,nx),dtype=float),
                {"units":"m3",
                 "description":("Natural log of the maximum surface "
                      "volume per spill, summed across all spills.")})
        ),
        coords=dict(
            grid_y=range(ny),
            grid_x=range(nx)),
        attrs=dict(
            SfcVolume_threshold=sfc_vol_threshold,
            SfcConcentration_threshold=sfc_conc_threshold,
            SfcVolume_threshold_units="m3",
            SfcConcentration_threshold_units="Kg/m3"),
        )
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # loop through runs and aggregate beaching information
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    for run in range(nruns):
        print(f'Run {run} of {nruns}')
        input_file=run_list[run]
        input_dir=os.path.dirname(os.path.abspath(input_file))
        # identify oil type and run number from .nc file to query Lagrangian.dat file
        nrun = input_file.split('/')[-1].split('-')[-1][:-3]
        oil_tag = input_file.split('/')[-1].split('_')[1].split('-')[0]
        Lagrangian_file = input_dir+f'/Lagrangian_{oil_tag}-{nrun}.dat'
        if os.path.isfile(input_file):
            # Read in results from output netcdf
            try:
                with xarray.open_dataset(input_file, engine='h5netcdf') as ds:
                    spill_start = ds.time[0]
                    spill_end = ds.time[-1]
                    # Select surface volume, concentration and dissolution
                    vol3d=ds.OilWaterColumnOilVol_3D.isel({'grid_z': 39})
                    conc3d=ds.OilConcentration_3D.isel({'grid_z': 39})

            except:
                print(f'missing {input_file}') 
                continue 
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            # Grab spill information from Lagrangian file
            with open(Lagrangian_file, 'r') as lagrangianFile:
                print(Lagrangian_file)
                for line in lagrangianFile:
                    if 'POINT_VOLUME              :' in line: 
                        # select spill volume quantity after ':'
                        spillvolume = line.split(':')[-1].split('\n')[0]
                    if 'POSITION_COORDINATES       :' in line:
                        spill_location = line.split(':')[-1].split('\n')[0]
                        print(spill_location)
                    if 'POSITION_COORDINATES      :' in line:
                        spill_location = line.split(':')[-1].split('\n')[0]
                        print(spill_location)
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            # Store basics: Filename, lat, lon, spill volume
            files.append(input_file)
            spill_volume[run]=float(spillvolume)
            latitude[run]=(float(spill_location.split(' ')[2]))
            longitude[run]=(float(spill_location.split(' ')[1]))
            # ~~~~~~~~~~~~~~

            # Beaching 
            # ~~~~~~~~~~~~~~    
            # Beaching time (converted from ns to hours)
            MOHID_In.BeachTime[run,:,:]=(ds.Beaching_Time-spill_start
                )*nanosecond_to_hour
            # Set time to NaT where volume is below threshold 
            MOHID_In['BeachTime']=MOHID_In.BeachTime.where(
                ds.Beaching_Volume>beach_threshold
            )
            # Save volume over threshold 
            MOHID_In.BeachVolume[run,:,:]=ds.Beaching_Volume.where(
                ds.Beaching_Volume>beach_threshold
            )             
            # Presence above threshold
            MOHID_In.BeachPresence[run,:,:]=(
                ds.Beaching_Volume>beach_threshold
            ).astype(int)
            MOHID_In.BeachPresence_24h[run,:,:]=(
                ds.Beaching_Volume>beach_threshold).where(numpy.logical_and(
                   ds.Beaching_Time>=spill_start,
                   ds.Beaching_Time<spill_start+one_day),
                False).astype(int)          
            MOHID_In.BeachPresence_24h_to_72h[run,:,:]=(
                ds.Beaching_Volume>beach_threshold).where(numpy.logical_and(
                   ds.Beaching_Time>=spill_start+one_day,
                   ds.Beaching_Time<spill_start+three_days),
                False).astype(int)
            MOHID_In.BeachPresence_72h_to_168h[run,:,:]=(
                ds.Beaching_Volume>beach_threshold).where(numpy.logical_and(
                   ds.Beaching_Time>=spill_start+three_days,
                   ds.Beaching_Time<spill_start+seven_days),
                False).astype(int)
            # ~~~~~~~~~~~~~~
            # Surface Values
            # ~~~~~~~~~~~~~~
            MOHID_In.SurfacePresence[run,:,:]=(
                vol3d.max(dim='time',skipna=True)>sfc_vol_threshold
            ).astype(int)
            MOHID_In.SurfacePresence_24h[run,:,:]=(
                vol3d.max(dim='time',skipna=True)>sfc_vol_threshold
                ).where(numpy.logical_and(
                    ds.Oil_Arrival_Time>=spill_start,
                    ds.Oil_Arrival_Time<spill_start+one_day),
                    False
            ).astype(int)
            MOHID_In.SurfacePresence_24h_to_72h[run,:,:]=(
                vol3d.max(dim='time',skipna=True)>sfc_vol_threshold
                ).where(numpy.logical_and(
                    ds.Oil_Arrival_Time>=spill_start+one_day,
                    ds.Oil_Arrival_Time<spill_start+three_days),
                    False
            ).astype(int)
            MOHID_In.SurfacePresence_72h_to_168h[run,:,:]=(
                vol3d.max(dim='time',skipna=True)>sfc_vol_threshold
                ).where(numpy.logical_and(
                    ds.Oil_Arrival_Time>=spill_start+three_days,
                    ds.Oil_Arrival_Time<spill_start+seven_days),
                    False
            ).astype(int)
            # Sum volume over time where volume is greater than threshold
            vol3d_sumt = vol3d.where(vol3d>sfc_vol_threshold).sum(
                    dim="time",skipna=True)
            conc3d_sumt = conc3d.sum(dim="time",skipna=True)
            # 3d volume above threshold limits
            vol3dthresh = vol3d.where(vol3d>sfc_vol_threshold)
            # Surface max above surface threshold
            vol3d_max = vol3d.max(dim="time",skipna=True)
            # Integrated surface volume over time where oiling>threshold
            MOHID_In.SurfaceVolumeSum[run,:,:]=vol3d_sumt
            MOHID_In.SurfaceVolumeSum_24h[run,:,:]=vol3dthresh.where(
                numpy.logical_and(
                    ds.Oil_Arrival_Time>=spill_start,
                    ds.Oil_Arrival_Time<spill_start+one_day),
                    False
            ).sum(dim="time",skipna=True)
            MOHID_In.SurfaceVolumeSum_24h_to_72h[run,:,:]=vol3dthresh.where(
                numpy.logical_and(
                    ds.Oil_Arrival_Time>=spill_start+one_day,
                    ds.Oil_Arrival_Time<spill_start+three_days),
                    False
            ).sum(dim="time",skipna=True)
            MOHID_In.SurfaceVolumeSum_72h_to_168h[run,:,:]=vol3dthresh.where(
                numpy.logical_and(
                    ds.Oil_Arrival_Time>=spill_start+three_days,
                    ds.Oil_Arrival_Time<spill_start+seven_days),
                    False
            ).sum(dim="time",skipna=True)
            MOHID_In.SurfaceVolumeMax[run,:,:]=vol3d_max.where(
                vol3d_max>sfc_vol_threshold, 0)
            MOHID_In.SurfaceConcentrationSum[run,:,:]=conc3d_sumt
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Flatten MOHID output into 2D arrays by 
    # taking minimum of spill values or adding across spill values 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    MOHID_In.fillna(0)
    nspills=len(files)
    # Beaching xarray for output netcdf
    # By default, .sum() only skips missing values for float dtypes 
    # but it seems to function for timedelta64[ns]
    # keeping `skipna=True` in code for clarity purposes only
    BeachingOut.attrs['Filenames']=files
    BeachingOut.attrs['N_spills']=nspills
    BeachingOut.attrs['spill_volume']=spill_volume
    BeachingOut.attrs['latitude']=latitude
    BeachingOut.attrs['longitude']=longitude
    BeachingOut.attrs['creation_date']=date.today().strftime("%B %d, %Y") 
    BeachingOut.attrs['created_by']='Rachael D. Mueller'
    SurfaceOut.attrs['created_with']=(
        'https://github.com/MIDOSS/analysis-rachael/blob/'
        'main/scripts/monte_carlo/aggregate_oil_spills.py')
    BeachingOut.attrs['project_website']=(
        'https://midoss-docs.readthedocs.io/en/latest/index.html'   
    )
    BeachingOut['BeachTime_Min']=MOHID_In.BeachTime.where(
        MOHID_In.BeachTime>time_threshold).min(dim='nspills', skipna=True)
    BeachingOut['BeachTime_Sum']=(
        MOHID_In.BeachTime.sum(dim='nspills', skipna=True)
    )
    BeachingOut['TotalBeachVolume']=MOHID_In.BeachVolume.sum(
        dim='nspills', skipna=True)
    BeachingOut['TotalBeachVolume_ln']=numpy.log(MOHID_In.BeachVolume.where(
        MOHID_In.BeachVolume>0)).sum(dim='nspills', skipna=True)
    BeachingOut['BeachPresence']=MOHID_In.BeachPresence.sum(
        dim='nspills', skipna=True)
    BeachingOut['BeachPresence_24h']=MOHID_In.BeachPresence_24h.sum(
        dim='nspills', skipna=True)
    BeachingOut['BeachPresence_24h_to_72h']=(
        MOHID_In.BeachPresence_24h_to_72h.sum(dim='nspills', skipna=True)
    )
    BeachingOut['BeachPresence_72h_to_168h']=(
        MOHID_In.BeachPresence_72h_to_168h.sum(dim='nspills', skipna=True)
    )
    print('surface')
    # Surface oiling xarray for output netcdf
    SurfaceOut.attrs['Filenames']=files
    SurfaceOut.attrs['N_spills']=nspills
    SurfaceOut.attrs['spill_volume']=spill_volume
    SurfaceOut.attrs['latitude']=latitude
    SurfaceOut.attrs['longitude']=longitude
    SurfaceOut.attrs['creation_date']=date.today().strftime("%B %d, %Y")  
    SurfaceOut.attrs['created_by']='Rachael D. Mueller'
    SurfaceOut.attrs['created_with']=(
        'https://github.com/MIDOSS/analysis-rachael/blob/'
        'main/scripts/monte_carlo/aggregate_oil_spills.py')
    SurfaceOut.attrs['project_website']=(
        'https://midoss-docs.readthedocs.io/en/latest/index.html'
    )
    SurfaceOut['SurfacePresence']=MOHID_In.SurfacePresence.sum(dim='nspills') 
    SurfaceOut['SurfacePresence_24h']=(
        MOHID_In.SurfacePresence_24h.sum(dim='nspills')
    )
    SurfaceOut['SurfacePresence_24h_to_72h']=(
        MOHID_In.SurfacePresence_24h_to_72h.sum(dim='nspills')
    )
    SurfaceOut['SurfacePresence_72h_to_168h']=(
        MOHID_In.SurfacePresence_72h_to_168h.sum(dim='nspills')
    ) 
    # straight-sum
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
    # log transformed surface volumes
    SurfaceOut['SurfaceVolume_SumSum_ln']=numpy.log(
       MOHID_In.SurfaceVolumeSum.where(MOHID_In.SurfaceVolumeSum>0)
    ).sum(dim='nspills', skipna=True)
    SurfaceOut['SurfaceVolume_SumSum_24h_ln']=numpy.log(
       MOHID_In.SurfaceVolumeSum_24h.where(MOHID_In.SurfaceVolumeSum_24h>0)
    ).sum(dim='nspills', skipna=True)
    SurfaceOut['SurfaceVolume_SumSum_24h_to_72h_ln']=numpy.log(
       MOHID_In.SurfaceVolumeSum_24h_to_72h.where(
           MOHID_In.SurfaceVolumeSum_24h_to_72h>0)
    ).sum(dim='nspills', skipna=True)
    SurfaceOut['SurfaceVolume_SumSum_72h_to_168h_ln']=numpy.log(
       MOHID_In.SurfaceVolumeSum_72h_to_168h.where(
           MOHID_In.SurfaceVolumeSum_72h_to_168h>0)
    ).sum(dim='nspills', skipna=True)
    SurfaceOut['SurfaceVolume_MaxSum_ln']=numpy.log(
        MOHID_In.SurfaceVolumeMax.where(
        MOHID_In.SurfaceVolumeMax>0)).sum(dim='nspills', skipna=True)
    SurfaceOut['SurfaceConcentration_SumSum_ln']=numpy.log(
        MOHID_In.SurfaceConcentrationSum.where(
        MOHID_In.SurfaceConcentrationSum>0)).sum(
            dim='nspills', skipna=True)
    return BeachingOut, SurfaceOut, MOHID_In

def main(yaml_file, sort_tag, first, last, output_folder):
    """Aggregate surface and beaching output from SOILED
    :param yaml_file: Directory path to yaml file the contains a dictionary 
         of output netcdf paths organized by oil types 
         (created with `get_SOILED_netcdf_filenames` in 
         `create_SOILED_runlist.ipynb`.)
    :type yaml_file: :py:class:`pathlib.Path`
    :param sort_tag: either oil type label or months, i.e.: 
         ('akns', 'bunker', 'dilbit', 'jet', 'diesel', 'gas', 'other'), or
         ('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep',
         'Oct','Nov','Dec')
    :type sort_tags: :py:class:`str` or `int`
    :param first: array index of the first file in yaml_file[sort_tag] 
       to process as part of this batch of runs of [first, last) files
    :type first: :py:class:`int`
    :param last: array index of the last file in yaml_file[sort_tag] 
       to process as part of this batch of runs of [first, last) files
    :type last: :py:class:`int`
    :param output_folder: directory to place output netcdf
    :type output_folder: :py:class:`pathlib.Path`
    """
    startTime = time.time()
    print(f'{sort_tag}, files[{first}-{last})\n')
    #------------------------------------------------------------
    # Global/fixed variables
    #------------------------------------------------------------
    # Specify surface level for depth slice
    input_netcdf_dir=pathlib.Path('/scratch/dlatorne/MIDOSS/runs/monte-carlo')
    output_netcdf_dir=pathlib.Path('/scratch/rmueller/MIDOSS/Results',output_folder) 
    # create threshold for surface and beach volume in m3
    surface_threshold = 3e-3
    beach_threshold = 5e-3
    #------------------------------------------------------------
    # Load yaml file name with list of output netcdf files to aggregate
    #------------------------------------------------------------
    with yaml_file.open("rt") as f:
        run_paths = yaml.safe_load(f)   
    #------------------------------------------------------------
    # Define output netcdf name
    #------------------------------------------------------------
    aggregated_beaching_nc = output_netcdf_dir / f'beaching_{sort_tag}_{first}-{last}.nc'
    aggregated_surface_nc = output_netcdf_dir / f'surface_{sort_tag}_{first}-{last}.nc'
    mohid_output_nc = output_netcdf_dir / f'mohid_{sort_tag}_{first}-{last}.nc'
    #------------------------------------------------------------
    # Aggregate beaching and surface model output 
    #------------------------------------------------------------
    beaching,surface,mohid_output = aggregate_SOILED(
        run_paths[sort_tag][first:last]
    )
    # add information about yaml file version
    beaching.attrs['yaml_file']=str(yaml_file)
    surface.attrs['yaml_file']=str(yaml_file)
    #------------------------------------------------------------
    # Save output netcdf files
    #------------------------------------------------------------
    # My thinking with this fill value is it will help make 
    # the coding easier for aggregating the aggregated files, but
    # I'm evaluating this choice....
    fillval = {'_FillValue':0}
    beach_encoding = {var: fillval for var in beaching.data_vars}
    surface_encoding = {var: fillval for var in surface.data_vars}
    beaching.to_netcdf(
        aggregated_beaching_nc, engine='h5netcdf',encoding=beach_encoding
    )
    surface.to_netcdf(
        aggregated_surface_nc, engine='h5netcdf',encoding=surface_encoding
    )
    mohid_output.to_netcdf(
        mohid_output_nc, engine='h5netcdf'
    )
    executionTime = (time.time() - startTime)
    print(f'Execution time in minutes for {sort_tag}_{first}-{last}: {executionTime/60:.2f}')

if __name__ == "__main__":
    args = sys.argv[1:]
    yaml_file = pathlib.Path(args[0])
    sort_tag = args[1]
    start = int(args[2])
    end = int(args[3])
    folder_name = args[4]
    main(yaml_file, sort_tag, start, end, folder_name)
