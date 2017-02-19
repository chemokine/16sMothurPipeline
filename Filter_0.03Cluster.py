#!/usr/bin/python

import sys
import shutil
import os
from subprocess import call


"""
Filter out low abundant OTUs
avg_rel_group=(sum of rel in this group)/number of samples in this group
detectable_rel_avg=1/(average number of read of all samples)
At least in one group avg_rel_group>=detectable_rel_avg
"""
if len(sys.argv)!=2:
    raise Exception ("Usage: Filter_0.03Cluster.py <output folder>")

output_dir=sys.argv[1]
mothur_pipeline=output_dir+"mothur/Mothur_pipeline/mothur_run/"
work_dir=output_dir+"Filter_0.03Cluster_OTU/"
design=output_dir+'DesignFiles/CohortGroups.design'

if os.path.exists(work_dir):
    shutil.rmtree(work_dir)
os.mkdir(work_dir)

print "- Filter OTUs table with taxonomic information..."
name="0.03Cluster_OTU_taxonomyInfo"
otu_infile=mothur_pipeline+name+'.txt'
otu_outfile=work_dir+name+'_Filter.txt'
python_script="./filter_0.03Cluster_TaxaTable.py"
call([python_script,otu_infile,otu_outfile,design])

print "- Filter OTUs table from Shared file..."
python_script="./filter_0.03Cluster_SharedTable.py"
taxa_otu_infile=work_dir+name+'_Filter.txt'
shared_infile=mothur_pipeline+"stability.trim.contigs.good.unique.good.filter.unique.precluster.pick.pick.an.unique_list.shared"
shared_outfile=work_dir+"0.03Cluster_OTU_Filter.shared"
call([python_script,taxa_otu_infile,shared_infile,shared_outfile])

print "Filter is done!"
quit()
