#!/usr/bin/python

import os
import sys
import re
from subprocess import call
import shutil


"""
(1)Calculate average reletive abundance for each treatment group for each taxa on each taxa level
(2)Draw them on the piechar
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
if len(sys.argv)!=3:
    raise Exception ("Usage of PieChart_taxa.py <taxonomic method> <output folder>")
taxa_method=sys.argv[1]
output_dir=sys.argv[2]

design_file=output_dir+'DesignFiles/CohortGroups.design'
rel_taxa_dir=output_dir+"Taxa_summary_"+taxa_method+"/taxa_summary_Filter_rel/"

work_dir=output_dir+"PieChart_taxa/"
plot_dir=work_dir+'Draw_PieChart/'
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
        python_script="./piechart_table.py"
        call([python_script,design_file,infile,outfile])


#Draw piechar in R
print "- Draw Pie Chart using R..."
r_script='./R/piechart_plot.R'
r_script_new='piechart_plot.R'
modify_r_script(r_script,r_script_new,output_dir)
call(["R","CMD","BATCH",r_script_new])

print "Pie chart plot is done!"
quit()

