#!/usr/bin/python

import os
import sys
import re
from Bio import SeqIO

def count_reads(file,file_type):
    count_reads=0
    for record in SeqIO.parse(file,file_type):
        count_reads=count_reads+1

    return(count_reads)


"""
Main function
"""
if len(sys.argv)!=3:
    raise Exception ("Usage: count_ReadsSample.pl <fastq folder: ./All_fastq/> <output file path>")

fq_dir=sys.argv[1]
out_file=sys.argv[2]
out_fh=open(out_file,'w')
out_fh.write("SampleID\tReadCounts\n")

#Key:sid
#value: counts
dict_reads={}
for file in os.listdir(fq_dir):
    if file.endswith(".fastq") and re.search('R1',file):
        print file
        fq_file=fq_dir+file
        sid=re.sub('.fastq','',file)
        dict_reads[sid]=count_reads(fq_file,'fastq')


#Print out information
for sid in sorted(dict_reads.keys()):
    out_fh.write(sid+'\t'+str(dict_reads[sid])+'\n')

out_fh.close()
quit()

    
    
