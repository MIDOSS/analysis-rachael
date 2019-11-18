This analysis folder organizes scripts, data and products used to  of model output towards understanding Salish Sea circulation, influences and impacts.

The links below are to static renderings of the notebooks via
[nbviewer.jupyter.org](https://nbviewer.jupyter.org/).
Descriptions under the links below are from the first cell of the notebooks
(if that cell contains Markdown or raw text).

* ##[plot_vvl_test.ipynb](https://nbviewer.jupyter.org/urls/bitbucket.org/midoss/analysis-rachael/raw/default/notebooks/vvl/plot_vvl_test.ipynb)  
    
    **Plot results from VVL test with SSH = 0**  
    These results were generated with teh following setup:  
    - Salmon bank spill at -122.86 48.38  
    - currents west above 2m and north below 2m  
    - constant wave period (5), wave height (0.8), wcc (0.001), StokesU = StokesV = 0  
    - currents $PROJECT/rmueller/MIDOSS/forcing/vvl_testing/currents_west_above2_north_below2.hdf5  
    - /scratch/dlatorne/MIDOSS/forcing/vvl_test/e3t.hdf5  
      
    Both e3t.hdf5 and t.hdf5 were re-created for this run to try and troubleshoot the "land point" error.   

* ##[Final_scale_e3t_forcing.ipynb](https://nbviewer.jupyter.org/urls/bitbucket.org/midoss/analysis-rachael/raw/default/notebooks/vvl/Final_scale_e3t_forcing.ipynb)  
    
    **Read in e3t and create a +/-2 m SSH versions **  

* ##[scale_e3t_forcing.ipynb](https://nbviewer.jupyter.org/urls/bitbucket.org/midoss/analysis-rachael/raw/default/notebooks/vvl/scale_e3t_forcing.ipynb)  
    
    **Read in e3t and create a +/-2 m SSH versions **  


##License

These notebooks and files are copyright 2013-2019
by the Salish Sea MEOPAR Project Contributors
and The University of British Columbia.

They are licensed under the Apache License, Version 2.0.
https://www.apache.org/licenses/LICENSE-2.0
Please see the LICENSE file for details of the license.
