#!/usr/bin/python
import sys
import re
import os

"""
Filter OTUs from .shared files
(1)Use filtered BIOM file, for the .shared file OTUs filter
(2)The same criteria as BIOM file filter
"""
def get_taxa_otus(file):
        in_fh=open(file,'r')
        count=0
        for line in in_fh:
                count=count+1
                line=line.rstrip('\n')
                list=line.split('\t',)
                if count>2:
			id=list[0]
			dict_taxa_otu[id]=1
	in_fh.close()
	return


def get_shared_otu(file):
	in_fh=open(file,'r')
        count=0
        for line in in_fh:
                count=count+1
                line=line.rstrip('\n')
		list=line.split('\t',)
                if count==1:
			for i,v in enumerate(list):
				if i<3 or list[i]=='':
					continue
				else:
					id=list[i]
					if id in dict_taxa_otu:
						list_otu.append([list[i],1])
					else:
						list_otu.append([list[i],0])
                        continue


                sid=list[1]
                for i,v in enumerate(list):			
                        if i<3 or list[i]=='':
                                continue
                        if sid not in dict_otu:
                                dict_otu[sid]=[list[i],]
                        else:
                                dict_otu[sid].append(list[i])

        in_fh.close()
        return


def filter_shared_otu(out_fh):
	num_passed_otus=0
	#Print out all of the information
	out_fh.write("label\tGroup\tnumOtus")
	for i,iv in enumerate(list_otu):
		if list_otu[i][1]==1:
			num_passed_otus=num_passed_otus+1
			out_fh.write("\t"+list_otu[i][0])
	out_fh.write("\n")

	for sid,values in dict_otu.items():
		out_fh.write("0.03\t"+sid+'\t'+str(num_passed_otus))
		for i,iv in enumerate(list_otu):
			if list_otu[i][1]==1:
				out_fh.write('\t'+str(dict_otu[sid][i]))
		out_fh.write("\n")

	
	return



"""
Main funtions
"""
if len( sys.argv ) != 4:
        raise Exception( "Usage: filter_0.03Cluster_SharedTable.py <filtered taxa OTUs table> <input shared file> <output shared file>")
taxa_otu_infile=sys.argv[1]
shared_otu_infile=sys.argv[2]
shared_otu_outfile=sys.argv[3]

#Key:otuID
#Value:1
dict_taxa_otu={}
get_taxa_otus(taxa_otu_infile)


#Process OTUs table without taxonomic information from .shared file
shared_out_fh=open(shared_otu_outfile,'w')
#Key:sampleID
#Values(list):all OTUs
dict_otu={}
#[0]OTU name,[1]1 or 0, keep or filtered out
list_otu=[]
get_shared_otu(shared_otu_infile)
filter_shared_otu(shared_out_fh)
shared_out_fh.close()

quit()
