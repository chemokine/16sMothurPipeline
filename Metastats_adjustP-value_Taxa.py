#!/usr/bin/python

import sys
import shutil
import os
from subprocess import call
import re
import time

"""
Run Metastats on taxa in mothur
(1)Reverse the taxonomic table with counts
(2)Generate mothur batch file and run mothur
(3)Select genus information, and correct multiple hyposothis testing using BH(FDR)
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

def modify_r_script(r_script,r_script_new,output_dir):
    outfh=open(r_script_new,'w')
    infh=open(r_script,'r')
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
        raise Exception( "Usage: Metastats_adjustP-value_Taxa.py <Mothur path> <taxonomic method> <input folder> <output folder>")

mothur=sys.argv[1]
taxa_method=sys.argv[2]
input_dir=sys.argv[3]
output_dir=sys.argv[4]

design_dir=output_dir+"DesignFiles/"
taxa_dir=output_dir+"Taxa_summary_"+taxa_method+"/"
work_dir=output_dir+"mothur/Metastats_Taxa/"
if os.path.exists(work_dir)==False:
	os.mkdir(work_dir)

#(1)Reverse taxonomic table
print "- Reverse taxonomic table for running metastats..."
python_script="./metastats_reverse_taxaSummaryTable.py"
in_dir=taxa_dir+'taxa_summary_Filter_rel/'
out_dir=work_dir+'Reverse_taxa_summaryTable_rel/'
if os.path.exists(out_dir):
	shutil.rmtree(out_dir)
os.mkdir(out_dir)
call([python_script,in_dir,out_dir])

in_dir=taxa_dir+'taxa_summary_Filter_ab/'
out_dir=work_dir+'Reverse_taxa_summaryTable_ab/'
if os.path.exists(out_dir):
	shutil.rmtree(out_dir)
os.mkdir(out_dir)
call([python_script,in_dir,out_dir])


#(2)Generate mothur batch file, and run mothur
print "- Run Metastats on taxa using mothur..."
metastats_out_dir=work_dir+'metastats_out/'
if os.path.exists(metastats_out_dir):
	shutil.rmtree(metastats_out_dir)
os.mkdir(metastats_out_dir)
mothur_script=work_dir+'metastats.mothur'
out_fh=open(mothur_script,'w')
out_fh.write("set.dir(output="+metastats_out_dir+")\n")

#Parameters for group pair
listfile=work_dir+"Metastats_ParametersList.txt"
shutil.copy(input_dir+'CohortGroups_ParametersList.txt',listfile)
#group1[i][0],group2[i][1],designfile[i][2]
list_para=[]
get_parameter_list(listfile)
for i,v in enumerate(list_para):
    designfile=design_dir+list_para[i][2]
    sets=list_para[i][0]+'-'+list_para[i][1]
    for file in os.listdir(out_dir):
        if file.endswith(".txt"):
            shared=out_dir+file
            out_fh.write("metastats(shared="+shared+',design='+designfile+',sets='+sets+")\n")
out_fh.close()
call([mothur,mothur_script])    
        
#(3-1)Select information on genus level, and run BH to calculate FDR
print "- Calculate FDR to correct p-values..."
select_file=metastats_out_dir+'metastats_Genus_Filter.txt'
python_script="./metastats_filter_records_Genus.py"
call([python_script,metastats_out_dir,select_file])

#Run R
r_script='./R/calculate_FDR_BH_Genus.R'
r_script_new='calculate_FDR_BH_Genus.R'
modify_r_script(r_script,r_script_new,output_dir)
call(["R","CMD","BATCH",r_script_new])

print "Statistical test using metastats is done!"
quit()
