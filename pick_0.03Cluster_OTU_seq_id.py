#!/usr/bin/python
import sys
import re
import os
import Bio
from Bio import SeqIO

"""
(1)Get all unique reads for each OTU
Inputs from 'mothur_pipeline'
stability.trim.contigs.good.unique.good.filter.unique.precluster.pick.pick.an.unique_list.list
stability.trim.contigs.good.unique.good.filter.unique.precluster.uchime.pick.pick.count_table
stability.trim.contigs.good.unique.good.filter.unique.precluster.pick.pick.fasta
(2)Pick the most abundant unique read for each OTU using all unique reads belonged to this OTU
Rule:
new sequence ID is OTU ID
represent sequence: the most abunant unique read

Output
0.03Cluster_OTU_seq.fasta (gaps, with #reads)
0.03Cluster_OTU_seq.names
"""
def get_unique_seqs(file,file_type):
    for seq_record in SeqIO.parse(file,file_type):
        seq_id=seq_record.id
        dict_unique[seq_id]=[str(seq_record.seq),0]

    return

def get_unique_counts(file):
    in_fh=open(file,'r')
    count_line=0
    for line in in_fh:
        count_line=count_line+1
        line=line.rstrip('\n')
        list=line.split('\t',)
        if count_line>1:
            rid=list[0]
            i=1
            sum_counts=int(list[1])
            if rid in dict_unique:
                dict_unique[rid][1]=sum_counts
    in_fh.close()
    return
            

                
def pick_OTU_seq(file):
    in_fh=open(file,'r')
    #Keep all of the OTU ID
    list_otu=[]
    count_line=0
    for line in in_fh:
        line=line.rstrip('\n')
        list=line.split("\t",)
        count_line=count_line+1

        #Get OTU IDs
        if count_line==1:
            i=2
            while i<len(list) and list[i]!='':
                list_otu.append(list[i])
                i=i+1
            continue

        if(list[0]==str(cutoff)):
            i=2
            while i<len(list) and list[i]!='':
                ##In each group, it may have more than one rid, separated by ','
                tmp_list=[]
                tmp_list=list[i].split(',',)
                otu_id=list_otu[i-2]

                #Go through all of the unique sequences, and make consensus sequence
                seq=''
                num_seq=len(tmp_list)
                if num_seq==1:
                    seq=dict_unique[tmp_list[0]][0]
                else:
                    max_counts=0
                    for k,kv in enumerate(tmp_list):
                        rid=tmp_list[k]
                        if rid in dict_unique:
                            if dict_unique[rid][1]>max_counts:
                                seq=dict_unique[rid][0]
                                max_counts=dict_unique[rid][1]
                                    
                 #Print out the sequence of this OTU in fast file
                fa_fh.write('>'+otu_id+'\n'+seq+'\n')

                #Print out for name file
                #otu_id\tother unique sequences
                name_fh.write(otu_id+'\t')
                string=tmp_list[0]                
                for j in range(len(tmp_list)):
                    if j==0:
                        continue
                    string=str(string+','+tmp_list[j])
                    
                if string!='':
                    name_fh.write(string+'\n')

                i=i+1    


    in_fh.close()
    return



   

"""
Main function
"""
if len( sys.argv ) != 3:
        raise Exception( "Usage: pick_OTU_seq_id.py <input directory> <output directory>")

#../output/mothur/Mothur_pipeline/mothur_run/
indir=sys.argv[1]
#../output/Pick_OTU_seq/
outdir=sys.argv[2]

#Get input file's name
cluster_infile=indir+'stability.trim.contigs.good.unique.good.filter.unique.precluster.pick.pick.an.unique_list.list'
fa_infile=indir+'stability.trim.contigs.good.unique.good.filter.unique.precluster.pick.pick.fasta'
count_infile=indir+'stability.trim.contigs.good.unique.good.filter.unique.precluster.uchime.pick.pick.count_table'
cutoff=0.03

#Get output files' names
fa_outfile=outdir+str(cutoff)+'Cluster_OTU_seq.fasta'
name_outfile=outdir+str(cutoff)+'Cluster_OTU_seq.names'
fa_fh=open(fa_outfile,'w')
name_fh=open(name_outfile,'w')

#Get unique reads' IDs and sequences
#Key:rid
#Value:sequence/read counts
dict_unique={}
print "- Get unique sequences..."
get_unique_seqs(fa_infile,'fasta')
print "- Get read counts for each unique sequence..."
get_unique_counts(count_infile)
print "Pick one read for each OTU..."
pick_OTU_seq(cluster_infile)

fa_fh.close()
name_fh.close()
quit()
