outfile='../output/mothur/Metastats_Taxa/metastats_out/metastats_Genus_Filter_FDR_BH.txt'
file.remove(outfile)
infile="../output/mothur/Metastats_Taxa/metastats_out/metastats_Genus_Filter.txt"
write(paste('Groups\tTaxa\tFDR\tMeanGroup1\tVarianceGroup1\tStderrGroup1\tMeanGroup2\tVarianceGroup2\tStderrGroups',sep=''),file=outfile,append=TRUE);

data<-read.table(infile,header=TRUE);
new_Pvalues<-data$Pvalue;
new_groups<-data$Group;
      
group1_mean<-data$mean_group1
group1_var<-data$variance_group1
group1_std<-data$stderr_group1
group2_mean<-data$mean_group2
group2_var<-data$variance_group2
group2_std<-data$stderr_group2
      
new_subjects<-data$Subjects;
q_values<-p.adjust(new_Pvalues,method="BH");

for(j in 1:length(new_groups)){
      write(paste(new_groups[[j]],'\t',new_subjects[[j]],'\t',q_values[[j]],'\t',group1_mean[[j]],'\t',group1_var[[j]],'\t',group1_std[[j]],'\t',group2_mean[[j]],'\t',group2_var[[j]],'\t',group2_std[[j]], sep=''),file=outfile,append=TRUE);
}




