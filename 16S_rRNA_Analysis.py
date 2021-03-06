#!/usr/bin/python

import os
import re
import sys
import shutil
from subprocess import call
from subprocess import check_call
import datetime
from time import gmtime, strftime


def get_parameters(file):
    in_fh=open(file,'r')
    mothur_path=''
    processors=''
    fasttree_path=''
    for line in in_fh:
        line=line.rstrip('\n')
        if re.match('mothur_path=',line):
            mothur_path=line.replace('mothur_path=','')
            continue
        if re.match('processors=',line):
            processors=line.replace('processors=','')
            continue
        if re.match('FastTree=',line):
            fasttree_path=line.replace('FastTree=','')
            continue
 
    in_fh.close()
    return(mothur_path,processors,fasttree_path)


"""
Main function
"""
if len(sys.argv)!=5:
    print "Useage of 16S_rRNA_Analysis.py\n -fq Full path of fastq folder\n -a full path of analysis to hold input and output folder\nExample:\npython 16S_rRNA_Analysis.py -fq /data/cctm/fastq -a /data/cctm/nl/analysis\n"
    quit()

raw_reads_path=''
analysis_dir=''
if sys.argv[1]=='-fq':
    raw_reads_path=sys.argv[2]+'/'
if sys.argv[3]=='-a':
    analysis_dir=sys.argv[4]+'/'
if raw_reads_path=='' or analysis_dir=='':
    print "Please double check the parameters for running this package!\n"
    quit()


#Make a copy of configuration file
configuration_file='../16S_rRNA_Analysis_Configuration.txt'
shutil.copy(configuration_file,analysis_dir)
ref_dir="../ref/"

#Setup folders for the new run
input=analysis_dir+'input/'
output=analysis_dir+'output/'
mothur_dir=output+'mothur/'
design_dir=output+'DesignFiles/'


if os.path.exists(output)==False:
    os.mkdir(output)
if os.path.exists(mothur_dir)==False:
    os.mkdir(mothur_dir)
if os.path.exists(design_dir)==False:
    os.mkdir(design_dir)


#Get Design file
print "Get user's desgin file..."
flag_design_file=0
for file in os.listdir(input):
    if file.endswith(".design"):
        flag_design_file=1
        design_file=input+file
        shutil.copy(design_file,design_dir)
        break
if flag_design_file==0:
    raise Exception("Couldn't find user's design file. Please check ./input/ folder and Documentation to make sure design file is correct.")


#Get all of the paths
print "\n\nExtract parameters from file to run analysis pipeline..."
(mothur_path,processors,fasttree_path)=get_parameters(configuration_file)
if mothur_path=='' or processors=='' or fasttree_path=='':
    raise Exception("Parameters from file '16S_rRNA_Analysis_Configuration.txt' are incorrect. Please check parameter file or Documentaion!")




#Run mothur
print "\n\nRun raw reads through mothur..."
python_script="./Preprocessing_MiSeq.py"
call([python_script,processors,mothur_path,raw_reads_path,ref_dir,input,output])


#Convert BIOM file to text file with taxonomic information using BIOM
mothur_run=mothur_dir+'Mothur_pipeline/mothur_run/'
#BIOM 1.0
##command="convert_biom.py -i "+mothur_run+"stability.trim.contigs.good.unique.good.filter.unique.precluster.pick.pick.an.unique_list.0.03.biom -o "+mothur_run+"0.03Cluster_OTU_taxonomyInfo.txt -b --header_key=taxonomy"
#BIOM2.1
command="biom convert -i "+mothur_run+"stability.trim.contigs.good.unique.good.filter.unique.precluster.pick.pick.an.unique_list.0.03.biom -o "+mothur_run+"0.03Cluster_OTU_taxonomyInfo.txt --to-tsv --header-key=taxonomy"
os.system(command)


"""
#Use mothur's output to do statistical tests or visualization
"""
print "==========================="
print "Analysis and Visualization"
print "==========================="

