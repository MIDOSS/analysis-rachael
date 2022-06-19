#!/bin/bash
#SBATCH --account=def-allen
#SBATCH --job-name="oil_spills(month-a)"
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
srun glost_launch /scratch/rmueller/MIDOSS/Results/ByMonth/14March2022/aggregate_200_oil_spills_14March2022.list
echo "Finished run at: `date`"

