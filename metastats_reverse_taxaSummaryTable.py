#!/usr/bin/python
import sys
import re
import os

######################################
#Similar function as 
#Reverse_TaxaSummaryTable_metastats.pl
######################################
if len( sys.argv ) != 3:
        raise Exception( "Usage: Reverse_TaxaSummaryTable_metastats.py <taxa_summary_Filter_ab> <Reverse_taxa_summaryTable_ab>")

dir=sys.argv[1]
outdir=sys.argv[2]

for file in os.listdir(dir):
	if file.endswith(".txt"):
		infile=dir+file
		name=file.replace(".txt",'_reverse.txt')
		outfile=outdir+name
		in_fh=open(infile,'r')
		out_fh=open(outfile,'w')
	    
	        #Get original taxa table
		LL_info=[]
		L_sample=[]
		count=0
		for line in in_fh:
			count=count+1
			line=line.rstrip('\n')
			list=line.split('\t',)
		    
			#Store all of the titles
			if count==1:
				for idx, val in enumerate(list):
					if idx>0:
						L_sample.append(val)
			else:       
                                #Store all of the information
				LL_info.append(list)

		in_fh.close()

                #Print out the titles
		out_fh.write("label\tGroup\tnumTaxa")
		for idx, val in enumerate(LL_info):
			out_fh.write("\t"+LL_info[idx][0])
		out_fh.write("\n")

		#Print out values
		for idx,val in enumerate(L_sample):
			numtaxa=count-1
			string=str("unique\t"+str(L_sample[idx])+"\t"+str(numtaxa))
			out_fh.write(string)
			i=0
			while i<len(LL_info):
				if re.search('_ab',outdir):
					read_counts=int(float(LL_info[i][idx+1]))
					out_fh.write('\t'+str(read_counts))
				else:
					out_fh.write('\t'+str(LL_info[i][idx+1]))
				i=i+1
			out_fh.write("\n")

		out_fh.close()

quit()
