#!/usr/bin/python

import sys
import os
from subprocess import call
import shutil

"""
(1)Pick one read to represent one OTU. 
Rule: the read is the most abundant unique read of this OTU (represent sequence of OTU)
(2)Filter low abundant OTUs, cutoff:
avg_rel_group=(sum of rel in this group)/number of samples in this group
detectable_rel_avg=1/(average number of read of all samples)
At least in one group avg_rel_group>=detectable_rel_avg
Basically, use the filtered OTUs_Filter.shared table
"""
if len(sys.argv)!=2:
    raise Exception ("Usage: Pick_0.03Cluster_OTU_seq.py <output folder>")

output_dir=sys.argv[1]
mothur_pipeline=output_dir+"mothur/Mothur_pipeline/mothur_run/"
filter_otus_dir=output_dir+"Filter_0.03Cluster_OTU/"
work_dir=output_dir+"Pick_0.03Cluster_OTU_seq/"
if os.path.exists(work_dir):
#    shutil.rmtree(work_dir)
    print work_dir
else:
    os.mkdir(work_dir)

#(1)Pick represent sequence for each OTU, consider the most abundant unique read
print "Pick represent sequence for each OTU, consider the most abundant unique read..."
python_script="./pick_0.03Cluster_OTU_seq_id.py"
call([python_script,mothur_pipeline,work_dir])


#(2)Filter low abundant OTUs
print "Filter low abundant OTUs..."
#Use the same criteria as Filter_OTUs
work_dir_tmp=work_dir
work_dir=work_dir+'Filtered_OTU_seq/'
if os.path.exists(work_dir):
    shutil.rmtree(work_dir)
os.mkdir(work_dir)
python_script="./pick_0.03Cluster_OTU_seq_filter.py"
mothur_shared=filter_otus_dir+"0.03Cluster_OTU_Filter.shared"
call([python_script,mothur_shared,work_dir_tmp,work_dir])


print "Represented sequences are picked for each OTU!"
quit()
