#!/usr/bin/python
import sys
import os
import re
import os.path

"""
(1)Copy the raw reads file of each sample to specified folder
(2)Unzip those file
"""

if len(sys.argv)!=3:
    raise Exception ("Usage of pre_cp_unzip_fastq.py <Path of downloaded ziped fastq files from DanaFarber> <Output path of unzipped fastq files>")

in_dir=sys.argv[1]
out_dir=sys.argv[2]


#Process each sample
for each in os.listdir(in_dir):
    #If the samples are .fastq.gz files in one folder
    if each.endswith('.fastq.gz'):
        print each
        fq_infile=in_dir+each
        fq_outfile=out_dir+each
        fq_unzip_outfile=fq_outfile.replace('.gz','')

        #Copy the file to folder
        command='cp '+fq_infile+' '+fq_outfile
        os.system(command)
        #Unzip the file
        if os.path.isfile(fq_unzip_outfile):
            os.remove(fq_unzip_outfile)
        command="gunzip "+fq_outfile
        os.system(command)
    else:
        #IF the samples are in each folder with R1&R2
        if each=='.DS_Store':
            continue
        full_path=in_dir+each+'/'
        for file in os.listdir(full_path):
            if re.search('.fastq.gz',file):
                print file
                fq_infile=full_path+file
                fq_outfile=out_dir+file
                fq_unzip_outfile=fq_outfile.replace('.gz','')
                
                #Copy the file to folder 
                command='cp '+fq_infile+' '+fq_outfile
                os.system(command)
                #Unzip the file 
                if os.path.isfile(fq_unzip_outfile):
                    os.remove(fq_unzip_outfile)
                command="gunzip "+fq_outfile
                os.system(command)

print "Unzip all of the fastq files..."
quit()

