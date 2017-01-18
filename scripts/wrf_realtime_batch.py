import sys
import os
import subprocess
import numpy as np
import wget
from datetime import datetime, timedelta
import fileinput

def replace_str(fileToSearch,textToSearch, textToReplace):
    # Read in the file
    filedata = None
    with open(fileToSearch, 'r') as file :
        filedata = file.read()

    # Replace the target string
    filedata = filedata.replace(textToSearch, textToReplace)

    # Write the file out again
    with open(fileToSearch, 'w') as file:
        file.write(filedata)

initdate=sys.argv[1]

maxfcst=sys.argv[2]

freq=sys.argv[3]

hh=initdate[-2:]

print(hh)

currdir=os.getcwd()+'/'

starttime=datetime.strptime(initdate,'%Y%m%d%H')
endtime=starttime+timedelta(hours=int(maxfcst))

st_wps=starttime.strftime('%Y-%m-%d_%H:%M:%S')
et_wps=endtime.strftime('%Y-%m-%d_%H:%M:%S')

styr=starttime.strftime('%Y')
stmo=starttime.strftime('%m')
stdy=starttime.strftime('%d')
sthr=starttime.strftime('%H')

edyr=endtime.strftime('%Y')
edmo=endtime.strftime('%m')
eddy=endtime.strftime('%d')
edhr=endtime.strftime('%H')


print("preparting to run wrf from ",starttime,endtime)

urlbase='http://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/gfs.{}/'.format(initdate)

urls=[]

wps_base='/data/snesbitt/f/snesbitt/wrf/domains/sa_3km/'
wps_dir=wps_base+initdate
print(wps_dir)
subprocess.call(['mkdir','-p',wps_dir])

wrfrun_dir='/data/meso/a/snesbitt/wrf38/WRFV3/test/em_sa/'

os.chdir(wps_dir)

for i in np.arange(0,np.int(maxfcst)+1,np.int(freq)):
    urls.append('{}gfs.t{}z.pgrb2.0p25.f{:03d}'.format(urlbase,hh,i))
    print(urls[i])
    subprocess.call(['wget','-c',urls[i]])

wps_exe='/data/meso/a/snesbitt/wrf38/WPS/'

os.system('ln -sf '+wps_exe+'link_grib.csh .')
os.system('cp '+currdir+'namelist.wps.template ./namelist.wps')

replace_str('./namelist.wps','STARTDATE',st_wps)
replace_str('./namelist.wps','ENDDATE',et_wps)

os.system('ln -sf '+wps_exe+'ungrib/Variable_Tables/Vtable.GFS ./Vtable')
os.system('ln -sf '+wps_exe+'metgrid* .')
os.system('ln -sf '+wps_exe+'ungrib* .')

os.system('ln -sf '+wps_base+'geo_em.d01.nc .')

os.system('./link_grib.csh gfs.t*')
os.system('./ungrib.exe')
os.system('mpirun -np 20 ./metgrid.exe')

os.system('rm -rf '+wrfrun_dir+'met_em* '+wrfrun_dir+'+namelist.input')
os.system('ln -sf `pwd`/met_em* '+wrfrun_dir)

os.system('cp '+currdir+'namelist.input.template '+wrfrun_dir+'namelist.input')

replace_str(wrfrun_dir+'namelist.input','STYR',styr)
replace_str(wrfrun_dir+'namelist.input','STMO',stmo)
replace_str(wrfrun_dir+'namelist.input','STDY',stdy)
replace_str(wrfrun_dir+'namelist.input','STHR',sthr)

replace_str(wrfrun_dir+'namelist.input','EDYR',edyr)
replace_str(wrfrun_dir+'namelist.input','EDMO',edmo)
replace_str(wrfrun_dir+'namelist.input','EDDY',eddy)
replace_str(wrfrun_dir+'namelist.input','EDHR',edhr)

script='run_unipost'
os.system('rm '+wrfrun_dir+'/postprd/*')
os.system('cp '+currdir+'run_unipost.template '+wrfrun_dir+'/postprd/'+script)
replace_str(wrfrun_dir+'/postprd/'+script,'POSTSTARTDATE',initdate)
replace_str(wrfrun_dir+'/postprd/'+script,'POSTLAST',maxfcst)


print("ready to run wrf from ",starttime,endtime)
