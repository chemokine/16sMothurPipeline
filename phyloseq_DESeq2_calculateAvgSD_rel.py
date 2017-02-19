#!/usr/bin/python

import sys
import shutil
import os
from subprocess import call
import re
import math

"""
(1)Calculate average relative abundance for each cohort group,and combine with negative bionormial results
"""

__author__ = 'Ning Li (lin.cmb@gmail.com)'
__version__ = '3.0'
__date__ = 'November 7, 2014'


def calculate_avg_sd(rel_list):
    sum=0.0
    num_samples=len(rel_list)
    sum_sd=0.0
    for i,iv in enumerate(rel_list):
        sum=sum+rel_list[i]
    avg=sum/float(num_samples)
    
    for i,iv in enumerate(rel_list):
        sum_sd=sum_sd+math.pow((rel_list[i]-avg),2)
    sd=math.sqrt(sum_sd/float(num_samples-1))
    return(avg,sd)

#get_avg_sd(rel_infile,group1,group2,design,nb_infile,nb_outfile)
def get_avg_sd(rel,g1,g2,design,nb_infile,nb_outfile):
    #Get samples IDs in the two cohort groups
    in_fh=open(design,'r')
    #Key:sampleID
    #value:cohort
    dict_samples={}
    for line in in_fh:
        line=line.rstrip('\n')
        list=line.split('\t',)
        sid=list[0]
        group=list[1]
        if group==g1 or group==g2:
            dict_samples[sid]=group
    in_fh.close()

    #Get relative abundance information for the selected samples
    in_fh=open(rel,'r')
    #Key:taxaName
    #Values(list):relative abundance of samples
    dict_g1={}
    dict_g2={}
    #Key:idx of sample
    #Value:cohort
    dict_idx={}
    count=0
    for line in in_fh:
        count=count+1
        line=line.rstrip('\n')
        list=line.split('\t',)
        if count==1:
            i=1
            while i<len(list):
                sid=list[i]
                if sid in dict_samples:
                    dict_idx[i]=dict_samples[sid]
                i=i+1
        else:
            taxa_name=list[0]
            i=1
            while i<len(list):
                rel=float(list[i])
                if i in dict_idx:
                    group=dict_idx[i]
                    if group==g1:
                        if taxa_name in dict_g1:
                            dict_g1[taxa_name].append(rel)
                        else:
                            dict_g1[taxa_name]=[rel,]
                    else:
                        if taxa_name in dict_g2:
                            dict_g2[taxa_name].append(rel)
                        else:
                            dict_g2[taxa_name]=[rel,]
                i=i+1
    in_fh.close()


    #Calculate average relative abundance in each cohort
    in_fh=open(nb_infile,'r')
    out_fh=open(nb_outfile,'w')
    count=0
    for line in in_fh:
        count=count+1
        line=line.rstrip('\n')
        list=line.split('\t',)
        if count==1:
            out_fh.write(line+'\t'+g1+'_rel\t'+g1+'_SD\t'+g2+'_rel\t'+g2+'_SD\n')
        else:
            taxa_name=list[1]
            out_fh.write(line+'\t')
            avg_g1=0.0
            sd_g1=0.0
            avg_g2=0.0
            sd_g2=0.0
            if taxa_name in dict_g1:
                (avg_g1,sd_g1)=calculate_avg_sd(dict_g1[taxa_name])
            if taxa_name in dict_g2:
                (avg_g2,sd_g2)=calculate_avg_sd(dict_g2[taxa_name])

            out_fh.write(str(avg_g1)+'\t'+str(sd_g1)+'\t'+str(avg_g2)+'\t'+str(sd_g2)+'\n')
    in_fh.close()
    out_fh.close()
    return

"""
Main function
"""
if len(sys.argv)!=4:
    raise Exception ("Usage: phyloseq_DESeq2_calculateAvgSD_rel.py <parameter file for run phyloseq R> <design file> <taxa relative abundance directory>")

para_outfile=sys.argv[1]
design=sys.argv[2]
rel_dir=sys.argv[3]

#Process each file
para_infh=open(para_outfile,'r')
for line in para_infh:
    line=line.rstrip('\n')
    list=line.split('\t',)
    nb_infile=list[-1]
    nb_outfile=nb_infile.replace('.txt','_relSD.txt')

    list1=nb_infile.split('/',)
    #list[-1] 'DESeq2_nbinomWaldTest_pAdjust-BH_L2_C57WT-TrpM5KO.txt'
    list1[-1]=list1[-1].replace('.txt','')
    list2=list1[-1].split('_',)
    list3=list2[-1].split('-')
    rel_infile=rel_dir+'Taxa_'+list2[-2]+'.txt'
    group1=list3[0]
    group2=list3[1]
    
    #Get average relative abundance and combine with ng results
    get_avg_sd(rel_infile,group1,group2,design,nb_infile,nb_outfile)

para_infh.close()    
quit()
