#!/bin/bash

#SBATCH --job-name=wrf_3km
#SBATCH -c 20
#SBATCH -n 4
#SBATCH --partition g
#SBATCH --time=6:00:00
#SBATCH --mem-per-cpu=5000
#SBATCH --mail-type=BEGIN
#SBATCH --mail-type=FAIL
#SBATCH --mail-type=END
#SBATCH --mail-user=snesbitt@illinois.edu

cd /data/keeling/a/snesbitt/wrf_realtime/scripts

inc=1
len=36
#run=`date -u +%Y%m%d`${1}
run=${1}

now=$(date +"%T")
echo "Start time : $now"

module load intel/intel-14.0.3
module load intel/netcdf4-4.2-intel-14.0.3
module load intel/openmpi-1.6.4a-intel-14.0.3

python wrf_realtime_batch.py ${run} ${len} ${inc}

cd /data/meso/a/snesbitt/wrf38/WRFV3/test/em_sa

rm wrfout*

KMP_STACKSIZE=100000000 #might still be subject to tuning
OMP_STACKSIZE=100000000 #might still be subject to tuning
ulimit -s unlimited

export OMP_NUM_THREADS=4
time mpirun -n 1 ./real.exe
export OMP_NUM_THREADS=10
time mpirun -n 8 ./wrf.exe

cd wrfprd
ln -sf ../wrfout* .
cd ..

cd postprd
./run_unipost

mkdir -p /data/meso/a/snesbitt/wrf38/fcsts/${run}

for i in WRFPRS*; do
 mv $i /data/meso/a/snesbitt/wrf38/fcsts/${run}/${run}_$i.grb2
done

now=$(date +"%T")
echo "End time : $now"

echo ""|mailx -s "wrf 3 km initialized at ${1} completed" snesbitt@illinois.edu

