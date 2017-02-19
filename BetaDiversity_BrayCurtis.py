#!/usr/bin/python

import sys
import shutil
import os
from subprocess import call
import re

"""
Run Bray-Curtis 
(1)Run Bray-Curtis in mothur
(2)Plot PCoA figures of Bray-Curtis of 2D
"""
def get_parameter_list(file):
    in_fh=open(file,'r')
    count=0
    for line in in_fh:
        count=count+1
        if count==1:
            continue

        line=line.rstrip('\n')
        list=line.split('\t',)
        list_para.append(list)

    return

def modify_mothur_script(mothur_script,mothur_script_new,output_dir):
    outfh=open(mothur_script_new,'w')
    infh=open(mothur_script,'r')
    for line in infh:
        if re.search("../output/",line):
            line=line.replace("../output/",output_dir)
        outfh.write(line)
    outfh.close()
    infh.close()
    return



"""
#Main function
"""
if len( sys.argv ) != 5:
        raise Exception( "Usage: BetaDiversity_BrayCurtis.py <Mothur path> <running reference folder> <input folder> <output folder>")

mothur=sys.argv[1]
ref_dir=sys.argv[2]
input_dir=sys.argv[3]
output_dir=sys.argv[4]

shared_dir=output_dir+"Filter_0.03Cluster_OTU/"
design_dir=output_dir+"DesignFiles/"
work_dir=output_dir+"mothur/BrayCurtis/"
if os.path.exists(work_dir)==False:
	os.mkdir(work_dir)


#(1)Run BrayCurtis in mothur
print "Run BrayCurtis using mothur..."
shared_file=shared_dir+"0.03Cluster_OTU_Filter.shared"
shutil.copy(shared_file,work_dir)
mothur_script=''
for file in os.listdir('./mothur/'):    
    if re.search('bray_curtis.mothur',file):
        mothur_script='./mothur/'+file
        mothur_script_new=work_dir+file
        modify_mothur_script(mothur_script,mothur_script_new,output_dir)
call([mothur,mothur_script_new])
for file in os.listdir('./'):
    if file.endswith(".logfile"):
        shutil.move(file,work_dir)


#(2)Plot 2D PCoA of Bray-Curtis
print "Plot BrayCurtis PCoA with 2D..."
#Build directory
plot_dir=work_dir+'Plot_PCoA/'
if os.path.exists(plot_dir):
    shutil.rmtree(plot_dir)
os.mkdir(plot_dir)

#Parameters for group pair
listfile=work_dir+"BrayCurtis_ParametersList.txt"
shutil.copy(input_dir+'CohortGroups_ParametersList.txt',listfile)
#group1[i][0],group2[i][1],designfile[i][2]
list_para=[]
get_parameter_list(listfile)

#Plot figure for each matrix
script='./plot_PCoA_2D.pl'
for file in os.listdir(work_dir):
    if file.endswith(".axes"):
        infile=work_dir+file
        level='1-2'
        for i,v in enumerate(list_para):
            designfile=design_dir+list_para[i][2]
            groups=list_para[i][0]+'-'+list_para[i][1]
            type='BrayCurtis'
            call([script,infile,level,designfile,groups,plot_dir,type])
        

quit()
