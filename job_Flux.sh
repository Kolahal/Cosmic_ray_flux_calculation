#!/bin/bash
#SBATCH --account="miniclean"
#SBATCH --time=4-00:00:00
#SBATCH -o slurm-%A_%a.out
#SBATCH -e slurm-%A_%a.err
#SBATCH -N 1
#SBATCH -p gpu

unset DISPLAY

module purge

module load python/3.7.2
#export PATH=/share/apps/python/3.7.2/bin/python:$PATH
#export PYTHONPATH=/share/apps/python/3.7.2/lib/python3.7

#module load python/3.7.2
#export PATH=/share/apps/python/3.7.2/bin/python:$PATH
#export PYTHONPATH=/share/apps/python/3.7.2/lib/python3.7

python runFlux.py 0
