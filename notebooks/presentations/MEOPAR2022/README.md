# Mueller et al. graphics code for MEOPAR All Science Meeting, 2022 

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

Use `analysis-rachael/env/monte_carlo.yaml` to create a [Conda](https://docs.conda.io/en/latest/miniconda.html) environment for these notebook:
```
 conda env create -f [analysis-rachael/env/monte_carlo.yaml]
```
or, to activate this environment, use
```
 conda activate monte-carlo
```
To deactivate an active environment, use
```
 conda deactivate
```

Next, add the `scripts` directory to your `PYTHONPATH` environment variable to access the `tools` module:

```
$ export PYTHONPATH=$PYTHONPATH:/path/to/analysis-rachael/scripts
```
Any of the notebooks can by run by starting a Jupyter session and navigating to the `notebooks` directory:

```
$ jupyter lab
```

## Licenses

These notebooks are copyright 2022 by Rachael Mueller and The University of British Columbia.

They are licensed under the Apache License, Version 2.0.
http://www.apache.org/licenses/LICENSE-2.0
Please see the LICENSE file for details of the license.
