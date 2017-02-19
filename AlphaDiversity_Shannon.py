#!/usr/bin/python

import sys
import shutil
import os
from subprocess import call
import re

"""
(1)Run batch alpha diversity
(2)Run R to plot rarefacation figures for alpha diversity
(3)Calculate Shannon Entropy for single samples, average & SD
(4)Statistical testing on shannon value for between cohort groups

(5)(6)Observed species
(7)(8)Species evenness
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
        for i,iv in enumerate(list_diversity):
            tmp_list=[]
            tmp_list.append(list_diversity[i])
            for j,jv in enumerate(list):
                tmp_list.append(list[j])
            list_para.append(tmp_list)

    return


def calculate_max_y(file):
    in_fh=open(file,'r')
    count=0
    max_y=0.0
    for line in in_fh:
        count=count+1
        if count==1:
            continue

        line=line.rstrip('\n')
        list=line.split('\t',)
        y=float(list[1])+float(list[2])
        if y>max_y:
            max_y=y

        y=float(list[4])+float(list[5])
        if y>max_y:
            max_y=y

    in_fh.close()
    return(max_y)


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
    raise Exception ("Usage: Calculate_countsSample.py <input folder> <output folder>")

input_dir=sys.argv[1]
output_dir=sys.argv[2]

design_file=output_dir+"DesignFiles/CohortGroups.design"
#This shared file is the input for simulation, which could be filtered or before filtering
filter_dir=output_dir+"Filter_0.03Cluster_OTU/"
shared_file=filter_dir+'0.03Cluster_OTU_Filter.shared'   
#mothur_run="../output/mothur/Mothur_pipeline/mothur_run/"
#shared_file=mothur_run+"stability.R1.trim.good.unique.good.filter.unique.precluster.pick.pick.an.unique_list.shared"

work_dir=output_dir+"AlphaDiversity/"
list_diversity=['shannon','observed-species']
if os.path.exists(work_dir)==False:
    os.mkdir(work_dir)
plot_dir=work_dir+'alpha_diversity_plot/'
if os.path.exists(plot_dir):
    shutil.rmtree(plot_dir)
os.mkdir(plot_dir)


#(1)Run alpha diversity one by one
print "- Simulate alpha diversity rarefaction curve table..."
#Get parameter file
listfile=work_dir+"AlphaDiversity_ParametersList.txt"
shutil.copy(input_dir+'CohortGroups_ParametersList.txt',listfile)
list_para=[]
get_parameter_list(listfile)

for i,iv in enumerate(list_para):
    diversity=list_para[i][0]
    group1=list_para[i][1]
    group2=list_para[i][2]
    
    print diversity+'\t'+group1+'\t'+group2+'\n'
    python_script="./alpha_diversity_matrix.py"
    call([python_script,diversity,group1,group2,work_dir,design_file,shared_file])



#(2)Plot alpha diversity figures
print "- Plot alpha diversity rarefaction curves..."
plot_parameter_list=work_dir+'AlphaDiversity_plotList.txt'
out_fh=open(plot_parameter_list,'w')
for file in os.listdir(work_dir):
        if file.endswith(".txt") and (re.search('observed',file) or re.search('shannon',file)):
            name=file.replace('.txt','')
            infile=work_dir+file
            outfile=plot_dir+name+'.pdf'

            list=name.split('_',)
            type=list[0]


            max_x=list[2].replace('Max','')
            max_x=int(max_x)+100
            max_y=calculate_max_y(infile)
            max_y=int(max_y)

            title=''
            if type=='shannon':
                title='Shannon_entropy'
                max_y=max_y+1
            else:
                if type=='observed-species':
                    title='OTU_number'
                    max_y=max_y+10


            list_groups=list[1].split('-',)
            group1=list_groups[0]
            group2=list_groups[1]
            out_fh.write(infile+'\t'+outfile+'\t'+type+'\t'+title+'\t'+str(max_x)+'\t'+str(max_y)+'\t'+group1+'\t'+group2+'\n')
            
out_fh.close()


#Run R
r_script='./R/alpha_diversity_errbar_plot.R'
r_script_new='alpha_diversity_errbar_plot.R'
modify_r_script(r_script,r_script_new,output_dir)
call(["R","CMD","BATCH",r_script_new])


#Shannon
#(3)Calculate average and SD of Shannon entropy for each cohort group
print "- Calculate average of Shannon Entropy and SD for each cohort group!"
#Get script for plot bar and s.d.
r_script='./R/Shannon_Avg-SD_bar.R'
python_script='./alpha_diversity_Shannon_Avg-SD.py'
call([python_script,r_script,work_dir,design_file,shared_file,output_dir])


#(4)Statistical testing on shannon value for between cohort groups 
print "- Statistical testing on shannon value for between cohort groups!"
python_script="./alpha_diversity_Shannon_pvalues.py"
shannon_table=work_dir+'Shannon_singleSample.txt'
r_script=work_dir+'Shannon_singleSample_test.R'
pvalue_file=work_dir+'Shannon_singleSample_Pvalues.txt'
call([python_script,shannon_table,listfile,r_script,pvalue_file])

#Observed species
#(5)Calculate average and SD of observed species for each cohort group
print "- Calculate average of observed species and SD for each cohort group!"
#Get script for plot bar and s.d.
r_script='./R/ObservedSpecies_Avg-SD_bar.R'
python_script='./alpha_diversity_ObservedSpecies_Avg-SD.py'
call([python_script,r_script,work_dir,design_file,shared_file,output_dir])


#(6)Statistical testing on observed value for between cohort groups 
print "- Statistical testing on observed species value for between cohort groups!"
python_script="./alpha_diversity_ObservedSpecies_pvalues.py"
observedspecies_table=work_dir+'ObservedSpecies_singleSample.txt'
r_script=work_dir+'ObservedSpecies_singleSample_test.R'
pvalue_file=work_dir+'ObservedSpecies_singleSample_Pvalues.txt'
call([python_script,observedspecies_table,listfile,r_script,pvalue_file])


#Species evenness based on Shannon and observed species
#(7)Calculate average and SD of species evenness for each cohort group
print "- Calculate average of species evenness and SD for each cohort group!"
#Get script for plot bar and s.d.
r_script='./R/SpeciesEvenness_Avg-SD_bar.R'
python_script='./alpha_diversity_SpeciesEvenness_Avg-SD.py'
observedspecies_table=work_dir+'ObservedSpecies_singleSample.txt'
shannon_table=work_dir+'Shannon_singleSample.txt'
call([python_script,r_script,work_dir,design_file,shannon_table,observedspecies_table,output_dir])


#(8)Statistical testing on observed value for between cohort groups 
print "- Statistical testing on species evenness value for between cohort groups!"
python_script="./alpha_diversity_SpeciesEvenness_pvalues.py"
speciesevenness_table=work_dir+'SpeciesEvenness_singleSample.txt'
r_script=work_dir+'SpeciesEvenness_singleSample_test.R'
pvalue_file=work_dir+'SpeciesEvenness_singleSample_Pvalues.txt'
call([python_script,speciesevenness_table,listfile,r_script,pvalue_file])


print "Alpha diversity plot is done!"
quit()
