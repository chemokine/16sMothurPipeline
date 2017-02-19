#!/usr/bin/python

import sys
import shutil
import os
from subprocess import call
import re
import math

"""
Prepare files for  phyloseq wrapped with DESeq2 to compute negative binormial for feature selection
(1)Generate parameter file for R script
(2)Split taxa file for each pair of cohort groups, and convert them into BIOM file
"""

__author__ = 'Ning Li (lin.cmb@gmail.com)'
__version__ = '3.0'
__date__ = 'November 7, 2014'

def get_map_infile(g1,g2,design_infile,map_outfile):
    in_fh=open(design_infile,'r')
    out_fh=open(map_outfile,'w')
    out_fh.write('#SampleID\tDescription\n')
    for line in in_fh:
        line=line.rstrip('\n')
        list=line.split('\t',)
        sid=list[0]
        group=list[1]
        if group==g1 or group==g2:
            out_fh.write(line+'\n')
    in_fh.close()
    out_fh.close()
    return

def get_biom_infile(taxa_infile,taxa_outfile,biom_outfile,map_infile):
    #Get samples from map_infile, which includes samples in the two cohort groups
    in_fh=open(map_infile,'r')
    count=0
    #Key:sampleID
    #value:cohort
    dict_samples={}
    for line in in_fh:
        count=count+1
        if count>1:
            line=line.rstrip('\n')
            list=line.split('\t',)
            sid=list[0]
            group=list[1]
            dict_samples[sid]=group
    in_fh.close()

    #Get counts information for those samples
    in_fh=open(taxa_infile,'r')
    out_fh=open(taxa_outfile,'w')
    count=0
    #Key:sample's idx
    #Value:1 or 0 (in those two cohort groups or not)
    dict_idx={}
    for line in in_fh:
        count=count+1
        line=line.rstrip('\n')
        list=line.split('\t',)
        if count==1:
            out_fh.write(list[0])
            i=1
            while i<len(list):
                if list[i] in dict_samples:
                    dict_idx[i]=1
                    out_fh.write('\t'+list[i])
                else:
                    dict_idx[i]=0
                i=i+1
            out_fh.write('\n')
        else:
            out_fh.write(list[0])
            i=1
            while i<len(list):
                if dict_idx[i]==1:
                    out_fh.write('\t'+list[i])
                i=i+1
            out_fh.write('\n')
    in_fh.close()
    out_fh.close()

    #Convert count table to BIOM table
    #BIOM1.0
    #convert_biom.py -i Taxa_L6.txt --biom_table_type="taxon table" -o Taxa_L6.biom
    #BIOM2.1
    #biom convert -i Taxa_L2_Control-MS.txt -o Taxa_L2_Control-MS_json.biom --table-type="OTU table" --to-json
    command="biom convert -i "+taxa_outfile+" -o "+biom_outfile+' --table-type="Taxon table" --to-json'
    os.system(command)
            
    return

def get_parameters_files(infile,outfile):
    in_fh=open(infile,'r')
    out_fh=open(outfile,'w')
    count=0
    for line in in_fh:
        count=count+1
        if count>1:
            line=line.rstrip('\n')
            list=line.split('\t',)
            group1=list[0]
            group2=list[1]
            designfile=design_dir+list[-1]
            
            #Only keep the two cohort groups and the samples
            map_infile=input_dir+'CohortGroups_'+group1+'-'+group2+'.txt'
            get_map_infile(group1,group2,designfile,map_infile)

            #Taxa level from L2 to L6
            #Process all of the taxa levels for this pair cohort groups
            for file in os.listdir(ab_dir):
                taxa_originalfile=ab_dir+file
                taxa_rank=file.replace('Taxa_','')
                taxa_rank=taxa_rank.replace('.txt','')

                taxa_infile=input_dir+'Taxa_'+taxa_rank+'_'+group1+'-'+group2+'.txt'
                biom_infile=input_dir+'Taxa_'+taxa_rank+'_'+group1+'-'+group2+'.biom'
                outfile=nb_dir+'DESeq2_nbinomWaldTest_pAdjust-BH_'+taxa_rank+'_'+group1+'-'+group2+'.txt'
                out_fh.write(biom_infile+'\t'+map_infile+'\t'+outfile+'\n')
                
                get_biom_infile(taxa_originalfile,taxa_infile,biom_infile,map_infile)

    in_fh.close()
    out_fh.close()
    return

"""
Main function
"""
if len(sys.argv)!=7:
    raise Exception ("Usage: phyloseq_DESeq2_makingFiles.py <para_infile> <para_outfile> <design_dir> <ab_taxa_dir> <nb_input_dir> <nb_output_dir>")

para_infile=sys.argv[1]
para_outfile=sys.argv[2]
design_dir=sys.argv[3]
ab_dir=sys.argv[4]
input_dir=sys.argv[5]
nb_dir=sys.argv[6]

get_parameters_files(para_infile,para_outfile)
quit()
