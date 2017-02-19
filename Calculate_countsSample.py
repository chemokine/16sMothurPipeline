#!/usr/bin/python

import os
from subprocess import call
import shutil
import sys

"""
(1)Run count_group.py three times for different steps from mothur
"""
if len(sys.argv)!=2:
    raise Exception ("Usage: Calculate_countsSample.py <output folder>")

output_dir=sys.argv[1]
mothur_run_dir=output_dir+'mothur/Mothur_pipeline/mothur_run/'
work_dir=output_dir+'Calculate_countsSample/'
if os.path.exists(work_dir):
    shutil.rmtree(work_dir)
os.mkdir(work_dir)

python_script="./count_group.py"

#reads/sample after trim.seqs
print "- Calculate samples after trimming..."
name='stability.trim.contigs.good.count_table'
infile=mothur_run_dir+name
outfile=work_dir+name+'_ReadCount.txt'
call([python_script,infile,outfile])

#reads/sample after filter.seqs
print "- Calculate samples after alignment and filtering..."
name='stability.trim.contigs.good.unique.good.filter.count_table'
infile=mothur_run_dir+name
outfile=work_dir+name+'_ReadCount.txt'
call([python_script,infile,outfile])


#reads/sample after chimera checking
print "- Calculate samples after chimera checking..."
name='stability.trim.contigs.good.unique.good.filter.unique.precluster.uchime.pick.count_table'
infile=mothur_run_dir+name
outfile=work_dir+name+'_ReadCount.txt'
call([python_script,infile,outfile])

print "Calculation is done!"
quit()