############################
#Use all of OTUs from mothur
############################
#Calculate counts per sample
#Use original files from mothur_run
print "\n\nCalculate counts per sample..."
print strftime("%Y-%m-%d %H:%M:%S", gmtime())
python_script="./Calculate_countsSample.py"
call([python_script,output])


#Filter low abundant OTUs
print "\nFilter low abundant OTUs..."
print strftime("%Y-%m-%d %H:%M:%S", gmtime())
python_script="./Filter_0.03Cluster.py"
call([python_script,output])


#Pick represent sequence for each OTU
#Use the Filter_OTUs results
print "\nPick represent sequence for each OTU..."
print strftime("%Y-%m-%d %H:%M:%S", gmtime())
python_script="./Pick_0.03Cluster_OTU_seq.py"
call([python_script,output])


#####################################################
#Operate on 0.03Cluster_OTUs, and filtered OTUs table
#####################################################
#Alpha diversity
#Use Filter_OTUs shared table
print "\n\nAlpha diversity..."
print strftime("%Y-%m-%d %H:%M:%S", gmtime())
python_script="./AlphaDiversity_Shannon.py"
call([python_script,input,output])


#Calculate Beta diversity
#Use Filter_OTUs results
#Calculate UniFrac as beta diversity
print "\nRun Beta diversity of UniFrac and plot 2D PCoA..."
print strftime("%Y-%m-%d %H:%M:%S", gmtime())
python_script="./BetaDiversity_UniFrac.py"
call([python_script,fasttree_path,mothur_path,ref_dir,input,output])


#Calculate Bray-curtis as beta diversity
print "\nRun Beta diversity of Bray-curtis and plot 2D PCoA..."
print strftime("%Y-%m-%d %H:%M:%S", gmtime())
python_script="./BetaDiversity_BrayCurtis.py"
call([python_script,mothur_path,ref_dir,input,output])


#Convert OTUs to taxonomic table
#Use filtered results and none filtered
print "\nConvert OTUs table to taxonomic table using RDP classification..."
print strftime("%Y-%m-%d %H:%M:%S", gmtime())
python_script="./Taxa_summary.py"
call([python_script,'RDP',output])

############################################             
#Operate on RDP_summary_taxa results
############################################           
#Draw pie char of relative abundance of taxa in each treatment group
#Use filtered results
print "\nDraw Pie Chart of realative abundance of taxa..."
print strftime("%Y-%m-%d %H:%M:%S", gmtime())
taxa_method='RDP'
python_script="./PieChart_taxa.py"
call([python_script,taxa_method,output])

#Draw bar char of relative abundance with SD of taxa in each treatment group
#Use filtered results
print "\nDraw Bar Chart of realative abundance with SD of taxa..."
print strftime("%Y-%m-%d %H:%M:%S", gmtime())
python_script="./BarChart_taxa.py"
call([python_script,taxa_method,output])

#Statistic test of taxonomic table using DESeq2 wrapped by phyloseq
#Use filtered results
print "Run phyloseq wrapped with DESeq2 to compute negative binormial for feature selection..."
print strftime("%Y-%m-%d %H:%M:%S", gmtime())
python_script="./Phyloseq_DESeq2.py"
call([python_script,taxa_method,input,output])


#Statistic test of taxonomic table using Metastats
#Use filtered results
print "Statistic test on genus level using Metastats, and q-values will be calculated on genus level..."
print strftime("%Y-%m-%d %H:%M:%S", gmtime())
python_script="./Metastats_adjustP-value_Taxa.py"
call([python_script,mothur_path,taxa_method,input,output])


#Clean up
command="rm -rf *.R *.Rout"
os.system(command)
full_mothur_dir=output+'mothur/Mothur_pipeline/mothur_run/'
command="gzip "+full_mothur_dir+'*.align '+full_mothur_dir+'*.fasta '+full_mothur_dir+'*.qual'
os.system(command)
print "All analysis run is done!\n"

quit()
