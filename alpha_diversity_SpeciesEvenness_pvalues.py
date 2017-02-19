#!/usr/bin/python
import sys
import re
import os
import shutil
from subprocess import call
import math

"""
Run statistical testing on species evenness values between groups:
Species evenness values were calculated on Shannon value and observed species, originally from filtered 0.03Cluster OTU table for each sample
(1)Build R script to run Wilcox and T test
(2)Run R script to get p-values
"""


if len(sys.argv)!=5:
    raise Exception ("Useage of alpha_diversity_SpeciesEvenness_pvalues.py <input species evenness value table> <comparison groups list> <R script full path> <ouput pvalue table file>")

infile=sys.argv[1]
listfile=sys.argv[2]
r_script=sys.argv[3]
outfile=sys.argv[4]


outfh=open(r_script,'w')
outfh.write('infile="'+infile+'"'+"\n")
outfh.write('outfile="'+outfile+'"'+"\n")
outfh.write('file.remove("'+outfile+'"'+")\n")
outfh.write('write(paste("Group_x\\tGroup_y\\tMean_x\\tSD_x\\tMean_Y\\tSD_y\\tWilcoxPvalue\\tTtestPvalue"),sep="",file=outfile,append=T)'+"\n")
outfh.write("data<-read.table(infile,header=T)\n")

infh=open(listfile,'r')
count=0
for line in infh:
    count=count+1
    if count>1:
        list=line.split('\t',)
        x_name=list[0]
        y_name=list[1]
        
        outfh.write("x<-data$SpeciesEvenness[data$CohortGroups=='"+x_name+"']\n")
        outfh.write("y<-data$SpeciesEvenness[data$CohortGroups=='"+y_name+"']\n")
        outfh.write("mean_x<-mean(x)\n")
        outfh.write("sd_x<-sd(x)\n")
        outfh.write("mean_y<-mean(y)\n")
        outfh.write("sd_y<-sd(y)\n")
        outfh.write("wt<-wilcox.test(x,y,paired=F,exact=T,correct=T)\n")
        outfh.write("tt<-t.test(x,y,paired=F)\n")
        outfh.write("write(paste('"+x_name+"','\\t','"+y_name+"','\\t',mean_x,'\\t',sd_x,'\\t',mean_y,'\\t',sd_y,'\\t',wt$p.value,'\\t',tt$p.value),sep=\"\",file=outfile,append=T)\n")

infh.close()
outfh.close()

call(["R","CMD","BATCH",r_script])
print "Statistical testing is done!"

quit()
