#!/usr/bin/python
import sys
import re
import os

"""
Filter OTUs from BIOM files
(1)In all samples, average relative abundance=1/average reads per sample
(2)In each treatment group, average relative abundance=sum rel/number of samples in the group
(3)Criteria: 
avg_rel_group=(sum of rel in this group)/number of samples in this group
detectable_rel_avg=1/(average number of read of all samples)
At least in one group avg_rel_group>=detectable_rel_avg
"""
def get_taxa_otus(file,out_fh):
	in_fh=open(file,'r')
	count=0
	for line in in_fh:
		count=count+1
		line=line.rstrip('\n')
		list=line.split('\t',)
		if count<=2:
			out_fh.write(line+'\n')
			if count==2:
				for i,v in enumerate(list):
					if i>0 and i<len(list)-1:
						list_samples.append([list[i],0])
					
			continue


		id=list[0]
		for i,v in enumerate(list):
			if i==0:
				continue

			if i!=len(list)-1:
   			        #If the value is read counts
				#Modify string to integrate for calculation 
				list[i]=float(list[i])
				list_samples[i-1][1]=list_samples[i-1][1]+list[i]
			
			#Put information into OTU dictionary
			if id not in dict_otu:
				dict_otu[id]=[list[i],]
			else:
				dict_otu[id].append(list[i])

	in_fh.close()
	return

def get_design_info(file):
	in_fh=open(file,'r')
	for line in in_fh:
		line=line.rstrip('\n')
		list=line.split('\t',)
		sid=list[0]
		gid=list[1]
		dict_design[gid]=1
		dict_design_samples[sid]=gid


	in_fh.close()
	return

def filter_taxa_otus(out_fh):
	#Sort keys
	for id in sorted(dict_otu_rel.iterkeys()):
		flag_good_otu=0
		for gid,value in dict_design.items():
			group_avg_rel=0.0
			group_num=0
			group_sum=0.0
			for i,v in enumerate(list_samples):
				if list_samples[i][0] in dict_design_samples and dict_design_samples[list_samples[i][0]]==gid:
					group_num=group_num+1
					group_sum=group_sum+dict_otu_rel[id][i]

			group_avg_rel=float(group_sum)/float(group_num)
			if group_avg_rel>=avg_rel:
				flag_good_otu=1
		
		
		#Print out OTUs, which pass filter cutoff
		#At lease one group
		if flag_good_otu==1:
			taxa_out_fh.write(id)
			for i,v in enumerate(dict_otu[id]):
				taxa_out_fh.write('\t'+str(dict_otu[id][i]))
			taxa_out_fh.write('\n')

	return


"""
Main funtions
"""
if len( sys.argv ) != 4:
        raise Exception( "Usage: filter_0.03Cluster_TaxaTable.py <input file full path> <output file full path> <design file full path>")

taxa_otu_infile=sys.argv[1]
taxa_otu_outfile=sys.argv[2]
design_file=sys.argv[3]


#Process OTUs table with taxonomic information
taxa_out_fh=open(taxa_otu_outfile,'w')
#Key:OTU id
#Values(list):all samples,[-1]taxonomy
dict_otu={}
#value:sampleID/total number of reads
list_samples=[]
get_taxa_otus(taxa_otu_infile,taxa_out_fh)

#Calculate releative abundance for each sample in each OTU
#Key:OTU id 
#Values(list):all samples of releative abundance
dict_otu_rel={}
for id,value in dict_otu.items():
	for i,iv in enumerate(dict_otu[id]):
		#Last column is taxonomy information
		if i==len(dict_otu[id])-1:
			break
		rel_value=float(dict_otu[id][i])/float(list_samples[i][1])
		if id in dict_otu_rel:
			dict_otu_rel[id].append(rel_value)
		else:
			dict_otu_rel[id]=[rel_value,]


#Calculate the average relative abundance
sum=0
count_samples=len(list_samples)
for i,iv in enumerate(list_samples):
	sum=sum+list_samples[i][1]
avg_ab=float(sum)/float(count_samples)
avg_rel=float(1)/avg_ab
#print avg_ab
#print avg_rel

#Get design file information
#Key:sampleID
#Value:group
dict_design_samples={}
#Key:groupID
#Value:1
dict_design={}
get_design_info(design_file)

#Filter OTUs according to the rule
filter_taxa_otus(taxa_out_fh)
taxa_out_fh.close()


quit()
