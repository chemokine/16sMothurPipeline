#!/usr/bin/python
import sys
import re
import os
import Bio
from Bio import SeqIO

"""
(1)Get the filtered OTUs list from Filter_OTUs
(2)Get those OTUs represent reads
(3)Build names and fasta file

Inputs:
OTUs_Filter.shared (only need OTU IDs)
0.03Cluster_OTU_seq.fasta (gaps,OTU ID as represent read ID)
0.03Cluster_OTU_seq.names

Outputs:
0.03Cluster_OTU_seq_Filter.fasta
0.03Cluster_OTU_seq_Filter.names
"""
def get_otus(file):
    in_fh=open(file,'r')
    count_line=0
    for line in in_fh:
        line=line.rstrip('\n')
        list=line.split("\t",)
        count_line=count_line+1

        #Get OTU IDs
        if count_line==1:
            i=3
            while i<len(list) and list[i]!='':
                dict_otus[list[i]]=1
                i=i+1
            break
    in_fh.close()
    return


def get_names(file):
    in_fh=open(file,'r')
    for line in in_fh:
        line=line.rstrip('\n')
        list=line.split("\t",)
        if list[0] in dict_otus:
            names_outfh.write(line+'\n')

    in_fh.close()
    return


def get_seq(file,file_type):
    for seq_record in SeqIO.parse(file,file_type):
        oid=seq_record.id
        if oid in dict_otus:
            fasta_outfh.write('>'+oid+'\n'+str(seq_record.seq)+'\n')
    
    return



   

"""
Main function
"""
if len(sys.argv)!=4:
    raise Exception( "Usage: filter_RepresentSeq4OTUs_rid.py <filtered shared table full path> <indir> <outdir>")

otus_infile=sys.argv[1]
indir=sys.argv[2]
outdir=sys.argv[3]

names_infile=indir+"0.03Cluster_OTU_seq.names"
fasta_infile=indir+"0.03Cluster_OTU_seq.fasta"

names_outfile=outdir+"0.03Cluster_OTU_seq_Filter.names"
names_outfh=open(names_outfile,'w')
fasta_outfile=outdir+"0.03Cluster_OTU_seq_Filter.fasta"
fasta_outfh=open(fasta_outfile,'w')

#Get filtered OTU list
#Key:OTU ID
#value:1
dict_otus={}
get_otus(otus_infile)

get_names(names_infile)
get_seq(fasta_infile,'fasta')
names_outfh.close()
fasta_outfh.close()
quit()
