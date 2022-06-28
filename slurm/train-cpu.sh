#!/bin/bash

#SBATCH --job-name dhc-test
#SBATCH --ntasks=1
#SBATCH --time=6:00:00

# **** available partition ****
# 1. cpu-share (max: 6)
# 2. gpu-share (max: 2)
# 3. himem-share (max: 2)
# *****************

# selecting partition
#SBATCH -p cpu-share

# **** example ****
# To use 2 cpu cores and 4 gpu devices in a node
##SBATCH -N 1 -n 2 --gres=gpu:4
# use 4 cpu cores
##SBATCH -N 1 -n 4
# *****************

# select cores, 1 cpu
#SBATCH -N 1 -n 1
#SBATCH --mem=8G # memory per node???

# output file location
## SBATCH --output=/home/hcchengaa/ml-projects/big2-rl/slurm_report/%j.out
  # Lmod has detected error, unknown module python
# source activate b
# module load python

srun which python # confirm python version. This should be executed if we used 'conda activate big2rl' before

# test with cpu
echo -e "\n\n\n Testing"
cd .. # go back to the main folder

srun python test.py

echo -e "Testing done"