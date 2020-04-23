def plot_massbalanc(input_dir):

import xarray as xr
import numpy as np
import matplotlib.pyplot as plt

# parse directory name to create output file names
# Assumes the last 3 directory names describe oil_type, location and date
dir_str = input_dir.split('/')
ndirs = len(dir_str)
out_tag = test_split[ndirs-4] + '_' + test_split[ndirs-3] + '_' + test_split[ndirs-2]

# define input file name
input_file = 'input_dir' + 'resOilOutput.sro'

# load data
with open(input_file, 'r') as the_file:
    all_data = [line.strip() for line in the_file.readlines()]
    header = all_data[4]

# Order header into list array by splitting up string
header_arr = []
header_arr = header.split(' ')

# Remove emtpy entries from list
header_arr = np.asarray([x for x in header_arr if x != ''])

# Load data
data2D = np.genfromtxt(input_file, skip_header=6, skip_footer=4)
nrows,ncols = data2D.shape

# define structure of structured array
dtype = [('Header',(np.str_,22)),('Values', np.float64)]

# create index list for for-loop over columns
header_range = range(header_arr.size)
data_range = range(nrows)

# Assign 2D data and header strings to structured array
massbalance = np.array([[(header_arr[hdr_index], data2D[data_index, hdr_index]) for hdr_index in header_range] for data_index in data_range], dtype=dtype)
[data_len, ncols] = massbalance.shape
