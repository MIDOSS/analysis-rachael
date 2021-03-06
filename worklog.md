### 5/20/19
oops.  Some of the work on this day was logged on the 19th.

####Updated Lagrangian_gasoline_refined.dat
Submitted a 5 minute test run

```
[rmueller@cedar1 SOG_01dec2017]$ mohid run submit_run_gas.yaml $PROJECT/rmueller/MIDOSS/results/LightEvaporator/gas/SOG_01dec2017
mohid_cmd.run INFO: Created temporary run directory /scratch/rmueller/MIDOSS/runs/LightEvaporators/SOG_01dec17_LightEvaporatorGas_1000m3_7days_2019-05-20T210302.855692-0700
mohid_cmd.run INFO: Wrote job run script to /scratch/rmueller/MIDOSS/runs/LightEvaporators/SOG_01dec17_LightEvaporatorGas_1000m3_7days_2019-05-20T210302.855692-0700/MOHID.sh
mohid_cmd.run INFO: Submitted batch job 21274382
```
from stdout
```
Please Wait...
 -------------------------- MODEL -------------------------

 Constructing      :
 ID                :            1

 OPENMP: Max number of threads available is            1
 OPENMP: Number of threads requested is           12
 <Compilation Options Warning>
 OPENMP: Number of threads implemented is            1

 Could not read solution from HDF5 file
 Last instant in file lower than simulation ending time
 Matrix name: mean wave period
```
The only issue I could see is that I submitted with "def-allen" instead of "rrg-allen".  Testing....

```
[rmueller@cedar1 SOG_01dec2017]$ mohid run submit_run_gas.yaml $PROJECT/rmueller/MIDOSS/results/LightEvaporator/gas/SOG_01dec2017
mohid_cmd.run INFO: Created temporary run directory /scratch/rmueller/MIDOSS/runs/LightEvaporators/SOG_01dec17_LightEvaporatorGas_1000m3_6ays_2019-05-20T212537.861744-0700
mohid_cmd.run INFO: Wrote job run script to /scratch/rmueller/MIDOSS/runs/LightEvaporators/SOG_01dec17_LightEvaporatorGas_1000m3_6ays_2019-05-20T212537.861744-0700/MOHID.sh
mohid_cmd.run INFO: Submitted batch job 21274785
```
 
SUCCESS! 
Submitted a full 6-day run for gasoline case;
```
[rmueller@cedar1 SOG_01dec2017]$ mohid run submit_run_gas.yaml $PROJECT/rmueller/MIDOSS/results/LightEvaporator/gas/SOG_01dec2017
mohid_cmd.run INFO: Created temporary run directory /scratch/rmueller/MIDOSS/runs/LightEvaporators/SOG_01dec17_LightEvaporatorGas_1000m3_6ays_2019-05-20T213015.032599-0700
mohid_cmd.run INFO: Wrote job run script to /scratch/rmueller/MIDOSS/runs/LightEvaporators/SOG_01dec17_LightEvaporatorGas_1000m3_6ays_2019-05-20T213015.032599-0700/MOHID.sh
mohid_cmd.run INFO: Submitted batch job 21274811
```

####Updated Lagrangian_jetfuel_refined.dat
Submitted a 5 minute test run

```
[rmueller@cedar1 SOG_01dec2017]$ mohid run submit_run_jetfuel.yaml $PROJECT/rmueller/MIDOSS/results/LightEvaporator/jet_fuel/SOG_01dec2017
mohid_cmd.run INFO: Created temporary run directory /scratch/rmueller/MIDOSS/runs/LightEvaporators/SOG_01dec17_LightEvaporatorJetFuel_1000m3_6days_2019-05-20T211724.068162-0700
mohid_cmd.run INFO: Wrote job run script to /scratch/rmueller/MIDOSS/runs/LightEvaporators/SOG_01dec17_LightEvaporatorJetFuel_1000m3_6days_2019-05-20T211724.068162-0700/MOHID.sh
mohid_cmd.run INFO: Submitted batch job 21274670
```
SUCCESS!
submitted a full 6-day run for jet fuel case:

```
[rmueller@cedar1 SOG_01dec2017]$ mohid run submit_run_jetfuel.yaml $PROJECT/rmueller/MIDOSS/results/LightEvaporator/jet_fuel/SOG_01dec2017
mohid_cmd.run INFO: Created temporary run directory /scratch/rmueller/MIDOSS/runs/LightEvaporators/SOG_01dec17_LightEvaporatorJetFuel_1000m3_6days_2019-05-20T212745.888804-0700
mohid_cmd.run INFO: Wrote job run script to /scratch/rmueller/MIDOSS/runs/LightEvaporators/SOG_01dec17_LightEvaporatorJetFuel_1000m3_6days_2019-05-20T212745.888804-0700/MOHID.sh
mohid_cmd.run INFO: Submitted batch job 21274792
```
### 5/19/19

Fixed time range error in Model_lowdt.dat, ran test simulation to make sure the model was running again, re-submitted job:
```
[rmueller@cedar1 SOG_01dec2017]$ mohid run submit_run_AKNScrude.yaml $PROJECT/rmueller/MIDOSS/results/MediumFloater/AKNS/SOG_01dec2017
nemo_cmd.prepare WARNING: There are uncommitted changes in /project/6001313/rmueller/MIDOSS/MIDOSS-MOHID-config
mohid_cmd.run INFO: Created temporary run directory /scratch/rmueller/MIDOSS/runs/MediumFloater/AKNS/SOG_01dec17_MediumFloater_1000m3_7days_2019-05-20T111949.975090-0700
mohid_cmd.run INFO: Wrote job run script to /scratch/rmueller/MIDOSS/runs/MediumFloater/AKNS/SOG_01dec17_MediumFloater_1000m3_7days_2019-05-20T111949.975090-0700/MOHID.sh
mohid_cmd.run INFO: Submitted batch job 21259146
```
There was an uncommited change which turned out to be:
```
[rmueller@cedar1 SOG_01dec2017]$ hg status
M MediumFloater/SOG_01dec2017/submit_run_AKNScrude.yaml
```
I commited changes

#### Testing Lagrangian_DieselFuel_refined.dat

```
Submitted the following 5-min test

[rmueller@cedar1 SOG_01dec2017]$ mohid run submit_run_diesel.yaml $PROJECT/rmueller/MIDOSS/results/LightEvaporator/diesel/SOG_01dec2017
mohid_cmd.run INFO: Created temporary run directory /scratch/rmueller/MIDOSS/runs/LightEvaporators/SOG_01dec17_LightEvaporatorsDiesel_1000m3_7days_2019-05-20T112758.876748-0700
mohid_cmd.run INFO: Wrote job run script to /scratch/rmueller/MIDOSS/runs/LightEvaporators/SOG_01dec17_LightEvaporatorsDiesel_1000m3_7days_2019-05-20T112758.876748-0700/MOHID.sh
mohid_cmd.run INFO: Submitted batch job 21259377
```

Both the diesel and AKNS test worked, so I submitted a 6-day run.  The runs completed successfully but did not convert to netcdf


```
cp: cannot stat '/scratch/rmueller/MIDOSS/runs/LightEvaporators/SOG_01dec17_LightEvaporatorsDiesel_1000m3_7days_2019-05-20T113445.501234-0700/res/Lagrangian_SOG_01dec17_LightEvaporatorsDiesel_1000m3_7days.hdf5': No such file or directory
Usage: hdf5-to-netcdf4 [OPTIONS] HDF5_FILE NETCDF4_FILE
Try "hdf5-to-netcdf4 --help" for help.

Error: Invalid value for "HDF5_FILE": Path "/localscratch/rmueller.21259492.0/Lagrangian_SOG_01dec17_LightEvaporatorsDiesel_1000m3_7days.hdf5" does not exist.
cp: cannot stat '/localscratch/rmueller.21259492.0/Lagrangian_SOG_01dec17_LightEvaporatorsDiesel_1000m3_7days.nc': No such file or directory
```

hdf5-to-netcdf4 seems to work okay when called in the results directory
```
[rmueller@cedar5 SOG_01dec2017]$ hdf5-to-netcdf4 Lagrangian_AKNS_crude_SOG_01dec17_MediumFloater_1000m3_7days.hdf5 Lagrangian_AKNS_crude_SOG_01dec17_MediumFloater_1000m3_7days.nc
```
Here are cases that didn't work:
```
[rmueller@cedar5 SOG_01dec2017]$ hdf5-to-netcdf4 -v Lagrangian_AKNS_crude_SOG_01dec17_MediumFloater_1000m3_7days.hdf5 Lagrangian_AKNS_crude_SOG_01dec17_MediumFloater_1000m3_7days.nc
Usage: hdf5-to-netcdf4 [OPTIONS] HDF5_FILE NETCDF4_FILE
Try "hdf5-to-netcdf4 --help" for help.

Error: Invalid value for "-v" / "--verbosity": invalid choice: Lagrangian_AKNS_crude_SOG_01dec17_MediumFloater_1000m3_7days.hdf5. (choose from debug, info, warning, error, critical)

[rmueller@cedar5 SOG_01dec2017]$ hdf5-to-netcdf4 --verbosity Lagrangian_AKNS_crude_SOG_01dec17_MediumFloater_1000m3_7days.hdf5 Lagrangian_AKNS_crude_SOG_01dec17_MediumFloater_1000m3_7days.nc
Usage: hdf5-to-netcdf4 [OPTIONS] HDF5_FILE NETCDF4_FILE
Try "hdf5-to-netcdf4 --help" for help.

Error: Invalid value for "-v" / "--verbosity": invalid choice: Lagrangian_AKNS_crude_SOG_01dec17_MediumFloater_1000m3_7days.hdf5. (choose from debug, info, warning, error, critical)
```



### 5/19/19

#### Lagrangian.dat errors

Not seeing model results. No conversion to .nc.  

re-submitted job 
```
>mohid run submit_run_AKNScrude.yaml $PROJECT/rmueller/MIDOSS/results/MediumFloater/AKNS/SOG_01dec2017
```

Stdout now reads: 
```
 -------------------------- MODEL -------------------------
 
 Constructing      : 
 ID                :            1
 
 OPENMP: Max number of threads available is            1
 OPENMP: Number of threads requested is           12
 <Compilation Options Warning>
 OPENMP: Number of threads implemented is            1
 
 Could not read solution from HDF5 file
```

This error indicates to me that the input hdf5 files are not being read, but I've checked paths and they are okay.

AH!  I think I've got it....I put in a longer time than we have data for in the HDF5file.

