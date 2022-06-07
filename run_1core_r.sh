#!/bin/bash
#
#SBATCH --account=def-marchanp
#SBATCH --time=11:59:00
#SBATCH --mem-per-cpu=8G

module load gdal/3.0.4
module load r/4.0.2

Rscript --vanilla $1