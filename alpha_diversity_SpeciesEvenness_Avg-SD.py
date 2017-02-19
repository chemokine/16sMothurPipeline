#!/usr/bin/python
import sys
import re
import os
import shutil
from subprocess import call
import math

"""
Calculate species evenness different cohort groups
J=H'/Hmax
H' i the number derived from Shannon diversity index
Hmax=lnS (S is the observed species in the sample)
(1)Use filtering OTUs table
(2)Calculate average of species evenness in each cohort
(3)Calculate SD for each cohort
(4)Modify R script and plot bar with s.d.
"""
def get_cohort_info(file):
    in_fh=open(file,'r')
    for line in in_fh:
        line=line.rstrip("\n")
        list=line.split('\t',)
        sid=list[0]
        cohort=list[1]
        if cohort in dict_cohort:
            dict_cohort[cohort].append(sid)
        else:
            dict_cohort[cohort]=[sid,]
    in_fh.close()
    return


def get_singleSample_Shannon(file):
    in_fh=open(file,'r')
    count=0
    for line in in_fh:
        count=count+1
        line=line.rstrip("\n")
        list=line.split('\t',)
        if count>1:
            sid=list[0]
            dict_shannon[sid]=float(list[-1])

    in_fh.close()
    return

def get_singleSample_ObservedSpecies(file):
    in_fh=open(file,'r')
    count=0
    for line in in_fh:
        count=count+1
        line=line.rstrip("\n")
        list=line.split('\t',)
        if count>1:
            sid=list[0]
            dict_observedspecies[sid]=float(list[-1])

    in_fh.close()
    return

def calculate_SpeciesEvenness():
    for key,values in dict_cohort.items():
        for i,iv in enumerate(dict_cohort[key]):
            sid=dict_cohort[key][i]
            if sid in dict_shannon and sid in dict_observedspecies:
                evenness=dict_shannon[sid]/math.log(dict_observedspecies[sid])
                dict_sample_speciesevenness[sid]=evenness
                single_outfh.write(sid+'\t'+key+'\t'+str(evenness)+'\n')

    return

def calculate_SpeciesEvenness_avg():
    for key,values in dict_cohort.items():
        #Calculate average value of mice at each time point
        sum=0.0
        num_samples=float(len(dict_cohort[key]))
        for i,iv in enumerate(dict_cohort[key]):
            sid=dict_cohort[key][i]
            if sid in dict_sample_speciesevenness:
                sum=sum+dict_sample_speciesevenness[sid]
        avg=sum/num_samples

        #Calculate SD and SE
        sum=0.0
        for i,iv in enumerate(dict_cohort[key]):
            sid=dict_cohort[key][i]
            if sid in dict_sample_speciesevenness:
                sum=sum+math.pow((dict_sample_speciesevenness[sid]-avg),2)
        sd=math.sqrt(sum/num_samples)
        err=sd/math.sqrt(num_samples)
        dict_shannon[key]=[avg,sd,err]

    return
    
def modify_r_script(infile,outfile,output_dir):
    in_fh=open(infile,'r')
    out_fh=open(outfile,'w')
    for line in in_fh:
        if re.search("../output/",line):
            line=line.replace("../output/",output_dir)

        if re.match('row_num=',line):
            out_fh.write('row_num='+str(num_cohort)+'\n')
        else:
            if re.match('y_max=',line):
                out_fh.write('y_max='+str(y_max)+'\n')
            else:
                out_fh.write(line)
    in_fh.close()
    out_fh.close()
    return


"""
Main function
"""
if len(sys.argv)!=7:
    raise Exception ("Useage of alpha_diversity_SpeciesEvenness_Avg-SD.py <Full path of R script to plot bar and s.d.> <current work directory> <design file> <single sample shannon info> <single sample observed species> <output folder>")

r_script=sys.argv[1]
work_dir=sys.argv[2]
design_file=sys.argv[3]
shannon_file=sys.argv[4]
observedspecies_file=sys.argv[5]
output_dir=sys.argv[6]

#design_file="../output/DesignFiles/CohortGroups.design"
#filter_dir="../output/Filter_0.03Cluster_OTU/"
#shared_file=filter_dir+'0.03Cluster_OTU_Filter.shared'

single_outfile=work_dir+'SpeciesEvenness_singleSample.txt'
single_outfh=open(single_outfile,'w')
single_outfh.write("SampleID\tCohortGroups\tSpeciesEvenness\n")
average_outfile=work_dir+'SpeciesEvenness_Avg-SD.txt'
avg_outfh=open(average_outfile,'w')
avg_outfh.write("CohortGroups\tAvg_SpeciesEvenness\tSD_SpeciesEvenness\tErr_SpeciesEvenness\n")

#Get OTUs table
#print "Get OTUs table..."
#Key:Cohort name
#Values (list):sampleID
dict_cohort={}
get_cohort_info(design_file)


#Key:SampleID
#Value:shannon value
dict_shannon={}
get_singleSample_Shannon(shannon_file)

#Key:sampleID
#Value:observed species
dict_observedspecies={}
get_singleSample_ObservedSpecies(observedspecies_file)

#Calculate species evenness for each sample
#print "Calculate species evenness for each sample..."
#Key:sampleID
#Value:species evenness
dict_sample_speciesevenness={}
calculate_SpeciesEvenness()


#Calculate average for each time point across samples
#print "Calculate average for each time point across samples..."
#Key: cohort
#Values:avg,sd,err
dict_shannon={}
calculate_SpeciesEvenness_avg()

        
#Print out
num_cohort=0
y_max=-10
for key in sorted(dict_shannon.keys()):
    num_cohort=num_cohort+1
    avg_outfh.write(key)
    for i,iv in enumerate(dict_shannon[key]):
        if dict_shannon[key][i]>y_max:
            y_max=dict_shannon[key][i]
        avg_outfh.write('\t'+str(dict_shannon[key][i]))
    avg_outfh.write('\n')
avg_outfh.close()
single_outfh.close()
y_max=int(y_max+1.5)

#Modify r script of number of cohort
list_names=r_script.split('/',)
new_r_script=work_dir+list_names[-1]
modify_r_script(r_script,new_r_script,output_dir)
call(["R","CMD","BATCH",new_r_script])


quit()
