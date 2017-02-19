#!/usr/bin/python

import os
import sys
import re
import math
"""
(1)Calculate the average relative abundnce of each taxa, and SD
"""

def get_design_info(file):
        in_fh=open(file,'r')
        for line in in_fh:
                line=line.rstrip('\n')
                list=line.split('\t',)
                sid=list[0]
                gid=list[1]
                dict_design[gid]=1
                dict_design_samples[sid]=[gid,]


        in_fh.close()
        return


def get_taxa_rel_info(file):
    in_fh=open(file,'r')
    count=0
    list_samples=[]
    for line in in_fh:
        line=line.rstrip("\n")
        count=count+1
        list=line.split("\t",)
        if count==1:
            i=1
            while i<len(list):
                list_samples.append(list[i])
                i=i+1
        else:
            list_taxa.append(list[0])
            i=1
            while i<len(list):
                sid=list_samples[i-1]
                if sid in dict_design_samples:
			dict_design_samples[sid].append(float(list[i]))
                i=i+1
    in_fh.close()
    return
                
def calculate_average_rel():
	#Print out the title
	out_fh.write("FullTaxa\tTaxa")
	for gid,values in dict_design.items():
		out_fh.write("\t"+gid+'\t'+gid+'_SD')
	out_fh.write('\n')

	#Print out values
	for i,iv in enumerate(list_taxa):
		list=list_taxa[i].split(";",)
		full_taxa=list_taxa[i]
		taxa=list[len(list)-1]
		out_fh.write(full_taxa+'\t'+taxa)

		#Process each group
		for gid,gvalues in dict_design.items():
			sum_rel=0.0
			sum_count=0
			sum_sd=0.0
			for sid,svalues in dict_design_samples.items():
				if dict_design_samples[sid][0]==gid:
					sum_count=sum_count+1
					j=1
					while j<len(dict_design_samples[sid]):
						if j==i+1:
							sum_rel=sum_rel+dict_design_samples[sid][j]
						j=j+1

			avg_rel=sum_rel/float(sum_count)
			for sid,svalues in dict_design_samples.items():
				if dict_design_samples[sid][0]==gid:
					j=1
					while j<len(dict_design_samples[sid]):
						if j==i+1:
							sum_sd=math.pow((dict_design_samples[sid][j]-avg_rel),2)
						j=j+1
			sd_rel=math.sqrt(sum_sd/float((sum_count-1)))
			out_fh.write('\t'+str(avg_rel)+'\t'+str(sd_rel))
		out_fh.write('\n')

	return


"""
Main function
"""
if len(sys.argv)!=4:
	raise Exception ("barchat_table.py <Design file> <taxa infile> <taxa outfile>")
	
design_file=sys.argv[1]
taxa_infile=sys.argv[2]
taxa_outfile=sys.argv[3]


#Key:group ID
#Value:1
dict_design={}
#Key:sampleID
#value:groupID,other taxa relative abundance
dict_design_samples={}
get_design_info(design_file)


list_taxa=[]
get_taxa_rel_info(taxa_infile)


out_fh=open(taxa_outfile,'w')
#Calculate average relative abundance for each treatment group
calculate_average_rel()
out_fh.close()
quit()

