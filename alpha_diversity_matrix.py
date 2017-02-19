#!/usr/bin/python
import sys
import re
import os
import random
import math


"""
March 11, 2014
According to the given parameters, calculate alpha diversity rafraction curve matrix
Alpha diversity: Shannon, Observed_species
"""
def get_group_info(file):
    in_fh=open(file,'r')
    for line in in_fh:
        line=line.rstrip('\n')
        list=line.split('\t',)
        #list[0] is sampleID
        #list[1] is group information
        #Only keep the samples in the two groups
        if group1==list[1] or group2==list[1]:
            dict_group[list[0]]=list[1]

    in_fh.close()
    return

def get_OTU_info(file):
    in_fh=open(file,'r')
    count=0
    for line in in_fh:
        count=count+1
        line=line.rstrip('\n')
        list=line.split('\t',)
        if count==1:
            for i,v in enumerate(list):
                if list[i]=='':
                    break
                if i>=3:
                    list_otu.append(v)
        else:
            sid=list[1]
            sum_reads_sid=0
            if sid in dict_group:
                for i,v in enumerate(list):
                    if list[i]=='':
                        break
                    if i>=3:
                        list[i]=int(list[i])
                        sum_reads_sid=sum_reads_sid+list[i]
                        if sid in dict_otu:
                            dict_otu[sid].append(v)
                        else:
                            dict_otu[sid]=[v,]

                #Filter out low abunance samples
                if sum_reads_sid>=min_reads_sample:
                    list_sampleReads.append(sum_reads_sid)

    in_fh.close()
    return
            
        
def get_counts():
    for k in dict_otu.keys():
        total_reads=0
#        list_tmp=map(int,dict_otu[k])
#        list_tmp=[int(i) for i in dict_otu[k]]
        for i,v in enumerate(dict_otu[k]):
            total_reads=total_reads+int(v)

        dict_sid[k]=total_reads

    return

def calculate_shannon(list,total_reads):
    diversity_value=0.0
    for i,iv in enumerate(list):
        p=float(iv)/float(total_reads)
        
        #Natural logarithm base
        tmp_log=math.log(p)
        diversity_value=diversity_value+p*tmp_log
    
    diversity_value=-diversity_value
    return(diversity_value)


def process_simulation(type,cycle_count):
    total_otus=len(list_otu)
    i=min
    while (i<=max_reads):
        for sid,v in dict_otu.items():
            #Store simulated results
            list=[]
            sum_reads=0
            while abs(float(sum_reads-i))/float(i)>0.01:
#                print abs(float(sum_reads-i))/float(i)
                #Get the random number
                j=random.randint(0,total_otus-1)
                if int(dict_otu[sid][j])!=0:
                    sum_reads=sum_reads+int(dict_otu[sid][j])
                
                    #If it goes over, do it again
                    if sum_reads>i*1.01:
                        sum_reads=sum_reads-int(dict_otu[sid][j])
                        continue
                    else:
                        list.append(int(dict_otu[sid][j]))
                    

            
            #When it is out while loop
#            print sid+'\t'+str(i)+'\t'+str(abs(float(sum_reads-i))/float(i))

            #Calculate diversity value according to different diversity type
            diversity_value=0.0
            if type=='observed-species':
                diversity_value=float(len(list))
            
            if type=='shannon':
                diversity_value=calculate_shannon(list,i)

            if cycle_count==1:
                if sid in dict_sim1:
                    dict_sim1[sid].append(diversity_value)
                else:
                    dict_sim1[sid]=[diversity_value,]
            else:
                if sid in dict_sim2:
                    dict_sim2[sid].append(diversity_value)
                else:
                    dict_sim2[sid]=[diversity_value,]
        
        #Next i needs to be
        i=i+step

    return



"""
Main function
"""

if len( sys.argv ) != 7:
        raise Exception( "Usage: alpha_diversity_matrix.py <shannon> <Group1: WT> <Group2: KO> <work directory> <design file> <otu shared file>")

diversity_type=sys.argv[1]
group1=sys.argv[2]
group2=sys.argv[3]
work_dir=sys.argv[4]
design_file=sys.argv[5]
shared_file=sys.argv[6]

#design_file="../output/DesignFiles/CohortGroups.design" 
#filter_dir="../output/Filter_0.03Cluster_OTU/"
#shared_file=filter_dir+'0.03Cluster_OTU_Filter.shared'

min=10
step=1000
min_reads_sample=8000

