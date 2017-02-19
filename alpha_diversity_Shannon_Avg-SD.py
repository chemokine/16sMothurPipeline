#!/usr/bin/python
import sys
import re
import os
import shutil
from subprocess import call
import math

"""
Calculate Shannon entropy different cohort groups
(1)Use filtering OTUs table
(2)Calculate average of Shannon entropy in each cohort
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


def get_OTUs(file):
    in_fh=open(file,'r')
    count=0
    for line in in_fh:
        count=count+1
        line=line.rstrip("\n")
        list=line.split('\t',)
        if count>1:
            sid=list[1]
            #Put read counts of each OTU for each mouse
            dict_samples[sid]=[0,]
            i=3
            sum=0
            while i<len(list):
                dict_samples[sid].append(int(list[i]))
                sum=sum+int(list[i])
                i=i+1
            dict_samples[sid][0]=sum

    in_fh.close()
    return

def calculate_shannon():
    for key,values in dict_cohort.items():
        for i,iv in enumerate(dict_cohort[key]):
            sid=dict_cohort[key][i]
            if sid in dict_samples:
                sum=0.0
                total_reads=dict_samples[sid][0]
                j=1
                while j<len(dict_samples[sid]):
                    p=float(dict_samples[sid][j])/float(total_reads)
                    if p>0:

#                        sum=sum+p*math.log10(p)
                        sum=sum+p*math.log(p)

                    j=j+1
                shannon=math.fabs(sum)
                dict_sample_shannon[sid]=shannon
                single_outfh.write(sid+'\t'+key+'\t'+str(shannon)+'\n')

    return

def calculate_shannon_avg():
    for key,values in dict_cohort.items():
        #Calculate average value of mice at each time point
        sum=0.0
        num_samples=float(len(dict_cohort[key]))
        for i,iv in enumerate(dict_cohort[key]):
            sid=dict_cohort[key][i]
            if sid in dict_sample_shannon:
                sum=sum+dict_sample_shannon[sid]
        avg=sum/num_samples

        #Calculate SD and SE
        sum=0.0
        for i,iv in enumerate(dict_cohort[key]):
            sid=dict_cohort[key][i]
            if sid in dict_sample_shannon:
                sum=sum+math.pow((dict_sample_shannon[sid]-avg),2)
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
if len(sys.argv)!=6:
    raise Exception ("Useage of alpha_diversity_Shannon_Avg-SD.py <Full path of R script to plot bar and s.d.> <current work directory> <design file> <otu shared file> <output folder>")

r_script=sys.argv[1]
work_dir=sys.argv[2]
design_file=sys.argv[3]
shared_file=sys.argv[4]
output_dir=sys.argv[5]

#design_file="../output/DesignFiles/CohortGroups.design"
#filter_dir="../output/Filter_0.03Cluster_OTU/"
#shared_file=filter_dir+'0.03Cluster_OTU_Filter.shared'

single_outfile=work_dir+'Shannon_singleSample.txt'
single_outfh=open(single_outfile,'w')
single_outfh.write("SampleID\tCohortGroups\tShannonEntropy\n")
average_outfile=work_dir+'Shannon_Avg-SD.txt'
avg_outfh=open(average_outfile,'w')
avg_outfh.write("CohortGroups\tAvg_Shannon\tSD_Shannon\tErr_Shannon\n")

#Get OTUs table
#print "Get OTUs table..."
#Key:Cohort name
#Values (list):sampleID
dict_cohort={}
get_cohort_info(design_file)

#Key:sampleID
#Values (list):total reads/reads in this OTUs...
dict_samples={}
get_OTUs(shared_file)

#Calculate shannon for each sample
#print "Calculate shannon for each sample..."
#Key:sampleID
#Value:shannon value
dict_sample_shannon={}
calculate_shannon()


#Calculate average for each time point across samples
#print "Calculate average for each time point across samples..."
#Key: cohort
#Values:avg,sd,err
dict_shannon={}
calculate_shannon_avg()

        
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
