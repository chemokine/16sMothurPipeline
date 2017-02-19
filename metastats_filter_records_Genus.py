#!/usr/bin/python

import sys
import re
import os
import shutil

"""
March 3, 2014
After running metastats, we pool each comparison together, and filter out some taxa
(1)Pick all of the records with p-values (Only pick L6)
(2)Both cohort groups should have counts (mean value>0, and SD!=mean, which means only one or two samples have counts)

After this, correct p-values together (all useful taxa and all groups)
"""

def get_record (file,subject):
    in_fh=open(file,'r')
    flag=0
    list_list=[]
    for line in in_fh:
        if re.search('mean\(group1\)',line):
            flag=1
            continue
        if flag==0:
            continue
        
        if flag==1 and re.search('\w',line):
            line=line.rstrip('\n')
            list=line.split('\t',)
            #Filter out OTUs only appear in one cohort group, and in one sample
            if (float(list[1])==0 and list[4]==list[6]) or (float(list[4])==0 and list[1]==list[3]):
                continue
            else:
                list_tmp=[]
                list_tmp=[subject,line]
                if list[0] in dict:
                    dict[list[0]].append(list_tmp)
                else:
                    dict[list[0]]=[list_tmp,]
#                list_list.append(list_tmp)

    in_fh.close()
    return


"""
#Main function
"""
if len( sys.argv ) != 3:
        raise Exception( "Usage: metastats_select_all_records_Genus.py <metastats output directory> <output file>")


#Build the output folder
dir=sys.argv[1]
outfile=sys.argv[2]
all_outfh=open(outfile,'w')
all_outfh.write('Group'+'\t'+'Subjects'+'\t'+'mean_group1'+'\t'+'variance_group1'+'\t'+'stderr_group1'+'\t'+'mean_group2'+'\t'+'variance_group2'+'\t'+'stderr_group2'+'\t'+'Pvalue'+'\t'+'Qvalue'+'\n')

#Key:taxaName
#values:(list) all others as one string
dict={}
for file in os.listdir(dir):
    if file.endswith(".metastats") and re.search('L6',file):
        print file
        infile=dir+file
        list_tmp=file.split('\.',)
        subject=list_tmp[0]        
        get_record(infile,subject)


for key,values in dict.items():
    name=key
    name=name.replace(';','.')
    for idx,val in enumerate(values):
        all_outfh.write(values[idx][0]+'\t'+values[idx][1]+'\n')

all_outfh.close()
quit()
