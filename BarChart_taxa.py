#!/usr/bin/python

import os
import sys
import re
from subprocess import call
import shutil


"""
Main function
(1)Calculate average reletive abundance,SD for each treatment group for each taxa on each taxa level
(2)Draw them on the bar
"""
if len(sys.argv)!=3:
    raise Exception ("Usage of BarChart_taxa.py <taxonomic method> <output folder>")
taxa_method=sys.argv[1]
output_dir=sys.argv[2]

design_file=output_dir+'DesignFiles/CohortGroups.design'
rel_taxa_dir=output_dir+"Taxa_summary_"+taxa_method+"/taxa_summary_Filter_rel/"

work_dir=output_dir+"BarChart_taxa/"
plot_dir=work_dir+'Draw_BarChart/'
if os.path.exists(work_dir)==False:
    os.mkdir(work_dir)
if os.path.exists(plot_dir):
    shutil.rmtree(plot_dir)
os.mkdir(plot_dir)


#Process each taxa level
print "- Pool cohort group into different taxonomic level..."
for file in os.listdir(rel_taxa_dir):
    if file.endswith(".txt"):
        print file
        infile=rel_taxa_dir+file
        outfile=work_dir+file
        python_script="./barchart_table.py"
        call([python_script,design_file,infile,outfile])


#Draw piechar in R
print "- Draw Bar Chart using R..."


quit()

