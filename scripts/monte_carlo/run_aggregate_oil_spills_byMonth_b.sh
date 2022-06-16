#!/bin/bash
#SBATCH --account=rrg-allen
#SBATCH --job-name="aggregate ByMonth_b"
#SBATCH --time=3:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=28
#SBATCH --mem-per-cpu=12800M
#SBATCH --mail-user=rmueller@eoas.ubc.ca
#SBATCH --mail-type=ALL

module load glost/0.3.1
module load python/3.8.2
source ~/venvs/pymem/bin/activate

echo "Starting run at: `date`"
srun glost_launch /home/rmueller/projects/def-allen/rmueller/MIDOSS/analysis-rachael/inputs/aggregation/ByMonth/SpillTime_00-30/aggregate_200_oil_spills_14December2021_b.list
echo "Finished run at: `date`"

