#!/usr/bin/python

import sys
import shutil
import os
from subprocess import call
import re
import math

"""
Run phyloseq wrapped with DESeq2 to compute negative binormial for feature selection
(1)Generate parameter file for R script and Split taxa file for each pair of cohort groups, and convert them into BIOM file
(2)Run R script to compute negative binormial for feature selection
(3)Calculate average relative abundance for each cohort group,and combine with negative bionormial results
"""
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
if len(sys.argv)!=4:
    raise Exception ("Usage of Phyloseq_DESeq2.py <taxonomic method> <input folder> <output folder>")
taxa_method=sys.argv[1]
input_dir=sys.argv[2]
output_dir=sys.argv[3]

design_dir=output_dir+"DesignFiles/"
taxa_dir=output_dir+"Taxa_summary_"+taxa_method+'/'
ab_dir=taxa_dir+'taxa_summary_Filter_ab/'
rel_dir=taxa_dir+'taxa_summary_Filter_rel/'
para_infile=input_dir+"CohortGroups_ParametersList.txt"

work_dir=output_dir+"Phyloseq_DESeq2/"
input_dir=work_dir+'phyloseq_DESeq_in/'
nb_dir=work_dir+'phyloseq_DESeq2_out/'

if os.path.exists(work_dir)==False:
    os.mkdir(work_dir)
if os.path.exists(input_dir):
    shutil.rmtree(input_dir)
os.mkdir(input_dir)
if os.path.exists(nb_dir):
    shutil.rmtree(nb_dir)
os.mkdir(nb_dir)


print "Prepare parameter files and files for running phyloseq_DESeq2..."
#Generate parameter file for R script
#Split taxa file for each pair of cohort groups, and convert them into BIOM file
para_outfile=work_dir+'Phyloseq_DESeq2_input_list.txt'
python_script='./phyloseq_DESeq2_makingFiles.py'
call([python_script,para_infile,para_outfile,design_dir,ab_dir,input_dir,nb_dir])


print "Run phyloseq_DESeq2..."
#Run R script to compute negative binormial for feature selection
r_script='./R/phyloseq_DESeq2.R'
r_script_new='phyloseq_DESeq2.R'
modify_r_script(r_script,r_script_new,output_dir)
call(["R","CMD","BATCH",r_script_new])


print "Calculate average releative abundance for each cohort group..."
#Calculate average relative abundance for each cohort group,and combine with negative bionormial results
design=design_dir+'CohortGroups.design'
python_script='./phyloseq_DESeq2_calculateAvgSD_rel.py'
call([python_script,para_outfile,design,rel_dir])

quit()
