#!/bin/bash
#SBATCH --account=rrg-allen
#SBATCH --job-name="oil_spills"
#SBATCH --time=2:30:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=27
#SBATCH --mem-per-cpu=12800M
#SBATCH --mail-user=rmueller@eoas.ubc.ca
#SBATCH --mail-type=ALL

module load glost/0.3.1
module load python/3.8.2
source ~/venvs/pymem/bin/activate

echo "Starting run at: `date`"
srun glost_launch /scratch/rmueller/MIDOSS/Results/ByOilType/13December2021/aggregate_200_oil_spills_13December2021_a.list
echo "Finished run at: `date`"