print "Get group information..."
#Get group information
#Key:sampleID
#value:group
dict_group={}
get_group_info(design_file)


print "Get OTUs information..."
#Get OTU information for each sample
#Key:sampleID
#value:number of counts for each OTU
dict_otu={}
#OTU ID
list_otu=[]
#No.reads/sample
list_sampleReads=[]
get_OTU_info(shared_file)
max_reads=10000000
for i,v in enumerate(list_sampleReads):
    if list_sampleReads[i]<step:
        continue
    if max_reads>list_sampleReads[i]:
        max_reads=list_sampleReads[i]
max_reads=int(max_reads/100)*100


#Key:sampleID
#Value:total reads in this sample
dict_sid={}
get_counts()

#*************Start simulation***************#
print "Simulate twice..."
#Key:sample ID
#values: simulated results
dict_sim1={}
print "Simulation1..."
process_simulation(diversity_type,1)
dict_sim2={}
print "Simulation2..."
process_simulation(diversity_type,2)


print "Average the simulated results..."
#Average the two simulations
dict_sim={}
for k,v in dict_sim1.items():
    for i,iv in enumerate(dict_sim1[k]):
#        print str(dict_sim1[k][i])+'\t'+str(dict_sim2[k][i])+'\t'+str(k)
        tmp_avg=float((dict_sim1[k][i]+dict_sim2[k][i])/2)
        if k in dict_sim:
            dict_sim[k].insert(i, tmp_avg)
        else:
            dict_sim[k]=[tmp_avg,]

print "Print out the results to file..."
#Output results
outfile=work_dir+diversity_type+'_'+group1+'-'+group2+'_Max'+str(max_reads)+'.txt'
out_fh=open(outfile,'w')
out_fh.write("Seq\tAvg_"+group1+"\tSD_"+group1+"\tErr_"+group1+"\tAvg_"+group2+"\tSD_"+group2+"\tErr_"+group2+"\n")
j=0
i=min
while i<=max_reads:
    sum_otus_1=0.0
    avg_otus_1=0.0
    sd_otus_1=0.0
    err_otus_1=0.0
    sum_otus_2=0.0
    avg_otus_2=0.0
    sd_otus_2=0.0
    err_otus_2=0.0

    #Calculate the average
    sample_num_1=0
    sample_num_2=0
    for sid,v in dict_sim.items():
        if dict_group[sid]==group1:
            sum_otus_1=sum_otus_1+dict_sim[sid][j]
            sample_num_1=sample_num_1+1
        else:
            if dict_group[sid]==group2:
                sum_otus_2=sum_otus_2+dict_sim[sid][j]
                sample_num_2=sample_num_2+1

    
    avg_otus_1=sum_otus_1/sample_num_1
    avg_otus_2=sum_otus_2/sample_num_2
#    print group1+'\t'+str(sum_otus_1)+'\t'+str(sample_num_1)+'\t'+group2+'\t'+str(sum_otus_2)+'\t'+str(sample_num_2)

    #Calculate SD and ERR
    tmp_1=0.0
    tmp_2=0.0
    list_1=[]
    list_2=[]
    for sid,v in dict_sim.items():
        if dict_group[sid]==group1:
            list_1.append(dict_sim[sid][j])
            tmp_1=tmp_1+(dict_sim[sid][j]-avg_otus_1)*(dict_sim[sid][j]-avg_otus_1)
        else:
            if dict_group[sid]==group2:
                list_2.append(dict_sim[sid][j])
                tmp_2=tmp_2+(dict_sim[sid][j]-avg_otus_2)*(dict_sim[sid][j]-avg_otus_2)


    
    tmp_value=float(tmp_1)/(float(sample_num_1)-1)
    sd_otus_1=math.sqrt(tmp_value)
    tmp_value=math.sqrt(sample_num_1)
    err_otus_1=sd_otus_1/tmp_value
    
    tmp_value=tmp_2/(float(sample_num_2)-1)
    sd_otus_2=math.sqrt(tmp_value)
    tmp_value=math.sqrt(sample_num_2)
    err_otus_2=sd_otus_2/tmp_value
    out_fh.write(str(i)+'\t'+str(avg_otus_1)+'\t'+str(sd_otus_1)+'\t'+str(err_otus_1)+'\t'+str(avg_otus_2)+'\t'+str(sd_otus_2)+'\t'+str(err_otus_2)+'\n')
    
    j=j+1
    i=i+step

out_fh.close()


quit()
