#!/bin/bash
#SBATCH --account=rrg-allen
#SBATCH --job-name="oil_spills"
#SBATCH --time=3:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=3
#SBATCH --mem-per-cpu=51200M
#SBATCH --mail-user=rmueller@eoas.ubc.ca
#SBATCH --mail-type=ALL

module load glost/0.3.1
module load python/3.8.2
source ~/venvs/python/bin/activate

echo "Starting run at: `date`"
srun glost_launch aggregate_oil_spills.list
echo "Finished run at: `date`"