Reducing time and submitting another test run.  


### 5/17/19

NEXT: 
1) Once confirmed that 7-day test is successful, remove test files from:
/home/rmueller/project/rmueller/MIDOSS/MIDOSS-MOHID-config/MediumFloater/SOG_01dec2017
2) Update all Lagrangian.dat files so they work
3) Ask Shihan about Fay method (not working)
4) Download and test new version of the code
5) Python tutorial
6) Use surface currents to practice plotting up output in python
7) Read Dept. of Ecology Report  



5/16/19

NEXT
1) Write up errors from yesterday and the solutions that helped fix them
2) finish debugging Lagrangian.dat file 
/home/rmueller/project/rmueller/MIDOSS/MIDOSS-MOHID-config/MediumFloater/SOG_01dec2017/test3/Lagrangian1.dat
3) Python tutorial
4) Use surface currents to practice plotting up output in python
5) Read Dept. of Ecology Report

(1) With doug's help, created an error-log.md file

https://bitbucket.org/midoss/midoss-mohid-config/src/default/error-log.md

Basic instructions from Doug for creating the file:
* changed the file extension from .txt to .md so that Bitbucket will render it through Markdown (same markup as we us in Jupyter)

* delimited the stdout, Lagrangian.dat, etc. blocks with ``` before and after so that they are rendered as "code blocks"

* changed the 1), 2) enumerations to headings; # is level 1, ## is level 2, etc.

There's a good guide for Markdown syntax at https://guides.github.com/features/mastering-markdown/

(2) Finished debugging Lagrangian.dat file and submitted a 7-day test run 21107333
/home/rmueller/project/rmueller/MIDOSS/MIDOSS-MOHID-config/MediumFloater/SOG_01dec2017


5/15/19

Priorities: 
1) Figure out why Lagrangian.dat file isn't working
2) Python tutorial
3) Use surface currents to practice plotting up output in python
4) Read Dept. of Ecology Report

(1) I did two test runs yesterday
 - test2 and test3.  test3 seems to work and test2 not.  When I went to verify
 files on scratch, I couldn't find the folders.  Re-doing runs to make sure that MOHID is running with the files that I think it's running with. 

Deleted all folders/files on scratch

Re-submitted test3 -> test3_2
[rmueller@cedar5 test3]$ mohid run submit_run.yaml $PROJECT/rmueller/MIDOSS/results/MediumFloater/AKNS/SOG_01dec2017/test3_2
mohid_cmd.run INFO: Created temporary run directory /scratch/rmueller/MIDOSS/runs/MediumFloater/SOG_01dec17_MediumFloater_1000m3_7days_2019-05-15T100401.964998-0700
mohid_cmd.run INFO: Wrote job run script to /scratch/rmueller/MIDOSS/runs/MediumFloater/SOG_01dec17_MediumFloater_1000m3_7days_2019-05-15T100401.964998-0700/MOHID.sh
mohid_cmd.run INFO: Submitted batch job 21067603

The submit_run.yaml file on scratch shows that the correct Lagrangian file is being used:
PARTIC_DATA: $PROJECT/rmueller/MIDOSS/MIDOSS-MOHID-config/MediumFloater/SOG_01dec2017/test3/Lagran
gian1.dat


Re-submit test2 -> test2_2

[rmueller@cedar5 test2]$ mohid run submit_run.yaml $PROJECT/rmueller/MIDOSS/results/MediumFloater/AKNS/SOG_01dec2017/test2_2
mohid_cmd.run INFO: Created temporary run directory /scratch/rmueller/MIDOSS/runs/MediumFloater/SOG_01dec17_MediumFloater_1000m3_7days_2019-05-15T101056.799342-0700
mohid_cmd.run INFO: Wrote job run script to /scratch/rmueller/MIDOSS/runs/MediumFloater/SOG_01dec17_MediumFloater_1000m3_7days_2019-05-15T101056.799342-0700/MOHID.sh
mohid_cmd.run INFO: Submitted batch job 21068257

test3_2 worked.  test2_2 did not. 
Resubmitting test2_2 -> test 2_3 

Changes: 
(1) removed "!!" at the beginning of file to just one "!"
(2) removed "!***********************" at the beginning of file
 
[rmueller@cedar5 test2]$ mohid run submit_run.yaml $PROJECT/rmueller/MIDOSS/results/MediumFloater/AKNS/SOG_01dec2017/test2_3
mohid_cmd.run INFO: Created temporary run directory /scratch/rmueller/MIDOSS/runs/MediumFloater/SOG_01dec17_MediumFloater_1000m3_7days_2019-05-15T110228.719454-0700
mohid_cmd.run INFO: Wrote job run script to /scratch/rmueller/MIDOSS/runs/MediumFloater/SOG_01dec17_MediumFloater_1000m3_7days_2019-05-15T110228.719454-0700/MOHID.sh
mohid_cmd.run INFO: Submitted batch job 21071907

test2_3 still not working. -> test2_4
Removed all comments (except the header line) from this intro section

test2_5: remove spaces in first few lines

[rmueller@cedar5 test2]$ mohid run submit_run.yaml $PROJECT/rmueller/MIDOSS/results/MediumFloater/AKNS/SOG_01dec2017/test2_5
mohid_cmd.run INFO: Created temporary run directory /scratch/rmueller/MIDOSS/runs/MediumFloater/SOG_01dec17_MediumFloater_1000m3_7days_2019-05-15T113215.423230-0700
mohid_cmd.run INFO: Wrote job run script to /scratch/rmueller/MIDOSS/runs/MediumFloater/SOG_01dec17_MediumFloater_1000m3_7days_2019-05-15T113215.423230-0700/MOHID.sh
mohid_cmd.run INFO: Submitted batch job 21072577

test2_6: Removed comment after output_time

[rmueller@cedar5 test2]$ mohid run submit_run.yaml $PROJECT/rmueller/MIDOSS/results/MediumFloater/AKNS/SOG_01dec2017/test2_6
mohid_cmd.run INFO: Created temporary run directory /scratch/rmueller/MIDOSS/runs/MediumFloater/SOG_01dec17_MediumFloater_1000m3_7days_2019-05-15T113653.115856-0700
mohid_cmd.run INFO: Wrote job run script to /scratch/rmueller/MIDOSS/runs/MediumFloater/SOG_01dec17_MediumFloater_1000m3_7days_2019-05-15T113653.115856-0700/MOHID.sh
mohid_cmd.run INFO: Submitted batch job 21072633

IT WORKED!!!!  Okay...so MOHID does NOT like comments after variables in the 
header section.  

test2_7: Putting all other header information back but leaving out the comment after 
OUTPUT_TIME

I'll be damned.  It works!

Testing the Lagrangian_AKNS_crude.dat file, modified to remove comment after OUTPUT_TIME 

[rmueller@cedar5 SOG_01dec2017]$ vi submit_run_AKNScrude.yaml 
[rmueller@cedar5 SOG_01dec2017]$ vi Lagrangian_AKNS_crude.dat
[rmueller@cedar5 SOG_01dec2017]$ mohid run submit_run_AKNScrude.yaml $PROJECT/rmueller/MIDOSS/results/MediumFloater/AKNS/SOG_01dec2017/
nemo_cmd.prepare ERROR: /scratch/rmueller/MIDOSS/runs/MediumFloater/AKNS path from "paths: runs directory" key not found - please check your run description YAML file
[rmueller@cedar5 SOG_01dec2017]$ mkdir /scratch/rmueller/MIDOSS/runs/MediumFloater/AKNS
[rmueller@cedar5 SOG_01dec2017]$ mohid run submit_run_AKNScrude.yaml $PROJECT/rmueller/MIDOSS/results/MediumFloater/AKNS/SOG_01dec2017/
mohid_cmd.run INFO: Created temporary run directory /scratch/rmueller/MIDOSS/runs/MediumFloater/AKNS/SOG_01dec17_MediumFloater_1000m3_7days_2019-05-15T114641.739326-0700
mohid_cmd.run INFO: Wrote job run script to /scratch/rmueller/MIDOSS/runs/MediumFloater/AKNS/SOG_01dec17_MediumFloater_1000m3_7days_2019-05-15T114641.739326-0700/MOHID.sh
mohid_cmd.run INFO: Submitted batch job 21072772

NEW ERROR! WOOT! :-)
 Maximum of          256  characters is supported.
 String: EMULSIFICATIONMETHOD      : Mackay        ! Shihan: Do you have the ref
 erence for this?  Can you send it to me?  Either Mackay reference or Fingas 199
 5...I think? I don't have the original paper, but some relevant information can
  be found in the MOHID description
 File  : /home/rmueller/project/rmueller/MIDOSS/MIDOSS-MOHID-config/settings/Med
 iumFloaters/Lagrangian_AKNS_crude.dat
 Line  :          127
Ended run at Wed May 15 11:47:46 PDT 2019
Results hdf5 to netCDF4 conversion started at Wed May 15 11:47:46 PDT 2019

Removing long comment and resubmitting run 
[rmueller@cedar5 SOG_01dec2017]$ mohid run submit_run_AKNScrude.yaml $PROJECT/rmueller/MIDOSS/results/MediumFloater/AKNS/SOG_01dec2017/
nemo_cmd.prepare WARNING: There are uncommitted changes in /project/6001313/rmueller/MIDOSS/MIDOSS-MOHID-config
mohid_cmd.run INFO: Created temporary run directory /scratch/rmueller/MIDOSS/runs/MediumFloater/AKNS/SOG_01dec17_MediumFloater_1000m3_7days_2019-05-15T132525.811503-0700
mohid_cmd.run INFO: Wrote job run script to /scratch/rmueller/MIDOSS/runs/MediumFloater/AKNS/SOG_01dec17_MediumFloater_1000m3_7days_2019-05-15T132525.811503-0700/MOHID.sh
mohid_cmd.run INFO: Submitted batch job 21078049

ANOTHER NEW ERROR!  WOOT!

 Found : at the end of line.
 Line: ! Comments are added after parameter in this format:
Ended run at Wed May 15 13:26:27 PDT 2019

edited /home/rmueller/project/rmueller/MIDOSS/MIDOSS-MOHID-config/settings/MediumFloaters/Lagrangian_AKNS_crude.dat to remove ':" at end of this line and re-submitted. 
5/14/19
[rmueller@cedar5 SOG_01dec2017]$ mohid run submit_run_AKNScrude.yaml $PROJECT/rmueller/MIDOSS/results/MediumFloater/AKNS/SOG_01dec2017/
nemo_cmd.prepare WARNING: There are uncommitted changes in /project/6001313/rmueller/MIDOSS/MIDOSS-MOHID-config
mohid_cmd.run INFO: Created temporary run directory /scratch/rmueller/MIDOSS/runs/MediumFloater/AKNS/SOG_01dec17_MediumFloater_1000m3_7days_2019-05-15T133355.079018-0700
mohid_cmd.run INFO: Wrote job run script to /scratch/rmueller/MIDOSS/runs/MediumFloater/AKNS/SOG_01dec17_MediumFloater_1000m3_7days_2019-05-15T133355.079018-0700/MOHID.sh
mohid_cmd.run INFO: Submitted batch job 21078135

Found another : at end of comment line and needed to fix/re-run

[rmueller@cedar5 SOG_01dec2017]$ mohid run submit_run_AKNScrude.yaml $PROJECT/rmueller/MIDOSS/results/MediumFloater/AKNS/SOG_01dec2017/
nemo_cmd.prepare WARNING: There are uncommitted changes in /project/6001313/rmueller/MIDOSS/MIDOSS-MOHID-config
mohid_cmd.run INFO: Created temporary run directory /scratch/rmueller/MIDOSS/runs/MediumFloater/AKNS/SOG_01dec17_MediumFloater_1000m3_7days_2019-05-15T133723.122490-0700
mohid_cmd.run INFO: Wrote job run script to /scratch/rmueller/MIDOSS/runs/MediumFloater/AKNS/SOG_01dec17_MediumFloater_1000m3_7days_2019-05-15T133723.122490-0700/MOHID.sh
mohid_cmd.run INFO: Submitted batch job 21078278

This run crashed with no warning:

STDOUT:

 ---Assimilation     :            0
 
Ended run at Wed May 15 13:38:27 PDT 2019
Results hdf5 to netCDF4 conversion started at Wed May 15 13:38:27 PDT 2019

STDERR

CheckOriginInLandCell - ModuleLagrangianGlobal - ERR30

I noticed a ":" at the end of a comment in the <<BeginOil>> <<EndOil>> Section
Removed this ":" and am re-submitting code. 

UGH!  Can't figure this out.  Going back to test3 and moving forward from the working Lagrangian1.dat file. 

test3_3: Turned on BIODEGREDATION :1

[rmueller@cedar1 test3]$ mohid run submit_run.yaml $PROJECT/rmueller/MIDOSS/results/MediumFloater/AKNS/SOG_01dec2017/test3_3
nemo_cmd.prepare WARNING: There are uncommitted changes in /project/6001313/rmueller/MIDOSS/MIDOSS-MOHID-config
mohid_cmd.run INFO: Created temporary run directory /scratch/rmueller/MIDOSS/runs/MediumFloater/SOG_01dec17_MediumFloater_1000m3_7days_2019-05-15T144852.964972-0700
mohid_cmd.run INFO: Wrote job run script to /scratch/rmueller/MIDOSS/runs/MediumFloater/SOG_01dec17_MediumFloater_1000m3_7days_2019-05-15T144852.964972-0700/MOHID.sh
mohid_cmd.run INFO: Submitted batch job 21079273

SUCCESS!

test3_4: Changed dispersion method to NewDispersion

SUCCESS!

test3_5: Add BIODEGREDATION coefficients
ANALYTEPERCENTAGE         : 13.6 2.61 82.67 1.13 0.01
MOLEWEIGHT                : 9.29E01 1.057011494E02 3.687520866E02 1.761327434E02 1.3E02
VAPORPRESSURE             : 4.79E00 2.48E-02 1.01E-04 2.87E-05 6.93E-04
SOLUBILITY                : 2.307208456E01 3.465517241E02 5.3424E-06 8.259566372 5.1000E04
BIOCOE                    : 1.0E-01 1.0E-01 1.0487601E-02 2.9389381E-02 5.0E-03  

SUCCESS!

test3_6: Updated the oil properties to match Shihan's google doc. 
OILTYPE                   : Crude       ! [] Options: Crude or Refined
API                       : 29.9
POURPOINT                 : -54         ! Pour point [-] (ºC)
TEMPVISCREF               : 15.           ! Temperature of reference viscosity [-] (ºC)
VISCREF                   : 16.           ! Reference Dynamic Viscosity [-] (cP)
DT_OIL_INTPROCESSES       : 60  ! Time step for weathering processes, in seconds
OIL_TIMESERIE             : OilOutput

SUCCESS!

test3_7: Add the following (testing whether comments are an issue)
!~~~ Weathering parameters corresponding to flags ~~~
!!! *** OIL_SPREADING [1]  ***
SPREADINGMETHOD           : ThicknessGradient
USERCOEFVELMANCHA         : 10

SUCCESS!

test3_8: Adding the following.  Testing the impact of commenting out these variables

!!! *** OIL_EVAPORATION [1] ***
EVAPORATIONMETHOD         : EvaporativeExposure  ! [EvaporativeExposure] Options: EvaporativeExposure/PseudoComponents/Fingas

   ! Shihan: Did I get this right, that these are for the PseudoComponents method?
   ! If EVAPORATIONMETHOD: PseudoComponents, the following 4 parameters are required:
   !ASPHALTENECONTENT         : 5
   !WAXCONTENT                : 2.9
   !RESINCONTENT              : 9
   !SATURATECONTENT           : 52

   ! If EVAPORATIONMETHOD: Fingas, the following 3 parameters are required
   !FINGAS_EVAP_EQTYPE        : Logarithmic
   !FINGAS_EVAP_EMP_DATA      : 0
   !PERC_MASSDIST180          : 22


FATAL; KEYWORD; Subroutine OilOptions - ModuleOil_0D. ERR70.


This works:
!!! *** OIL_EVAPORATION [1] ***
!ASPHALTENECONTENT         : 5
!WAXCONTENT                : 2.9
!RESINCONTENT              : 9
!SATURATECONTENT           : 52

   ! If EVAPORATIONMETHOD: Fingas, the following 3 parameters are required
   !FINGAS_EVAP_EQTYPE        : Logarithmic
   !FINGAS_EVAP_EMP_DATA      : 0
   !PERC_MASSDIST180          : 22

ANALYTEPERCENTAGE         : 13.6 2.61 82.67 1.13 0.01
MOLEWEIGHT                : 9.29E01 1.057011494E02 3.687520866E02 1.761327434E02 1.3E02
VAPORPRESSURE             : 4.79E00 2.48E-02 1.01E-04 2.87E-05 6.93E-04
SOLUBILITY                : 2.307208456E01 3.465517241E02 5.3424E-06 8.259566372 5.1000E04
BIOCOE                    : 1.0E-01 1.0E-01 1.0487601E-02 2.9389381E-02 5.0E-03

but when I add: 
EVAPORATIONMETHOD         : EvaporativeExposure  ! [EvaporativeExposure] Options: EvaporativeExposure/PseudoComponents/Fingas

I get "FATAL; KEYWORD; Subroutine OilOptions - ModuleOil_0D. ERR70"


Test changing / -> , 

test_14


5/14/19

The runs I submitted yesterday didn't work, but I'm not sure why.  Re-trying the AKNScrude example over 1-day 

> mohid run submit_run_AKNScrude.yaml $PROJECT/rmueller/MIDOSS/results/MediumFloater/SOG_01dec2017/test7
def_allen was slow, so I'm trying rrg_allen....21018386
committed .yaml file: changeset:   80:389d8b00c432

Result (error): 

[rmueller@cedar5 test7]$ more stderr
ModuleEnterData - ConstructEnterData - ERR05
cp: cannot stat '/scratch/rmueller/MIDOSS/runs/MediumFloater/AKNS/SOG_01dec17_MediumFloater_1000
m3_7days_2019-05-14T104909.843731-0700/res/Lagrangian_SOG_01dec17_MediumFloater_1000m3_7days.hdf
5': No such file or directory
Usage: hdf5-to-netcdf4 [OPTIONS] HDF5_FILE NETCDF4_FILE
Try "hdf5-to-netcdf4 --help" for help.

Error: Invalid value for "HDF5_FILE": Path "/localscratch/rmueller.21018386.0/Lagrangian_SOG_01d
ec17_MediumFloater_1000m3_7days.hdf5" does not exist.
cp: cannot stat '/localscratch/rmueller.21018386.0/Lagrangian_SOG_01dec17_MediumFloater_1000m3_7
days.nc': No such file or directory
[rmueller@cedar5 test7]$ 

On line 150 of prepare.py

    results_dir = tmp_run_dir / "res"
    results_dir.mkdir()

Re-tracing steps to see where I went wrong.  I'm noticing that test5 used test1 Lagrangian.dat file (!), so 
I am re-doing test1 and stepping up from there...again.

TEST1: AKNS crude
> mohid run submit_run.yaml $PROJECT/rmueller/MIDOSS/results/MediumFloater/AKNS/SOG_01dec2017/test1
mohid_cmd.run INFO: Created temporary run directory /scratch/rmueller/MIDOSS/runs/MediumFloater/SOG_01dec17_MediumFloater_1000m3_7days_2019-05-14T113649.899990-0700
mohid_cmd.run INFO: Wrote job run script to /scratch/rmueller/MIDOSS/runs/MediumFloater/SOG_01dec17_MediumFloater_1000m3_7days_2019-05-14T113649.899990-0700/MOHID.sh
mohid_cmd.run INFO: Submitted batch job 21019441


results look good.  The run was stepping through and was terminated due to wall time limit

TEST2: Changed submit_run.yaml to point to Lagrangian.dat file in test2 directory instead of test1

[rmueller@cedar1 test2]$ mohid run submit_run.yaml $PROJECT/rmueller/MIDOSS/results/MediumFloater/AKNS/SOG_01dec2017/test2
mohid_cmd.run INFO: Created temporary run directory /scratch/rmueller/MIDOSS/runs/MediumFloater/SOG_01dec17_MediumFloater_1000m3_7days_2019-05-14T140329.371725-0700
mohid_cmd.run INFO: Wrote job run script to /scratch/rmueller/MIDOSS/runs/MediumFloater/SOG_01dec17_MediumFloater_1000m3_7days_2019-05-14T140329.371725-0700/MOHID.sh
mohid_cmd.run INFO: Submitted batch job 21025458

** Typo in Lagrangian.dat file path -> needed to re-submit.
[rmueller@cedar5 test2]$ mohid run submit_run.yaml $PROJECT/rmueller/MIDOSS/results/MediumFloater/AKNS/SOG_01dec2017/test2
mohid_cmd.run INFO: Created temporary run directory /scratch/rmueller/MIDOSS/runs/MediumFloater/SOG_01dec17_MediumFloater_1000m3_7days_2019-05-14T171024.402666-0700
mohid_cmd.run INFO: Wrote job run script to /scratch/rmueller/MIDOSS/runs/MediumFloater/SOG_01dec17_MediumFloater_1000m3_7days_2019-05-14T171024.402666-0700/MOHID.sh
mohid_cmd.run INFO: Submitted batch job 21028648

FATAL; INTERNAL; OutPutTimeInternal - EnterData - ERR02.

*******

copied Lagrangian.dat from "test1" and changed only the part before <BeginOrigin>, calling it Lagrangian1.dat

[rmueller@cedar5 test2]$ mohid run submit_run.yaml $PROJECT/rmueller/MIDOSS/results/MediumFloater/AKNS/SOG_01dec2017/test2

mohid_cmd.run INFO: Created temporary run directory /scratch/rmueller/MIDOSS/runs/MediumFloater/SOG_01dec17_MediumFloater_1000m3_7days_2019-05-14T174002.343913-0700
mohid_cmd.run INFO: Wrote job run script to /scratch/rmueller/MIDOSS/runs/MediumFloater/SOG_01dec17_MediumFloater_1000m3_7days_2019-05-14T174002.343913-0700/MOHID.sh
mohid_cmd.run INFO: Submitted batch job 21030089

Final Particle Conditions.                                                                                                      
Keyword: PARTIC_FIN not found

 Registered Instance: EnterData
 Instance ID        :            2
 
 
Initial Particle Conditions.                                                                                                    
Keyword: PARTIC_INI not found

FATAL      INTERNAL   OutPutTimeInternal - EnterData - ERR02.

****

test3
Copied lines 63 - 81 of test2/Lagrangian to the beginning of <<BeginOil>> in test1/Lagrangian.  This becomes test3, saved as test3/Lagrangian1.dat

[rmueller@cedar1 test3]$ mohid run submit_run.yaml $PROJECT/rmueller/MIDOSS/results/MediumFloater/AKNS/SOG_01dec2017/test3
mohid_cmd.run INFO: Created temporary run directory /scratch/rmueller/MIDOSS/runs/MediumFloater/SOG_01dec17_MediumFloater_1000m3_7days_2019-05-14T175016.132871-0700
mohid_cmd.run INFO: Wrote job run script to /scratch/rmueller/MIDOSS/runs/MediumFloater/SOG_01dec17_MediumFloater_1000m3_7days_2019-05-14T175016.132871-0700/MOHID.sh
mohid_cmd.run INFO: Submitted batch job 21031754

TEST3: Changed submit_run.yaml to point to Lagrangian.dat file in test3 directory instead of test1

[rmueller@cedar5 test3]$ mohid run submit_run.yaml $PROJECT/rmueller/MIDOSS/results/MediumFloater/AKNS/SOG_01dec2017/test3
mohid_cmd.run INFO: Created temporary run directory /scratch/rmueller/MIDOSS/runs/MediumFloater/SOG_01dec17_MediumFloater_1000m3_7days_2019-05-14T140607.986285-0700
mohid_cmd.run INFO: Wrote job run script to /scratch/rmueller/MIDOSS/runs/MediumFloater/SOG_01dec17_MediumFloater_1000m3_7days_2019-05-14T140607.986285-0700/MOHID.sh
mohid_cmd.run INFO: Submitted batch job 21025563

TEST4: Changed submit_run.yaml to point to Lagrangian.dat file in test4 directory instead of test1

mohid run submit_run.yaml $PROJECT/rmueller/MIDOSS/results/MediumFloater/AKNS/SOG_01dec2017/test4
mohid_cmd.run INFO: Created temporary run directory /scratch/rmueller/MIDOSS/runs/MediumFloater/SOG_01dec17_MediumFloater_1000m3_7days_2019-05-14T140651.567810-0700
mohid_cmd.run INFO: Wrote job run script to /scratch/rmueller/MIDOSS/runs/MediumFloater/SOG_01dec17_MediumFloater_1000m3_7days_2019-05-14T140651.567810-0700/MOHID.sh
mohid_cmd.run INFO: Submitted batch job 21025567

TEST5: Changed submit_run.yaml to point to Lagrangian.dat file in test5 directory instead of test1

[rmueller@cedar5 test5]$ mohid run submit_run.yaml $PROJECT/rmueller/MIDOSS/results/MediumFloater/AKNS/SOG_01dec2017/test5
mohid_cmd.run INFO: Created temporary run directory /scratch/rmueller/MIDOSS/runs/MediumFloater/SOG_01dec17_MediumFloater_1000m3_7days_2019-05-14T140806.007211-0700
mohid_cmd.run INFO: Wrote job run script to /scratch/rmueller/MIDOSS/runs/MediumFloater/SOG_01dec17_MediumFloater_1000m3_7days_2019-05-14T140806.007211-0700/MOHID.sh
mohid_cmd.run INFO: Submitted batch job 21025583



5/13/19

Priorities:
1) Finish Lagrangian.dat files
2) Submit test runs for Light Evaporators (Gasoline, Diesel, Jet fuel), Medium Evaporator (South Louisianna Sweet), diluted Bitumen (Cold Lake Blend), Medium Floater (AK N. Slope Crude) and Heavy Floater (Bunker C).  
3) Finish JGR Review
4) Apply for Ocean Hack Week 

(1) Merged conflicts with Shihan's update to Lagrangian files.  Reviewed/corrected Lagrangian files. 
    	Created directories for LightEvaporators (and Lagrangian files for diesel, jet fuel, gas), 
	Medium Evaporators (and Lagrangian file for S. Louisiana Sweet crude) and MediumFloaters (AKNS crude)
(2) Testing 7-day run with AKNS Lagrangian file and all other settings/files equal to Ashu's setup
   	/home/rmueller/project/rmueller/MIDOSS/MIDOSS-MOHID-config/MediumFloater/SOG_01dec2017
	Submitted run 20985003: mohid run submit_run.yaml $PROJECT/rmueller/MIDOSS/results/MediumFloater/SOG_01dec2017/  

	Diesel: Job submission 20985421
	Jet Fuel: 20985419
        Gasoline: 20985417.  
MOHID-Cmd is calling hdf5-to-netcdf even though no hdf5 file exists.  No model error to indicate why there was this mistake. 

From Stderr:
ConstructHDFPredictDTMethod1 - ModuleFillMatrix - ERR50
cp: cannot stat '/scratch/rmueller/MIDOSS/runs/LightEvaporators/SOG_01dec17_LightEvapora
torGas_1000m3_7days_2019-05-13T122449.114951-0700/res/Lagrangian_SOG_01dec17_LightEvapor
atorGas_1000m3_7days.hdf5': No such file or directory
Usage: hdf5-to-netcdf4 [OPTIONS] HDF5_FILE NETCDF4_FILE
Try "hdf5-to-netcdf4 --help" for help.

Error: Invalid value for "HDF5_FILE": Path "/localscratch/rmueller.20985417.0/Lagrangian
_SOG_01dec17_LightEvaporatorGas_1000m3_7days.hdf5" does not exist.
cp: cannot stat '/localscratch/rmueller.20985417.0/Lagrangian_SOG_01dec17_LightEvaporato
rGas_1000m3_7days.nc': No such file or directory

(3) Submitted JGR review
(4) Applied for Oceanhack week    

5/9/19

Priorities:
1)  Work with Shihan in creating lagrangian.dat files for oil types and "fine combing" 
    parameter choices
2)  VVL diagnostics: plot bathymetry.dat files (after converting to netcdf) to
  see what the MOHID adjustments are.
3)  Start JGR review that is due Monday (!!!)

Test5 (submitted jobID 20768514 - Successully terminated): Changed Dispersion method to "NewDispersion" and added comments about the dispersion methods.  Sent email to Shihan to make sure my comments were/are accurate. 

Test6 (submitted job 20789924 - Successfully terminated): Changed ACCIDENT_METHOD from 1 to "Fay" per Shihan's correction
Commented out the following, as Shihan says they aren't needed for EvaporationExposure method of evaporation
   !ASPHALTENECONTENT         : 1.27
   !WAXCONTENT                : 2.9
   !RESINCONTENT              : 6.1
   !SATURATECONTENT           : 75.0


Questions: 
1) Do we want Stoke's drift on? 
2) What value for winddriftangle?  I suggest 0.0
3) What value for WindCoef?  From Li et al. (2014): From empirical data, 
the wind drift coefficient, i.e., the magnitude of wind-driven current induced 
by wind stress is approximately 0.03 of the wind speed at 10 m height and its 
direction can be assumed as nearly parallel to the wind direction [15], [16], [17]. 
Abascal et al. [18] used a set of drifting buoys during the 2002 Prestige 
oil spill in the Bay of Biscay, Spain to calibrate and validate the 
oil transport model together with meteorological data, indicating that the 
wind drag coefficient was linearly proportional to the wind speed under strong 
tidal currents, ranging from approximately 0.02 to 0.04 with the 
mean value of 0.027

I propose using a value of 0.027.

4) What value of WINDDRIFTANGLE?  I propose 3 based on Susan's email. 


5/8/19

MOHID insights:

[Shihan, email on 5/7/19]
For most of oil types we can choose Mackay's method right now, as long as the maximum water content is available. In theory, the Fingas's method should be more advanced, but I found there's some problems with this algorithm in the code, which I promised that I will try to fix it. At this moment, I think we can use Mackay's method

I added properties for jet fuel and gas oil in that one, also changed the dispersion method to "NewDispersion"

[Susan, email 5/8/19]
Consensus at this meeting (OceanPredict) seems to be 3% of the wind for oil.*  The angle actually seems to depend on the ocean model!  This is from Graig Sutherland in particular.

* most of this is Stokes drift, if we include this separately from the wave model, we will need to decrease that 3%

test2: Changed Lagrangian.dat to reflect the parameters within <<BeginOil>> section of /home/rmueller/project/rmueller/MIDOSS/MIDOSS-MOHID-config/MediumFloater/SOG_01dec2017/Lagrangian_AKNS_crude_shihan.dat

/home/rmueller/project/rmueller/MIDOSS/MIDOSS-MOHID-config/MediumFloater/SOG_01dec2017/test2

submitted run (20745795) to ensure I didn't break anything.  SUCCESS! :-)

test3: Turn on biodegredation.  Submitted run (20748108)
I think it ran successfully.  stdout looked good.  Stderr gave this message
slurmstepd: error: *** JOB 20698561 ON cdr813 CANCELLED AT 2019-05-07T16:47:08 ***

test4: Added more comments and changed order a little more. Submitted run to make sure I didn't break anything (20750016)

5/7/19

Started series of runs to test setup files 
/home/rmueller/project/rmueller/MIDOSS/MIDOSS-MOHID-config/MediumFloater/SOG_01dec2017
20698561 : Uses Ashu's Lagrangian.dat file [succesfully ran]
/home/rmueller/project/rmueller/MIDOSS/MIDOSS-MOHID-config/MediumFloater/SOG_01dec2017/test1
20700743 : Moved weathering flags to top of <<BeginOil>> section. 12 hour run. 

/home/rmueller/project/rmueller/MIDOSS/MIDOSS-MOHID-config/MediumFloater/SOG_01dec2017/test2
  : Added comments from Lagrangian_AKNS_crude_shihan.dat


5/6/19

Priorities:
1) Python tutorials 
2)  Create lagrangian.dat files for oil types
3)  VVL diagnostics: plot bathymetry.dat files (after converting to netcdf) to 
  see what the MOHID adjustments are.  

1) Worked through more of Udemy online course.  Ashu sent link to a book he likdes: http://greenteapress.com/wp/think-python-2e/.  Bookmarked to review

2) Noticing big differences in the Lagrangian.dat files that Ashu was running vs. the ones that Shihan has used.  Ashu's files are missing biodegredation coefficients.  I noticed this looking into the output file on flags used.  
The model worked because biodegredation was turned off. 

-Creating a new run directory with more explicit oil type (MediumFloater) and date tag (SOG_11dec2017).  
   /home/rmueller/project/rmueller/MIDOSS/MIDOSS-MOHID-config/MediumFloater/SOG_11dec2017
- This new directory will be used for testing a cleaned up lagrangian.dat file by replicating the working run that I copied from Ashu's run directory
- Files are copied from 
  /home/rmueller/project/rmueller/MIDOSS/MIDOSS-MOHID-config/MF0/SOG12117
- The only file that I change is Lagrangian .dat and submit_run.yaml

submit_run.yaml:
- run_id: SOG_01dec17_MediumFloater_1000m3_7days
- PARTIC_DATA: $PROJECT/rmueller/MIDOSS/MIDOSS-MOHID-config/MediumFloater/SOG_01dec2017/Lagrangian.dat
- runs directory: $SCRATCH/MIDOSS/runs/MediumFloater/

Lagrangian.dat:
- copied and modified from /home/rmueller/project/rmueller/MIDOSS/MIDOSS-MOHID-config/Shihan/clean to create:
/home/rmueller/project/rmueller/MIDOSS/MIDOSS-MOHID-config/MediumFloater/SOG_11dec2017/Lagrangian.dat

Submitted run using this Lagrangian file. JobID: 20653204


5/3/19
*** updating runs ***
use, e.g., 
> hg log Atmosphere.dat
to see commits for this .dat file and to select version for run
HRDPS winds (24:ae8f61605212)
WaterProperties.dat: SalishSeaCast temperature and Salinity (56:8a1b20344ecf)
Hydrodynamic: SSH (54:d94ca2dc478c)


*** MIDOSS-MOHID-grid ***
Added the MOHID grid files to the repo "MIDOSS-MOHID-grid"
Ashu added the weighting files for interpolating ww3 and hrdps output

*** ssh agent on cedar ***
Kept being prompted for passphrase when pushing or pulling to bitbucket
Resolved by: 
eval $(ssh-agent)
ssh-add
Look in 1-password under computecanada for passphrase if/when needed again

*** analysis-ashutosh****
Make HDF5 files:
The files are created using make-hdf5.yaml. 
Ashu added to repo: 
  wind_weights: ./MOHID_winds_weights.nc
  wave_weights: ./ww3_weighting_matrix_hake.nc
May want to move these to grid repo...created a MIDOSS-MOHID-grid repository
cd analysis-ashutosh/scripts
vi make-hdf5.yaml (enter date range)
python make_hdf5.py

ModuleNotFoundError: No module named 'salishsea_tools'
needed to update Smelt configuration with:
 cd /ocean/$USER/MEOPAR
hg clone ssh://hg@bitbucket.org/salishsea/tools
pip install --user --editable tools/SalishSeaTools

ModuleNotFoundError: No module named 'progressbar'
pip install progressbar2

Visualizing output:
mohid_diagnostic_tools/visualise_mohid_output.ipynb



****
Running MOHID with a new bathymetry.  

bathymetry: /home/rmueller/Data/SalishSeaCast/grid/AfterNEMOBathy201702_rdm.dat

MOHID changes the bathymetry upon initialization and creates a modified bathymetry that then needs to be copied and/or referenced with MOHID run(s). 

First run a 10-20 minute initialization run to just get the bathymetry correct: 
hg revert -r 59 submit_run.yaml
mohid run submit_run.yaml $PROJECT/rmueller/MIDOSS/results/MF0/vvl/nemo
submitted batch 20413321

from $PROJECT/rmueller/MIDOSS/results/MF0/vvl/nemo/stdout file: 
A new Bathymetry has been created, which consists with the geometry
 Modify the file Nomfich.dat and Re-run the model
 New Bathymetry file : 
 /home/rmueller/Data/SalishSeaCast/grid/AfterNEMOBathy201702_rdm_v01.dat

copied all files in $PROJECT/rmueller/MIDOSS/results/MF0/vvl/nemo
to 
$PROJECT/rmueller/MIDOSS/results/MF0/vvl/nemo/init_run

submitted a new job (20428852) using wall time of 1:30hrs and the MOHID-adjusted bathymetry:

bathymetry: /home/rmueller/Data/SalishSeaCast/grid/AfterNEMOBathy201702_rdm_v01.dat

Result: A new Bathymetry has been created, with isolated cells removed
 Modify the file Nomfich.dat and Re-run the model
 New Bathymetry file : 
 /home/rmueller/Data/SalishSeaCast/grid/AfterNEMOBathy201702_rdm_v02.dat

resubmited run to start with this 2x revised bathymetry: 20430107

Ashu says it's sometimes faster to run interactively and sometimes faster detatched.  Check. 

While initializing bathymetry, use run_time of 0:10:00 until the run moves beyond initialization.  This iterative process can take 1 time or many times. Unknown.
**I was having trouble with my RSA key, so I deleted files in ~/.ssh on Cedar and started over **
After deleting files on CEDAR, I ran the following command on SMELT
ssh-copy-id -i $HOME/.ssh/id_rsa cedar

when prompted, I entered my ComputeCanada password and tested with some hg commands that added more information to public key but then I got this error:


 hg commit submit_run.yaml -m "Updated submit_run.yaml to use 2x MOHID modified bathymetry, AfterNEMOBathy201702_rdm_v02.dat"
[rmueller@cedar5 test_vvl]$ hg pull --rebase
pulling from ssh://hg@bitbucket.org/midoss/midoss-mohid-config
remote: Permission denied (publickey).
abort: no suitable response from remote hg!


running interactively:
> mohid run submit_run.yaml $PROJECT/rmueller/MIDOSS/results/MF0/vvl/nemo --no-submit
cd to temporary run directory, e.g.:
> cd /scratch/rmueller/MIDOSS/runs/MF0/vvl_sshneg2_2019-05-03T093359.354600-0700
> salloc --time=0:10:0 --cpus-per-task=1 --mem-per-cpu=4096m --account=def-allen
> ./MohidWater.exe
When completed, exit from interactive node:
> exit

MOHID.sh is the shell script to modify for changing if/when files are deleted/converted/etc. 
to run from MOHID.sh, the command is something like:
> sbatch MOHID.sh ?

_v04 bathymetry yields the following error:
 -------------------------- MOHID -------------------------
 
 Constructing Mohid Water
 Please Wait...
 -------------------------- MODEL -------------------------
 
 Constructing      : 
 ID                :            1
 
 OPENMP: Max number of threads available is            1
 OPENMP: Number of threads requested is           12
 <Compilation Options Warning>
 OPENMP: Number of threads implemented is            1
Killed

Repeated with same results
AfterNEMOBathy201702.nc needs to be changed to have land values = -99 then re-create AfterNEMOBathy201702.dat and re-try


5/2/19

Updated MIDOSS-MOHID-CODE and ran a clean build
./compile_mohid.sh -c 
followed by a build
./compile_mohid.sh -mb1 -mb2 -mw

vvl bathymetry update run output to:
/home/rmueller/project/rmueller/MIDOSS/results/MF0/test


~ Today (in 2064)~
11-12: Document WW3 interpolation methodology (we can do this together)
1p-2:30/3: Review climatology and refine selection.  Run through the creation of HDF5 input files
(break)
3-5: setup and run cases for VVL with NEMO bathymetry, as well as some new climatology test cases. 

~ Friday (in 2064 and 3064) ~
9 or 10-12 (2064): Create a storyline for VVL test case
12-1p: Lunch
1-2p (3064): Whatever is most needed

5/1/19
Shihan: 
- compare Johansen et al. (2015), Delvigne and Sweeney (1988) and OSCAR model to see how the different dispersion methods measure up to industry standards.
- Per email communication: The motivation to switch to Johansen et al (2015) is because it includes more testing and validation than the 1988 parameterization.  

4/25/19
Location for cleaned up Lagrangian.dat file 
/home/rmueller/project/rmueller/MIDOSS/MIDOSS-MOHID-config/Shihan/clean

4/20/19

Finished draft of MEOPAR abstract
Sent Krista an email with meeting overview. 

4/19/2019

Updated ship classification with oil volume estimates
https://docs.google.com/spreadsheets/d/1G2DYXY7prpQACmWRYPmc_ZVfn9HzVZY23ATr8poGtIA/edit#gid=872104409

Started MEOPAR abstract

4/18/19

Meet with Krista:

Ship classification
https://docs.google.com/spreadsheets/d/1G2DYXY7prpQACmWRYPmc_ZVfn9HzVZY23ATr8poGtIA/edit#gid=872104409

Vessel Track Density Methodology
https://docs.google.com/document/d/1-5q66g5urRAUnOXRYj-TcJnkWyPnZUjDjzZlPHD0bo8/edit

Merge with Haibo's classifications
https://docs.google.com/drawings/d/198nZehBWuXNvcAd_dev3alJB6Mp-DsGjsEWQTDOWhT0/edit

Original questions: 
1) Where oil is transported?
2) What volume to spill?

Krista has oil volume by AIS shiptype and vessel length.  Use AIS data to create a histogram of number of AIS tracks binned by spill volume potential (by linking AIS shiptype and ship length with spill volume)

Do this histogram by oil type. 
-Create map of oil transport by oil type
-Run map and information by Shell oil contact to see if it's consistent with his understanding of oil transport.

Request: 
1) Points in SOG, TP and SB that intersect with ship tracks. Give lat/lon of current locations
2) Average length of Tankers, ATBs, Bulk Carriers and Container Ships (to get estimate of increase, by gallons, of oil moving over Salish Sea if all expansion projects go through.

4/17/19
Correct bathymetry.  
MOHID sets boundaries to zero, so is it a problem that NEMO-adjusted grid has zeros along the boundary? 


Meeting with Shihan, Ashu and Xiaomei.  
Discuss:
- Test case(s)
- Validation with Oscar

Shihan: 50 runs over the past few days.  One run crashed.  Still a problem in 
converting z to k (depth issue). Shihan is using lots of particles (1500).  
A particle may have gone to a place not covered by domain. Checking algorithms for oil concentration.  Did some modifications during biodegredation work.  
May have made a change that needs to be corrected.  The pattern would be the 
same but a differnt magnitude.  Checked unmodified code and is trying to figure out the way the original mohid fixes concentration.  Max. conc. with current version is > 100 kg/m3.  When Shihan changed to original version the outcome was 9 kg/m3. Trying to figure out the correct one. 
Hopes to update/firm up by next week. 
fmevaporate, fmdisperse, fmbiodegredated is for entire mass of oil, not single 
particle.  
Shihan will have access to Oscar next month to check what Oscar concentrations
are and to determine oil groups (for biodegredation) from Oscar database  

Oscar doesn't allow for WW3 input or VVL

Comparison runs: MOHID with VVL, MOHID without VVL, Oscar (without VVL) -- need hydrodynamic input rotate to lat/lon directions and use constant temperature and salinity, flat SSH (?). 
Oscar results are only visible in the software.  
The only exported result is oil mass balance.  
Oscar model also plots profiles of concentration within the software (doesn't export).  

Single precision or double precision version.  Single is much quicker.  How can we use single precision in MOHID on Cedar? 

Still using the original bathymetry, not the NEMO-adjusted bathymetry. 
Delvinge algorithm needs correction.  It's still using the empirical algorithm for calculating wave height and period from the winds rather than from WW3.   


Ashu: 3D dissolution is zero everywhere. Shihan uses .sro file to plot net dissolution vs. time. Shihan's results have dissolution values, albeit small. 

Xiaomei: 
- Discussed OPA aggregates with Haibo.  Need to first understand the whole 
process of sedimentation, including OPA formation and sinking.  Haibo thinks 
we should first use a simple formula to demonstrate this process and then
work toward including the complexity of OPA break-down.  She has been gathering
information 

- Plans to develop equations to calculate distribution of OPA diameter.  If we 
have oil droplet size and concentration and particle size and distribution then can determine OPA size, which can be used to calculate sinking rate. 

To do: 
- Get Shihan the NEMO-adjusted bathymetry. 
- Start a conversation with Shihan and Ashu regarding model validation


4/16/19

Graham setup (from Doug's 09-Apr-2019 MEOPAR group meeting):
project/ and nearline/ have both def-allen/ and rrg-allen/ trees which are separate; use $HOME/projects/def-allen/ and $HOME/nearline/def-allen/
Forcing tree is in $HOME/projects/def-allen/SalishSea/forcing/ or $PROJECT/SalishSea/forcing/ Please put export PROJECT=$HOME/projects/def-allen in your .bash_profile to ensure that $PROJECT is defined correctly. It is automatically updated daily by the nowcast system. It has the same directory structure as on cedar, so YAML file forcing sections shouldn't need to change.


4/15/19
Plotted up differences between NEMO-adjusted grid and original 201702 grid
/Users/rmueller/Projects/MIDOSS/analysis-rachael/matlab/grid/NEMOadjusted_grid_comparison.png

4/14/19
Reviewed Ashu's presentation and sent him an email with suggestions.

4/8/19
Next: 
1) Compare bathymetry between NEMO-adjusted and original
2) Update model download & run
3) Finish "clean" version(s) of initial .dat files
4) Write methodology from initial .dat files
5) Oil in WA 

4/5/19

Submitted 
/home/rmueller/project/rmueller/MIDOSS/MIDOSS-MOHID-config/MF0/SOG12117/submit_run.yaml

4/4/19
 'particle bigger than domain' error

4/3/2019
Time stepping: 


* Ashu motified .py script for creating e3t input so that masking is from "tmask" variable in 3D mesh mask

* Ashu did a run with DT_OIL = 60s and all other DT = 3600s.  NO_INTERPOLATION = 1. Using the new bathymetry file with land values = -99.  Oil moved in the run but then crashed after ~2 days. 


* Shihan has never used DT_OIL = 1200s.  He uses DT_OIL = 60s.  

* Model setup and test cases:

OUTPUT_TIME = DT_PARTIC = 1200s
DT_OIL = 60s

Test whether DT_PARTIC = 60s changes dynamics/oil advection. 

* LAYERTHICKNESS in Geometry.dat is used to initialize geometry and to set MOHID land/water points. 

* The level thicknesses in LAYERTHICKNESS are not the same as in NEMO b/c of a line length limit in MOHID .dat setting files that has prevented Shihan from putting in the exact values.  He has modified the values to work with the line length limitation.

*After model initialization, e3t is used to define level thickness as well as water/land points

* [Because LAYERTHICKNESS is used to create the initial model geometry, and because there is a line length limit that prevents us from using the actual NEMO levels, there may be a differece between the MOHID land  mask and NEMO land mask (where the sum of level thickness in MOHID doesn't match that in NEMO).  I’m still not sure if/how this may cause problems in the code if e3t is used to define land/water points after initialization, but I think it’s important to mention here.]

* e3t output is different from other output (e.g. salinity) in that other output (e.g. salinity) has values in land masked regions set to zero whereas e3t output has land values set to a default e3t value.  (I haven’t yet plotted this up yet but from the e3t on ERDAPP I’m seeing that the surface value is 1 everywhere, on land and ocean and that the standard land value changes with depth.) As such, output e3t has non-zero values where MOHID expected land (based on initialized geometry) and in places where other NEMO output (e.g. salinity) is set to zero.  Using e3t for land/water boundary after initialization was causing a problem b/c it doesn’t delineate between land and water in the same way as, e.g., salinity.

* The fix has been to multiply the output e3t by the land mask used by salinity so that there are now zeros everywhere that salinity output has zeros.  

* Can SalishSeaCast be modified so that e3t values are output with zero where there is land in order to eliminate this extra step? 

* Shihan’s has a running version of the code with the modified e3t that does not include temperature and salinity inputs.  

* Ashu created this modified e3t.hdf5 file and tried running the newest version of the code with all forcing files (including temperature and salinity), but it failed due to a overly light (less dense) water causing sinking oil. 

Ashu's run has fatal error after first time step:
-------------------------- MOHID -------------------------
 
 Running MOHID, please wait...
 
 
FATAL; INTERNAL; Function  F_FayArea - ModuleOil_0D. ERR02.


* Shihan is currently testing the new version on his end using temperature and salinity inputs. 

* Shihan is also testing the new version with Ashu’s e3t.hdf5 file, setup and forcings

4/2/2019
Understanding VVL code development.  Here is where we are at:
1) Ashu has compiled and run the model.  It's not moving oil.
2) Shihan has compiled and run the model.  When he runs the current version, oil does move even though the current version is likely not stable. He warns that it may crash.
3) Shihan compared DWZ using his new "Imposed VVL" method and found that the 
NEMO e3t has ocean values where MOHID has land. 
4) DWZ and e3t not comparable in pre-"Imposed VVL" versions.  
5) MOHID considers land where NEMO considers water…or visa versa?  I can see a problem arising if MOHID is calculating for what it sees as water points where NEMO has land (and no information), but I have a hard time understanding how the reverse is a problem.  

SHIHAN: Yes, there're a some points, that the 2 models define differently (water or land, especially for deep levels). For example, cell A is water in NEMO, has a e3t with 26m. MOHID defined A as land point (computed from bathymetry.dat and geometry.dat); then the output DWZ of A is the FillValue -9.9*10^(-15); When I did the comparison, I made all fillvalues as 0. As a result, e3t-DWZ=26m, and you will see places with non-zero value in my comparison. Reversely, if the NEMO defined it as land, while MOHID defined as water, I turned the water points to land points, and there won't be a problem. 

6) You have noticed that e3t has a different value-extent (distinguishing land and water) than the NEMO grid…did I get that right?  (If so then it may be a problem on our end that needs to be sorted out, and I will do some plots to investigate further. )

SHIHAN: Considering the 3 question, the DWZ from MOHID, if the point is not zero or fillvalue, it should have the same value with e3t; The non-zero value in my comparison figures is caused by 0 value for DWZ, and non-zero value for e3t.

My (emailed) questions for Shihan:
Here is what I find puzzling (which you don’t have to respond to today; we can discuss tomorrow): 

(1) MOHID shouldn’t care about NEMO points where MOHID sees land so why is it a problem for NEMO to have ocean points where MOHID has land points?  
(2) Land points based on NEMO bathymetry file ought to be the same as land points in e3t.  I am curious about why these are different. 

Can you please verify (this too can wait until tomorrow) which NEMO grid your bathymetry.dat and geometry.dat files are based on? 


Geometry.dat settings:

MINIMUMDEPTH              : 0.1
FACESOPTION               : 2
INITIALIZATION_METHOD     : CARTESIAN


!Cartesian Domain
<begindomain>
ID                        : 1
INITIALIZATION_METHOD     : CARTESIAN
TYPE                      : CARTESIAN
LAYERS                    : 40
LAYERTHICKNESS            : 27 27 27 27 27 27 27 27 27 26 26 24 23 22 18 14 10 6 4 3 2 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
DOMAINDEPTH               : 428
!MININITIALLAYERTHICKNESS  : 0.5
!LAGRANGIAN                : 1
ImposedVVL                : 1

!MINEVOLVELAYERTHICKNESS   : 0.5
FILENAME                  : I:\UBC file\e3t3.hdf5
<enddomain>


* worked with Doug to understand why hdf5-to-netcdf4 isn't working.  We changed one word on line 252 of the code and it works fine
datetime -> naive

252    time_step = getattr(hdf5_file.root.Time, f"Time_{index:05d}")
253    time_coord = xarray.DataArray(
254        name="time",
255        data=[arrow.get(*time_step.read().astype(int)).naive],

252 Takes the Time_00000 (05d numeric value) attribute and stores into time_step 
such that,e.g., time_step = array(["2017","12","01","00","30"])

255 time_step.read().astype(int): converts from string array to integer array or array([2017, 12, ...])
    "naive" says that it doesn't need to know the date format, which is okay because we are all UTC
    * converts from array to function input format such that ([2017,12,...]) -> (2017,12,...)
    arrow is a library that for manipulating and formating date and time information. 


4/1/2019
- Created spreadsheet to compare runs
- Emailed Ashu for update
- Tried running hdf5-to-netcdf4 but am still getting errors.

3/30/19
Trying to debug problem with converting HDF5 -> netcdf
        $ rm -rf .local
        $ cd $PROJECT/$USER/MIDOSS/
        $ pip3 install --user -e moad_tools

Ran into a problem with netcdf4 install that appears to have resolved....

Failed to build netCDF4
Installing collected packages: six, python-dateutil, arrow, Click, pyparsing, cycler, kiwisolver, numpy, matplotlib, cftime, netCDF4, pytz, pandas, scipy, numexpr, tables, xarray, moad-tools
  Running setup.py install for netCDF4 ... done
  Running setup.py develop for moad-tools
Successfully installed Click-7.0 arrow-0.13.1 cftime-1.0.3.4 cycler-0.10.0 kiwisolver-1.0.1 matplotlib-3.0.2 moad-tools netCDF4-1.5.0 numexpr-2.6.9 numpy-1.16.2 pandas-0.24.1 pyparsing-2.3.1 python-dateutil-2.8.0 pytz-2018.9 scipy-1.2.1 six-1.12.0 tables-3.4.4 xarray-0.12.0

        $ hdf5-to-netcdf4 --help
        $ pip install --user -e NEMO-Cmd/
        $ pip install --user -e MOHID-Cmd/

3/28/19

* copied Ashu's .yaml file to my MIDOSS directory. 
cp $PROJECT/abhudia/MIDOSS/MIDOSS-MOHID-config/MF0/SOG12117/* ./

* changed .yaml to use MIDOSS-MOHID and to use readable paths
vi SOGa_01dec17_MF0_1000m3_7days_const_w_unrotated_smalldt.yaml
$PROJECT/$USER/MIDOSS/MIDOSS-MOHID/
:%s/\/home\/abhudia\/project/$PROJECT/g

* Checked MOHID-Cmd version

MOHID-Cmd]$ hg tip
changeset:   39:c73ba8e9771c
tag:         tip
user:        Doug Latornell <dlatornell@eoas.ubc.ca>
date:        Tue Mar 12 09:45:57 2019 -0700
summary:     Preserve Lagrangian*.hdf5 results file.

* Check that local repo is up to date and compiled the model just to make sure all is current

[rmueller@cedar5 MIDOSS-MOHID-config]$ cd $PROJECT/$USER/MIDOSS/MIDOSS-MOHID/Solutions/linux
[rmueller@cedar5 linux]$ hg tip
changeset:   4:98f7ebc52505
tag:         tip
user:        Doug Latornell <dlatornell@eoas.ubc.ca.ca>
date:        Mon Mar 11 14:11:11 2019 -0700
summary:     Change compilation to debug mode so that segfaults give tracebacks.

[rmueller@cedar5 linux]$ salloc --time=0:10:0 --cpus-per-task=1 --mem-per-cpu=1024m --account=def-allen
salloc: Pending job allocation 18868419
salloc: job 18868419 queued and waiting for resources
salloc: job 18868419 has been allocated resources
salloc: Granted job allocation 18868419
salloc: Waiting for resource configuration
salloc: Nodes cdr768 are ready for job
[rmueller@cdr768 linux]$ ./compile_mohid.sh -mb1 -mb2 -mw

==========================================================================
build started:    Thu Mar 28 16:38:23 PDT 2019
build completed:  Thu Mar 28 16:45:11 PDT 2019

--->                  Executables ready                               <---

total 0
lrwxrwxrwx 1 rmueller def-allen 36 Mar 28 16:45 MohidWater.exe -> ../src/MohidWater/bin/MohidWater.exe

==========================================================================

* mohid run SOGa_01dec17_MF0_1000m3_7days_const_w_unrotated_smalldt.yaml $PROJECT/$USER/MIDOSS/results/MF0/SOG12117a

* mohid run SOGa_01dec17_MF0_1000m3_7days_unrotated_smalldt.yaml $PROJECT/$USER/MIDOSS/results/MF0/SOG12117b

* checked Ashu's MIDOSS-MOHID-CODE version
hg tip
not trusting file /project/6001313/abhudia/MIDOSS/MIDOSS-MOHID-CODE/.hg/hgrc from untrusted user abhudia, group def-allen
not trusting file /project/6001313/abhudia/MIDOSS/MIDOSS-MOHID-CODE/.hg/hgrc from untrusted user abhudia, group def-allen
changeset:   17:a1133c04f5c1
tag:         tip
user:        Your Name <your_email_address>
date:        Wed Mar 27 14:02:04 2019 -0700
summary:     modified shell script to account for interdependancy between Geometry and FillMatrix Modules

* reverted my "new" MIDOSS-MOHID-CODE to the one first installed and not edited for VVL
cd $PROJECT/rmueller/MIDOSS/MIDOSS-MOHID-CODE
hg revert --all --rev 991a511
reverting Software/MOHIDBase1/ModuleGlobalData.F90
reverting Software/MOHIDBase2/ModuleField4D.F90
reverting Software/MOHIDBase2/ModuleGeometry.F90
reverting Software/MOHIDBase2/ModuleInterpolation.F90
reverting Software/MOHIDWater/ModuleModel.F90
reverting Solutions/VisualStudio2010_IntelFortran12/MOHIDNumerics/MOHIDNumerics.suo
[rmueller@cedar5 MIDOSS-MOHID-CODE]$ hg tip
changeset:   9:5b34da4eac75
tag:         tip
user:        Shihan
date:        Thu Mar 14 19:54:55 2019 -0300
summary:     same as add vvl to MOHID. unfinished

hg update -r 991a511
6 files updated, 0 files merged, 0 files removed, 0 files unresolved
[rmueller@cedar5 MIDOSS-MOHID-CODE]$ hg tip
changeset:   9:5b34da4eac75
tag:         tip
user:        Shihan
date:        Thu Mar 14 19:54:55 2019 -0300
summary:     same as add vvl to MOHID. unfinished


I'm obviously don't know how to check-out 991a511 as "hg tip" shows that I didn't do it correctly....
3/22/19
Spent time on grid indexing and creating documentation for team on Google Drive:
MIDOSS_2/Notes_and_Docs/Mohid_NEMO_grid_setup/

Created MOHID_nc2dat_bathymetry.m, an updated version of Shihan's .m script 
that creates bathymetry values from AfterNEMOBathy201702.nc

Created: AfterNEMOBathy201702_rdm.dat

3/21/19
Run MOHID for 2-days with higher frequency output
$PROJECT/rmueller/MIDOSS/results/MF0/SOG12117

a) Learn how to adjust output time step in setting files:
$PROJECT/rmueller/MIDOSS/MIDOSS-MOHID-config/SOG12117
In Lagrangian.dat, changed 
OUTPUT_TIME   : 0 3600
to 
OUTPUT_TIME   : 0 1200
to match
DT_PARTIC     : 1200

WINDDRIFTANGLE  : 0.

Sent email to Shihan to confirm time stepping


VVL
- In smelt (/home/rmueller/Data/SalishSeaCast/grid) 
> hg pull --rebase 
to get Susan's update of bathymetry after NEMO has processed it: AfterNEMOBathy201702.nc

Susan saved "x" "y" to the .nc in place of latitude longitude, which MOHID needs.  To fix, I did the following
> cp bathymetry_201702.nc AfterNEMOBathy201702_rdm.nc
 
- Created /home/rmueller/Projects/MIDOSS/analysis-rachael/toolbox/matlab/Fix_AfterNEMOBathy201702.m to read in bathymetry from AfterNEMOBathy201702.nc and save it to AfterNEMOBathy201702_rdm.nc


 
3/20/19
transit-family emergency day (Ehren in hospital)

3/18-19/19
State Of Pacific Ocean Meeting

3/14/19
Printing to file the SZZ values calculated in MOHIDBase2/ModuleGeometry.F90,
line ~3916
[j,i] = [510, 200]

compiled and submitted job to run on cedar
Discussed FVCOM and NEMO in MOHID with Shihan
Next:
-Susan to create NEMO bathymetry
-Ashu and I to run model with new bathymetry and SZZ output to compare with e3t
-Particles (nparticles on surface vs. depth)
-

3/13/19
Troubleshoot error in run on Cedar: 
$PROJECT/rmueller/MIDOSS/MIDOSS-MOHID-config/SOG12117
when converting from HDF5 to netcdf, error:
TypeError: Timestamp subtraction must have the same timezones or no timezones

FIX: 
MOHID-Cmd> hg pull --rebase
MOHID-Cmd> pip3 install --user -e .
moad-tools> pip3 install --user -e

Resubmitted SOG121117 test case using updated model, from 
/home/rmueller/project/rmueller/MIDOSS/MIDOSS-MOHID-config/SOG12117
>mohid run SOGa_01dec17_MF0_1000m3_7days_hi_test.yaml $PROJECT/rmueller/MIDOSS/results/MF0_SOG12117/

NOTE: $PROJECT/rmueller/MIDOSS/results = /project/6001313/rmueller/MIDOSS/results

Made list of Code development:
1) [need] VVL
	Shihan, Rachael with Susan
2) [nice] Upgrading MOHID -> read in (and output?) staggered velocities.
3) [eventually] Can we use FVCOM & NEMO?  Shihan knows how to do this : please teach Ashu and Rachael Jan 16, 2019 or later
4) [coming] Xiaomei’s plans for dilbit
	Xiaomei with Rachael: what will you need? 
5) [eventually]Vertical diffusivities in MOHID: for Lagrangian
- Shihan/Rachael: are the diffusivities used as discussed in the docs? What is standard dev?
Ben, Rachael, Susan, Elise: get the needed variables out of NEMO
6) [nice] wind drift angle and wind drag coefficient
7) [eventually] Stokes drift from WW3 already in the files 
8) [all heads] dispersion by particle, what’s really going on, also look at vertical diffusion
9) [need] Hindcast of WW3 Susan
10) [eventually] Hindcast of FVCOM
11) [coming] Sedimentation
12) [need] Code evaluation  MODID (dispersion against OSCAR) ideal case
13) [need] Run and test the model: disappearing oil
14) [need] Real bathymetry file (as in the bathymetry that corresponds to e3t)



Shihan: FVCOM & NEMO, VVL, Vertical diffusivities in MOHID for Lagrangian, dispersion by particles (8), stokes drift from WW3, read in staggered velocities

Ashu: FVCOM & NEMO, Real bathymetry file, disappearing oil (run and test model)

Xiaomei: Plans for dilbit, sedimentation

Rachael: FVCOM & NEMO, Xiaomei's plans for dilbit, VVL, dispersion by particles, Vertical diffusivities (how are they in MOHID?), Run and test model (disppearing oil). 
 

3/12/19
How does MOHID treat oil particles? Is part of a particle dispersed or is a fraction of the oil dispersed as a number of particles into the water col.? Look in "ModuleLagrangianOil.F90, subroutine OilInternalProcesses

Next: 
- diff Shihan's .dat files with Ashu's to make sure they are the same
- plot up number of particles in the surface, number of particles at depth, and total number of particles over time
- VVL: Do we need SZZ? Or DWZ, DUZ, etc. :
 
3/11/19
Ashu: Make 3 panel movie of surface concentration, integrated concentration over all but surface layer, and integrated concentrations by depth. Make 3-panel movie of oil thickness, surface concentration and zoomed in window of both, all with surface current vectors and 1 wind vector in upper right hand corner

Shihan's talk take-aways from Susan:
- Investigate wind drift and drag
- Random walk for dispersion
- Update code to get stoke's drift from WW3

Follow-up with Shihan
- How to choose number of particles? 

Wind drift publications:
https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3907538/


2/28/19

Updating MIDOSS on Cedar:
> cd /home/rmueller/project/rmueller/MIDOSS/MOHID-Cmd
> hg update
> cd..
> pip3 install --user --editable MOHID-Cmd

Looking in links: /cvmfs/soft.computecanada.ca/custom/python/wheelhouse/avx2, /cvmfs/soft.computecanada.ca/custom/python/wheelhouse/generic
Obtaining file:///project/6001313/rmueller/MIDOSS/MOHID-Cmd
Requirement already satisfied: arrow in /home/rmueller/.local/lib/python3.7/site-packages (from MOHID-Cmd==19.1.dev0) (0.13.0)
Requirement already satisfied: attrs in /home/rmueller/.local/lib/python3.7/site-packages (from MOHID-Cmd==19.1.dev0) (18.2.0)
Requirement already satisfied: cliff!=2.9.0 in /home/rmueller/.local/lib/python3.7/site-packages (from MOHID-Cmd==19.1.dev0) (2.14.0)
Requirement already satisfied: python-hglib in /home/rmueller/.local/lib/python3.7/site-packages (from MOHID-Cmd==19.1.dev0) (2.6.1)
Requirement already satisfied: PyYAML in /home/rmueller/.local/lib/python3.7/site-packages (from MOHID-Cmd==19.1.dev0) (3.13)
Requirement already satisfied: python-dateutil in /home/rmueller/.local/lib/python3.7/site-packages (from arrow->MOHID-Cmd==19.1.dev0) (2.7.5)
Requirement already satisfied: pbr!=2.1.0,>=2.0.0 in /home/rmueller/.local/lib/python3.7/site-packages (from cliff!=2.9.0->MOHID-Cmd==19.1.dev0) (5.1.1)
Requirement already satisfied: stevedore>=1.20.0 in /home/rmueller/.local/lib/python3.7/site-packages (from cliff!=2.9.0->MOHID-Cmd==19.1.dev0) (1.30.0)
Requirement already satisfied: six>=1.10.0 in /home/rmueller/.local/lib/python3.7/site-packages (from cliff!=2.9.0->MOHID-Cmd==19.1.dev0) (1.12.0)
Requirement already satisfied: pyparsing>=2.1.0 in /home/rmueller/.local/lib/python3.7/site-packages (from cliff!=2.9.0->MOHID-Cmd==19.1.dev0) (2.3.1)
Requirement already satisfied: cmd2!=0.8.3; python_version >= "3.0" in /home/rmueller/.local/lib/python3.7/site-packages (from cliff!=2.9.0->MOHID-Cmd==19.1.dev0) (0.9.7)
Requirement already satisfied: PrettyTable<0.8,>=0.7.2 in /home/rmueller/.local/lib/python3.7/site-packages (from cliff!=2.9.0->MOHID-Cmd==19.1.dev0) (0.7.2)
Requirement already satisfied: pyperclip>=1.5.27 in /home/rmueller/.local/lib/python3.7/site-packages (from cmd2!=0.8.3; python_version >= "3.0"->cliff!=2.9.0->MOHID-Cmd==19.1.dev0) (1.7.0)
Requirement already satisfied: colorama in /home/rmueller/.local/lib/python3.7/site-packages (from cmd2!=0.8.3; python_version >= "3.0"->cliff!=2.9.0->MOHID-Cmd==19.1.dev0) (0.4.1)
Requirement already satisfied: wcwidth>=0.1.7 in /home/rmueller/.local/lib/python3.7/site-packages (from cmd2!=0.8.3; python_version >= "3.0"->cliff!=2.9.0->MOHID-Cmd==19.1.dev0) (0.1.7)
Installing collected packages: MOHID-Cmd
  Found existing installation: MOHID-Cmd 19.1.dev0
    Uninstalling MOHID-Cmd-19.1.dev0:
      Successfully uninstalled MOHID-Cmd-19.1.dev0
  Running setup.py develop for MOHID-Cmd
Successfully installed MOHID-Cmd

>salloc --time=0:10:0 --cpus-per-task=1 --mem-per-cpu=1024m --account=def-allen

THIS TOOK FOREVER!!!! (10-20 minutes)
Finally...
> cd $PROJECT/$USER/MIDOSS/MIDOSS-MOHID/Solutions/linux
> ./compile_mohid.sh -mb1 -mb2 -mw


#### Mohid Base 1 ####
 compile mohidbase1 OK                                                                             


#### Mohid Base 2 ####
 compile mohidbase2 OK                                                                       


#### Mohid Water ####
 compile MohidWater OK                                                                           

==========================================================================
build started:    Thu Feb 28 11:11:12 PST 2019
build completed:  Thu Feb 28 11:17:26 PST 2019

--->                  Executables ready                               <---

total 0
lrwxrwxrwx 1 rmueller def-allen 36 Feb 28 11:17 MohidWater.exe -> ../src/MohidWater/bin/MohidWater.exe

==========================================================================



!*******************
Added files to analysis-rachael rep from Macbook Pro using
> hg add
> hg commit
> hg pull --rebase
> hg push

I then went to my Cedar account to update using:
> hg pull
[rmueller@cedar5 analysis-rachael]$ hg pull 
pulling from ssh://hg@bitbucket.org/midoss/analysis-rachael
searching for changes
adding changesets
adding manifests
adding file changes
added 2 changesets with 2 changes to 2 files
(run 'hg update' to get a working copy)
!*********************************

> hg update
> mohid run MarathassaConstTS.yaml $PROJECT/$USER/MIDOSS/results/MarathassaConstTS

nemo_cmd.prepare ERROR: /scratch/rmueller/MIDOSS/runs path from "paths: runs directory" key not found - please check your run description YAML file

created /scratch/rmueller/MIDOSS/runs

> mohid run MarathassaConstTS.yaml $PROJECT/$USER/MIDOSS/results/MarathassaConstTS

-bash: cd: /home/rmueller/project/rmueller/MIDOSS/results/MarathassaConstTS: No such file or directory

created home/rmueller/project/rmueller/MIDOSS/results/MarathassaConstTS

> mohid run MarathassaConstTS.yaml $PROJECT/$USER/MIDOSS/results/MarathassaConstTS
mohid_cmd.run INFO: Created temporary run directory /scratch/rmueller/MIDOSS/runs/MarathassaConstTS_2019-02-28T151911.989819-0800
mohid_cmd.run INFO: Wrote job run script to /scratch/rmueller/MIDOSS/runs/MarathassaConstTS_2019-02-28T151911.989819-0800/MOHID.sh
mohid_cmd.run INFO: Submitted batch job 17537913

discovered that "hg update" didn't pull the most recent version of MOHID-Cmd
hg pull --rebase
pulling from ssh://hg@bitbucket.org/midoss/mohid-cmd
searching for changes
adding changesets
adding manifests
adding file changes
added 8 changesets with 21 changes to 11 files
nothing to rebase - updating instead
11 files updated, 0 files merged, 0 files removed, 0 files unresolved
[rmueller@cedar5 MOHID-Cmd]$ hg tip
changeset:   37:79d074ecee6f
tag:         tip
user:        Doug Latornell <dlatornell@eoas.ubc.ca>
date:        Thu Jan 31 17:25:05 2019 -0800
summary:     Improve semantic markup in docs.


!****************
Working with Ashu:  He is re-running MOHID after having re-installed MOHID-Cmd to see if the HDF5toNetCDF conversion now works

We are writing Shihan to ask why his output looks different.  After doing "diffs" on files, we confirmed that the only changes are file names.  All values in Lagrangian.dat are the same.  It doesn't make sense that Shihan's oil releases in a line and Ashu's at a point.


!*****  Accessing Ashu's files on Cedar ****

cd /scratch/abhudia/MIDOSS/runs/ashu_testing/

cd ~/project/abhudia

>cd  /scratch/abhudia/MIDOSS/runs/ashu_testing/nextcloud_replicate_2019-02-26T153311.865648-0800/res/
> salloc --time=00:10:0 --cpus-per-task=1 --mem-per-cpu=20000m --account=def-allen
> hdf5-to-netcdf4 Lagrangian.hdf5 $PROJECT/$USER/MIDOSS/tmp/Lagrangian.nc


2/27/19

Work with Ashu on running MOHID on Cedar.  He rebuilt yesterday and the code now runs. Current challenge:  HDF5 to NETCDF conversion isn't working and errors differ on Cedar, Hake, and Salish.  Short-term work around: Access HDF5 output directly.  Look at oil_concentration_3D and beaching time. Work with Shihan's HDF5 reading scripts. 

Look up HDF5viewer and Panoply for looking at HDF5 files.

