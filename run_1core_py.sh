#!/bin/bash
#
#SBATCH --account=def-marchanp
#SBATCH --time=11:59:00
#SBATCH --mem-per-cpu=8G

module load python/3.9
module load scipy-stack

source ~/ENV/bin/activate 
python -u $1