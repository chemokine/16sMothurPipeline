#!/usr/bin/python

import sys
import shutil
import os
from subprocess import call
import re

"""
Run UniFrac for weighted and unweighted
It is based on OTU analysis, so use one sequence of each OTU
Now, we use represent read of each OTU
(1)Get phylogenetic tree of filtered represent reads
(2)Make new count table and Run UniFrac in mothur
(3)Plot PCoA figures of UniFrac of 2D
(4)Use AMOVA to test the differences between two cohort groups
"""
def get_parameter_list(file):
    in_fh=open(file,'r')
    count=0
    for line in in_fh:
        count=count+1
        if count==1:
            continue

        line=line.rstrip('\n')
        list=line.split('\t',)
        list_para.append(list)

    return

def modify_mothur_script(mothur_script,mothur_script_new,output_dir):
    outfh=open(mothur_script_new,'w')
    infh=open(mothur_script,'r')
    for line in infh:
        if re.search("../output/",line):
            line=line.replace("../output/",output_dir)
        outfh.write(line)
    outfh.close()
    infh.close()
    return



"""
#Main function
"""
if len( sys.argv ) != 6:
        raise Exception( "Usage: BetaDiversity_UniFrac.py <FastTree path> <Mothur path> <running reference folder> <input folder> <output folder>")

fasttree=sys.argv[1]
mothur=sys.argv[2]
ref_dir=sys.argv[3]
input_dir=sys.argv[4]
output_dir=sys.argv[5]

filter_dir=output_dir+"Filter_0.03Cluster_OTU/"
otuseq_dir=output_dir+"Pick_0.03Cluster_OTU_seq/Filtered_OTU_seq/"
name="0.03Cluster_OTU_seq_Filter"

design_dir=output_dir+"DesignFiles/"
work_dir=output_dir+"mothur/UniFrac/"
if os.path.exists(work_dir)==False:
	os.mkdir(work_dir)


#(1)Run FastTree
print "Use FastTree to build phylogenetic tree..."
aln_file=otuseq_dir+name+'.fasta'
tree_file=work_dir+name+'.tree'
call([fasttree,'-quiet','-out',tree_file,aln_file])

#(2)Make new count table and Run UniFrac in mothur
print "Make new count table..."
filterOTUs_table=filter_dir+'0.03Cluster_OTU_taxonomyInfo_Filter.txt'
count_table=work_dir+name+'.count_table'
python_script='./otu_seq_CountTable.py'
call([python_script,filterOTUs_table,count_table])

print "Run UniFrac using mothur..."
mothur_script=''
for file in os.listdir('./mothur/'):    
    if re.search('unifrac.mothur',file):
        mothur_script='./mothur/'+file
        mothur_script_new=work_dir+file
        modify_mothur_script(mothur_script,mothur_script_new,output_dir)
call([mothur,mothur_script_new])
for file in os.listdir('./'):
    if file.endswith(".logfile"):
        shutil.move(file,work_dir)


#(3)Plot 2D PCoA of UniFrac
print "Plot UniFrac PCoA with 2D..."
#Build directory
plot_dir=work_dir+'Plot_PCoA/'
if os.path.exists(plot_dir):
    shutil.rmtree(plot_dir)
os.mkdir(plot_dir)

#Parameters for group pair
listfile=work_dir+"UniFrac_ParametersList.txt"
shutil.copy(input_dir+'CohortGroups_ParametersList.txt',listfile)
#group1[i][0],group2[i][1],designfile[i][2]
list_para=[]
get_parameter_list(listfile)

#Plot figure for each matrix
script='./plot_PCoA_2D.pl'
for file in os.listdir(work_dir):
    if file.endswith(".axes"):
        infile=work_dir+file
        level='1-2'
        for i,v in enumerate(list_para):
            designfile=design_dir+list_para[i][2]
            groups=list_para[i][0]+'-'+list_para[i][1]
            type=''
            if re.search("unweighted",file):
                type='UniFrac_Unweighted'
            else:
                type='UniFrac_Weighted'

            call([script,infile,level,designfile,groups,plot_dir,type])
        

#(4)Use AMOVA to test the differences between two cohort groups
print "Use AMOVA to test the differences between two cohort groups..."
mothur_script=work_dir+'amova.mothur'
outfh=open(mothur_script,'w')
outfh.write("set.dir(output="+output_dir+"mothur/UniFrac)\n")
outfh.write("set.dir(input="+output_dir+"mothur/UniFrac)\n")
for i,iv in enumerate(list_para):
    group1=list_para[i][0]
    group2=list_para[i][1]
    designfile=design_dir+list_para[i][2]
    #amova(phylip=0.03Cluster_RepresentSeq4OTUs_Filter.tree1.weighted.phylip.dist,design=CohortGroups.design,sets=Control-FoodAllergy)
    outfh.write("amova(phylip="+name+".tree1.weighted.phylip.dist,design="+designfile+",sets="+group1+'-'+group2+")\n")
    outfh.write("amova(phylip="+name+".tree1.unweighted.phylip.dist,design="+designfile+",sets="+group1+'-'+group2+")\n")
outfh.close()
call([mothur,mothur_script])

for file in os.listdir('./'):
    if file.endswith(".logfile"):
        shutil.move(file,work_dir+'amova_mothur_results.txt')


quit()
