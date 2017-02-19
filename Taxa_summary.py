#!/usr/bin/python

import sys
import os
from subprocess import call
import shutil

"""
Pool OTUs together for the same taxonomy
The taxonomic classification is from mothur pipeline using RDP classification.
(1)Separate into files for different taxonomic level: phylum, class, order, family, genus (L2-L6)
(2)Generate two folders, including releative abundance and read counts.
(3)Run for OTU tables (from BIOM file) before filtering and after filtering.
"""
if len(sys.argv)!=3:
    raise Exception ("Usage of Taxa_summary.py <type of classification:RDP> <output folder>")

type=sys.argv[1]
output_dir=sys.argv[2]
#"../output/Taxa_summary_RDP/"
#"../output/Taxa_summary_pplacer"
work_dir=output_dir+"Taxa_summary_"+type+"/"
if os.path.exists(work_dir):
    shutil.rmtree(work_dir)
os.mkdir(work_dir)

nonefilter_otu=output_dir+"mothur/Mothur_pipeline/mothur_run/0.03Cluster_OTU_taxonomyInfo.txt"
filter_otu=output_dir+"Filter_0.03Cluster_OTU/0.03Cluster_OTU_taxonomyInfo_Filter.txt"
if type=='pplacer':
    nonefilter_otu=output_dir+"TaxaClassification_pplacer/uniqueCluster_OTU_taxonomyInfo.txt"
    filter_otu=output_dir+"TaxaClassification_pplacer/speciesCluster_OTU_taxonomyInfo_Filter.txt"


print "- Make taxonomic table with read counts..."
python_script="./taxa_summary_table_ab.py"
call([python_script,nonefilter_otu,'nonFilter',work_dir])
call([python_script,filter_otu,'Filter',work_dir])


print "- Make taxonomic table with relative abundance..."
python_script="./taxa_summary_table_rel.py"
call([python_script,nonefilter_otu,'nonFilter',work_dir])
call([python_script,filter_otu,'Filter',work_dir])

print "Taxa summary is done!"
quit()
