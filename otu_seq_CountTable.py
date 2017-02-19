#!/usr/bin/python
import sys

"""
Make count table for unifrac.mothur
(1)Represent sequence IDs are OTU IDs
(2)Use filtered OTUs table

Format:
Representative_Sequence\ttotal\tSample1\t...
"""
def get_otus(file):
    in_fh=open(file,'r')
    count=0
    for line in in_fh:
        line=line.rstrip('\n')
        count=count+1
        list=line.split('\t',)
        if count==1:
            continue
        if count==2:
            out_fh.write('Representative_Sequence\ttotal')
            i=1
            #Last column is taxonomic information
            while i<len(list)-1:
                out_fh.write('\t'+list[i])
                i=i+1
            out_fh.write('\t\n')
        else:
            sum=int(float(list[1]))
            string=str(int(float(list[1])))
            i=2
            while i<len(list)-1:
                sum=sum+int(float(list[i]))
                string=string+'\t'+str(int(float(list[i])))
                i=i+1
            out_fh.write(list[0]+'\t'+str(sum)+'\t'+string+'\t\n')

    in_fh.close()
    return

"""
Main function
"""

if len(sys.argv)!=3:
    raise Exception ("Usage: otu_seq_CountTable.py <Path of filtered taxa OTU table with name> <Path of count table with name>")

otus_infile=sys.argv[1]
count_outfile=sys.argv[2]
out_fh=open(count_outfile,'w')
get_otus(otus_infile)
out_fh.close()

quit()
