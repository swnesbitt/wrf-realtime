#!/bin/bash

#SBATCH --job-name=plot
#SBATCH --array=0-36
#SBATCH --ntasks=1
#SBATCH --time=0:15:00
#SBATCH --mem-per-cpu=2000

sleep $[ ( $RANDOM % 10 )  + 1 ]s

export run=${1}

source activate pyn_test
cd /data/keeling/a/snesbitt/wrf_realtime/py-postplot

export fhr=`printf "%02d\n" ${SLURM_ARRAY_TASK_ID}`
export file=/data/meso/a/snesbitt/wrf38/fcsts/${run}/${run}_WRFPRS_d01.${fhr}.grb2
python sfc_plot.py $file 
python upa_plot.py $file

export DIRECTORY=/data/keeling/a/snesbitt/monsoon/public_html/RELAMPAGO/wrf_realtime/$run
if [ ! -d "$DIRECTORY" ]; then
  mkdir -p $DIRECTORY
  chmod o+rx $DIRECTORY
fi
mv ${run}_WRFPRS_d01.${fhr}.grb2*.png $DIRECTORY 
chmod o+r ${DIRECTORY}/${fhr}*.png
