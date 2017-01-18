#!/bin/bash

#SBATCH --job-name=wrf_3km
#SBATCH --nodes=4-4
#SBATCH --ntasks-per-node=20
#SBATCH --partition g
#SBATCH --time=6:00:00
#SBATCH --mem-per-cpu=5000
#SBATCH --mail-type=BEGIN
#SBATCH --mail-type=FAIL
#SBATCH --mail-type=END
#SBATCH --mail-user=snesbitt@@illinois.edu

echo $1 $2 $3

now=$(date +"%T")
echo "Start time : $now"

module load intel/intel-14.0.3
module load intel/netcdf4-4.2-intel-14.0.3
module load intel/openmpi-1.6.4a-intel-14.0.3

python wrf_realtime_batch.py ${1} ${2} ${3}

cd /data/meso/a/snesbitt/wrf38/WRFV3/test/em_sa

rm wrfout*

#KMP_STACKSIZE=100000000 #might still be subject to tuning
ulimit -s unlimited
export OMP_NUM_THREADS=1

#time mpirun -n 20 ./real.exe
time mpirun -n 80 ./wrf.exe

cd wrfprd
ln -sf ../wrfout* .
cd ..

cd postprd
./run_unipost

mkdir -p /data/meso/a/snesbitt/wrf38/fcsts/${1}

for i in (WRFPRS*); do
 mv $i /data/meso/a/snesbitt/wrf38/fcsts/${1}/${1}_$i.grb2
done

echo ""|mailx -s "wrf 3 km initialized at ${1} completed" snesbitt@@illinois.edu
