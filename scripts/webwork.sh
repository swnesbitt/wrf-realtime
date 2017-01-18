#!/bin/bash

#SBATCH --job-name=web
#SBATCH --ntasks=1
#SBATCH --time=0:15:00
#SBATCH --mem-per-cpu=2000

export run=${1}

source activate pyn_test

python postproc.py $run

chmod o+r ~/monsoon/public_html/RELAMPAGO/wrf_realtime/${run}/*
