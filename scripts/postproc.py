import glob
import os
import datetime
import sys

run=sys.argv[1]

files=glob.glob('/data/keeling/a/snesbitt/monsoon/public_html/RELAMPAGO/wrf_realtime/'+run+'/*.00.*')

fields=[i.split('.grb2_')[1][:-6] for i in files]


def replace_str(fileToSearch,fileToWrite,textToSearch, textToReplace):
    # Read in the file
    filedata = None
    with open(fileToSearch, 'r') as file :
        filedata = file.read()

    # Replace the target string
    filedata = filedata.replace(textToSearch, textToReplace)

    # Write the file out again
    with open(fileToWrite, 'w') as file:
        file.write(filedata)


for anim in fields:
    thesefiles=sorted(glob.glob('/data/keeling/a/snesbitt/monsoon/public_html/RELAMPAGO/wrf_realtime/'+run+'/*'+anim+'*.png'))
    thesefiles=[i.split('/')[-1] for i in thesefiles]
    myString = ", ".join(thesefiles)

    replace_str('/data/keeling/a/snesbitt/wrf_realtime/scripts/config_template.txt',
               '/data/keeling/a/snesbitt/monsoon/public_html/RELAMPAGO/wrf_realtime/'+run+'/config_'+anim+'.txt',
               'REPLACEME',
                myString)

    replace_str('/data/keeling/a/snesbitt/wrf_realtime/scripts/html_template.html',
               '/data/keeling/a/snesbitt/monsoon/public_html/RELAMPAGO/wrf_realtime/'+run+'/anim_'+anim+'.html',
               'REPLACEME',
                anim)

    os.system('chmod o+r '+'/data/keeling/a/snesbitt/monsoon/public_html/RELAMPAGO/wrf_realtime/'+run+'/config_'+anim+'.txt')
    os.system('chmod o+r '+'/data/keeling/a/snesbitt/monsoon/public_html/RELAMPAGO/wrf_realtime/'+run+'/anim_'+anim+'.html')
    os.system('chmod o+r '+'/data/keeling/a/snesbitt/monsoon/public_html/RELAMPAGO/wrf_realtime/'+run+'/*'+anim+'*.png')

replace_str('/data/keeling/a/snesbitt/monsoon/public_html/RELAMPAGO/wrf_realtime/index.html.template',
               '/data/keeling/a/snesbitt/monsoon/public_html/RELAMPAGO/wrf_realtime/index.html',
               'CURRUN',
                run)

replace_str('/data/keeling/a/snesbitt/monsoon/public_html/RELAMPAGO/wrf_realtime/index.html',
               '/data/keeling/a/snesbitt/monsoon/public_html/RELAMPAGO/wrf_realtime/index.html',
               'INITIALIZED',
                run)

replace_str('/data/keeling/a/snesbitt/monsoon/public_html/RELAMPAGO/wrf_realtime/index.html',
               '/data/keeling/a/snesbitt/monsoon/public_html/RELAMPAGO/wrf_realtime/index.html',
               'COMPLETED',
               datetime.datetime.utcnow().isoformat())
