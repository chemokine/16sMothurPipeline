#!/usr/bin/python
import sys
import re
import os
import shutil

"""
Pool OTUs together for the same taxonomy
(1)Separate into files for different taxonomic level: phylum, class, order, family, genus (L2-L6)
(2)Generate one folder, including releative abundance only
(3)Run for OTU tables (from BIOM file) before filtering and after filtering.
"""

def get_otu(file):
    in_fh=open(file,'r')
    count=0
    for line in in_fh:
        count=count+1
        line=line.rstrip('\n')
        list=line.split('\t',)
        if count==1:
            continue
        if count==2:
            for i,iv in enumerate(list):
                #First column is OTU ID
                #Last column is taxonomic information
                if i==0 or i==len(list)-1:
                    continue

                ll_ReadsSample.append([list[i],0])
            continue


        taxa_id=list[len(list)-1]
        taxa_id=taxa_id.replace(' ','')
        for i,v in enumerate(list):
            if i==0 or i==len(list)-1:
                continue


            #Modify string to integrate for calculation
            list[i]=float(list[i])

            #Sum reads for each sample across all OTUs
            ll_ReadsSample[i-1][1]=ll_ReadsSample[i-1][1]+list[i]
            #Store read counts for each sample in this taxa
            if taxa_id not in dict_otu:
                dict_otu[taxa_id]=[list[i],]
            else:
                #Store all of the samples for this taxa for the first time
                if len(dict_otu[taxa_id])<len(ll_ReadsSample):
                    dict_otu[taxa_id].append(list[i])
                #Another OTU with the same taxa, sum them
                else:
                    dict_otu[taxa_id][i-1]=dict_otu[taxa_id][i-1]+list[i]

    in_fh.close()
    return


def print_rel_abundance(out_dir,tag):
    #Process each taxa level
    for level,value in dict_taxa.items():
        #Output file name
        num=int(dict_taxa[level])+1
        out_file=out_dir+'Taxa_L'+str(num)+'.txt'
        out_fh=open(out_file,'w')

        #Key:Taxa name on this taxa level
        #Values (list):read counts for all samples
        dict={}
        dict.clear()
        for taxa,values in dict_otu.items():
            #Get taxa full name until this specified taxa level
            list=taxa.split(';',)
            count=1
            taxa_level_name=''
            if list[0]=='Bacteria':
                taxa_level_name='Bacteria'
            else:
                taxa_level_name='Archaea'

            while count<=dict_taxa[level]:
                taxa_level_name=taxa_level_name+';'+list[count]
                count=count+1
                
            #Sum reads for this taxa level for each sample
            for i,iv in enumerate(dict_otu[taxa]):
                if taxa_level_name not in dict:
                    dict[taxa_level_name]=[dict_otu[taxa][i],]
                else:
                    if len(dict[taxa_level_name])<len(dict_otu[taxa]):
                        dict[taxa_level_name].append(dict_otu[taxa][i])
                    else:
                        dict[taxa_level_name][i]= dict[taxa_level_name][i]+dict_otu[taxa][i]


        #Print out taxa and read counts
        #Print out titles
        out_fh.write('Taxon')
        for i,v in enumerate(ll_ReadsSample):
            out_fh.write('\t'+ll_ReadsSample[i][0])
        out_fh.write('\n')
        #Print out read counts
        for taxa_level_name in sorted(dict.iterkeys()):
            out_fh.write(taxa_level_name)
            for i,v in enumerate(dict[taxa_level_name]):
                #For absolutive counts
                if tag=='ab':
                    ab_counts=dict[taxa_level_name][i]
                    out_fh.write('\t'+str(ab_counts))
                #For relative abundance
                else:                    
                    rel_value=float(dict[taxa_level_name][i])/float(ll_ReadsSample[i][1])
                    out_fh.write('\t'+str(rel_value))
            out_fh.write('\n')
        
        out_fh.close()

    return

def bin_taxa(name):
    #(2)For taxonomic table with relative abundance
    out_dir=name+'_rel/'
    if os.path.exists(out_dir):
        shutil.rmtree(out_dir)
    os.mkdir(out_dir)
    print_rel_abundance(out_dir,'rel')


    return



"""
Main funtions
"""
if len( sys.argv ) != 4:
        raise Exception( "Usage: taxa_summary_rel.py <nonefilter file full path or filter OTUs full path> <Filter/nonFilter> <work directory>")

otu_infile=sys.argv[1]
tag=sys.argv[2]
#../output/Taxa_summary_RDP/
work_dir=sys.argv[3]

#Bacteria; Bacteroidetes; Bacteroidia; Bacteroidales; Porphyromonadaceae; Barnesiella
dict_taxa={'phylum':1,'class':2,'order':3,'family':4,'genus':5}

#Key:taxonomy 
#Values (list):read counts for each sample
dict_otu={}
#sampleID[i][0],total reads[i][1] 
ll_ReadsSample=[]


#Process filtered OTUs table
if tag=='Filter':
    print "Process filtered OTUs table..."
    get_otu(otu_infile)
    out_dir_name=work_dir+'taxa_summary_Filter'
    bin_taxa(out_dir_name)
else:
    #Process orginal OTUs table 
    if tag=='nonFilter':
        print "Process original OTUs table..."
        get_otu(otu_infile)
        out_dir_name=work_dir+'taxa_summary'
        bin_taxa(out_dir_name)

quit()


