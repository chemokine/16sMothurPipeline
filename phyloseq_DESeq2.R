#Load BIOM table and Mapping information
library("phyloseq")
library("DESeq2")
packageVersion("phyloseq")
packageVersion("DESeq2")


#prepare files
#biom_infile="Taxa.biom"
#map_infile="CohortGroups_map.txt"
#outfile="DESeq2_nbinomWaldTest_pAdjust-BH.txt"
para_infile="/data/cctm/16S_rRNA/T0421_Chatila_Azza_Allergy.2017/2017.2.15.combineTwoRuns.RemoveFailedInTheFirstRun/Analysis/output/Phyloseq_DESeq2/Phyloseq_DESeq2_input_list.txt"
file_list<-read.table(para_infile, colClasses="character")
biom_list<-file_list[[1]]
map_list<-file_list[[2]]
outfile_list<-file_list[[3]]
for(j in 1:length(biom_list)){
	biom_infile<-biom_list[j]
	map_infile<-map_list[j]
	outfile<-outfile_list[j]
#	file.remove(outfile)
	write(paste('CohortGroups\tTaxaName\tbaseMean\tlog2FoldChange\tlfcSE\tstat\tpvalue\tpadjust_BH_FDR',sep = ""),file=outfile,append=TRUE)

	#Load taxa or OTU count table
	biom_tax <- import_biom(biom_infile)
	map <- import_qiime_sample_data(map_infile)
	#Merg information together
	mat_data <- merge_phyloseq(biom_tax, map)

	#http://joey711.github.io/phyloseq-extensions/DESeq2.html
	#Convert phyloseq format to DESeq2 format
	diagdds = phyloseq_to_deseq2(mat_data, ~ Description)
	diagdds = DESeq(diagdds, test="Wald", fitType="parametric")
#	res = results(diagdds, cooksCutoff = FALSE)
	groupNames = levels(map$Description)
	numeratorGroup = groupNames[grep("case",groupNames)]
	DenominatorGroupToCompareAgainst = groupNames[grep("control",groupNames)]

	res = results(diagdds, cooksCutoff = FALSE, contrast=c("Description",))
	print (res)
	rnames<-rownames(diagdds)
	for (i in 1:length(res$basemean)){
		write(paste(resultsNames(diagdds)[2],'|',resultsNames(diagdds)[3],'\t',rnames[i],'\t',res$baseMean[i],'\t',res$log2FoldChange[i],'\t',res$lfcSE[i],'\t',res$stat[i],'\t',res$pvalue[i],'\t',res$padj[i],sep=""),file=outfile,append=TRUE)
	}
}
quit()
