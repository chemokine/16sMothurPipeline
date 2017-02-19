#!/usr/bin/python
import sys


"""
March 31, 2014
Calculate counts of reads per sample.

stability.R1.trim.good.count_table has #reads/sample after trim low quality bases and screen away reads (short, maxambig)
stability.R1.trim.good.unique.good.filter.count_table has #reads/sample after filter bad alignment and reads with long polymers
stability.R1.trim.good.unique.good.filter.unique.precluster.uchime.pick.count_table has #reads/sample after chimera checking and removing chimera
"""

#Get input file's name from stdin
#dir="../output/mothur/"
dir='../'
if len( sys.argv ) != 3:
        raise Exception( "Usage: count_group.py <input file> <output file>" )


infile=sys.argv[1]
outfile=sys.argv[2]


#Read information from input file
in_fh=open(infile,"r")
#sampleID[i][0],total counts[i][1]
list_samples=[]
list_counts=[]
count=0
for line in in_fh:
    line=line.rstrip('\n')
    count=count+1
    list=line.split('\t',)

    if count==1:
	    for i,iv in enumerate(list):
		    if i>=2 and list[i]!='':
			    list_samples.append(list[i])
			    list_counts.append(0)
    else:
	    for i,iv in enumerate(list):
		    if i>=2 and list[i]!='':
			    idx=i-2
			    list_counts[idx]=list_counts[idx]+int(list[i])
		    

in_fh.close()


#Print out information
out_fh=open(outfile,"w")
out_fh.write("SampleID\tNumReadsPerSample\n")
for i,iv in enumerate(list_samples):
	out_fh.write(list_samples[i]+'\t'+str(list_counts[i])+'\n')


out_fh.close()
quit()
