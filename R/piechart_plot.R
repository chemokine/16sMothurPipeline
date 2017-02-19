infile="../output/PieChart_taxa/Taxa_L2.txt"
outfile="../output/PieChart_taxa/Draw_PieChart/Taxa_L2_piechar"


data<-read.table(infile,header=TRUE) 
taxa<-data$FullTaxa
titles<-names(data)
for(i in 3:length(titles)){
	group_id<-titles[[i]]
	rel_values<-data[i][[1]]

	#Calculate percentage for each taxon
	pct<-round(rel_values/sum(rel_values)*100)
	# ad % to labels
	tmp_taxa<-paste(taxa,pct)
	tmp_taxa<-paste(tmp_taxa,"%",sep="")

	#Draw pie chart
	tmp_outfile=paste(outfile,group_id,sep="_")
	tmp_outfile1=paste(tmp_outfile,'_legend.pdf',sep="")
	pdf(tmp_outfile1);
	plot.new()
	legend("bottom", cex=0.8,legend = tmp_taxa, fill=rainbow(length(taxa)), bty="n")
	dev.off()
	
	tmp_outfile2=paste(tmp_outfile,'.pdf',sep="")
	pdf(tmp_outfile2);
	#pie(rel_values,labels=tmp_taxa,col=rainbow(length(taxa)),main="Pie Chart of relative abundance")
	pie(rel_values,labels="", col=rainbow(length(taxa)),clockwise=TRUE)
	dev.off()
}

infile="../output/PieChart_taxa/Taxa_L3.txt"
outfile="../output/PieChart_taxa/Draw_PieChart/Taxa_L3_piechar"


data<-read.table(infile,header=TRUE) 
taxa<-data$FullTaxa
titles<-names(data)
for(i in 3:length(titles)){
	group_id<-titles[[i]]
	rel_values<-data[i][[1]]

	#Calculate percentage for each taxon
	pct<-round(rel_values/sum(rel_values)*100)
	# ad % to labels
	tmp_taxa<-paste(taxa,pct)
	tmp_taxa<-paste(tmp_taxa,"%",sep="")

	#Draw pie chart
	tmp_outfile=paste(outfile,group_id,sep="_")
	tmp_outfile1=paste(tmp_outfile,'_legend.pdf',sep="")
	pdf(tmp_outfile1);
	plot.new()
	legend("bottom", cex=0.5,legend = tmp_taxa, fill=rainbow(length(taxa)), bty="n")
	dev.off()
	
	tmp_outfile2=paste(tmp_outfile,'.pdf',sep="")
	pdf(tmp_outfile2);
	#pie(rel_values,labels=tmp_taxa,col=rainbow(length(taxa)),main="Pie Chart of relative abundance")
	pie(rel_values,labels="", col=rainbow(length(taxa)),clockwise=TRUE)
	dev.off()
}


infile="../output/PieChart_taxa/Taxa_L4.txt"
outfile="../output/PieChart_taxa/Draw_PieChart/Taxa_L4_piechar"


data<-read.table(infile,header=TRUE) 
taxa<-data$FullTaxa
titles<-names(data)
for(i in 3:length(titles)){
	group_id<-titles[[i]]
	rel_values<-data[i][[1]]

	#Calculate percentage for each taxon
	pct<-round(rel_values/sum(rel_values)*100)
	# ad % to labels
	tmp_taxa<-paste(taxa,pct)
	tmp_taxa<-paste(tmp_taxa,"%",sep="")

	#Draw pie chart
	tmp_outfile=paste(outfile,group_id,sep="_")
	tmp_outfile1=paste(tmp_outfile,'_legend.pdf',sep="")
	pdf(tmp_outfile1);
	plot.new()
	legend("bottom", cex=0.5,legend = tmp_taxa, fill=rainbow(length(taxa)), bty="n")
	dev.off()
	
	tmp_outfile2=paste(tmp_outfile,'.pdf',sep="")
	pdf(tmp_outfile2);
	#pie(rel_values,labels=tmp_taxa,col=rainbow(length(taxa)),main="Pie Chart of relative abundance")
	pie(rel_values,labels="", col=rainbow(length(taxa)),clockwise=TRUE)
	dev.off()
}


infile="../output/PieChart_taxa/Taxa_L5.txt"
outfile="../output/PieChart_taxa/Draw_PieChart/Taxa_L5_piechar"


data<-read.table(infile,header=TRUE) 
taxa<-data$FullTaxa
titles<-names(data)
for(i in 3:length(titles)){
	group_id<-titles[[i]]
	rel_values<-data[i][[1]]

	#Calculate percentage for each taxon
	pct<-round(rel_values/sum(rel_values)*100)
	# ad % to labels
	tmp_taxa<-paste(taxa,pct)
	tmp_taxa<-paste(tmp_taxa,"%",sep="")

	#Draw pie chart
	tmp_outfile=paste(outfile,group_id,sep="_")
	tmp_outfile1=paste(tmp_outfile,'_legend.pdf',sep="")
	pdf(tmp_outfile1);
	plot.new()
	legend("bottom", cex=0.5,legend = tmp_taxa, fill=rainbow(length(taxa)), bty="n")
	dev.off()
	
	tmp_outfile2=paste(tmp_outfile,'.pdf',sep="")
	pdf(tmp_outfile2);
	#pie(rel_values,labels=tmp_taxa,col=rainbow(length(taxa)),main="Pie Chart of relative abundance")
	pie(rel_values,labels="", col=rainbow(length(taxa)),clockwise=TRUE)
	dev.off()
}

infile="../output/PieChart_taxa/Taxa_L6.txt"
outfile="../output/PieChart_taxa/Draw_PieChart/Taxa_L6_piechar"


data<-read.table(infile,header=TRUE) 
taxa<-data$FullTaxa
titles<-names(data)
for(i in 3:length(titles)){
	group_id<-titles[[i]]
	rel_values<-data[i][[1]]

	#Calculate percentage for each taxon
	pct<-round(rel_values/sum(rel_values)*100)
	# ad % to labels
	tmp_taxa<-paste(taxa,pct)
	tmp_taxa<-paste(tmp_taxa,"%",sep="")

	#Draw pie chart
	tmp_outfile=paste(outfile,group_id,sep="_")
	tmp_outfile1=paste(tmp_outfile,'_legend.pdf',sep="")
	pdf(tmp_outfile1);
	plot.new()
	legend("bottom", cex=0.5,legend = tmp_taxa, fill=rainbow(length(taxa)), bty="n")
	dev.off()
	
	tmp_outfile2=paste(tmp_outfile,'.pdf',sep="")
	pdf(tmp_outfile2);
	#pie(rel_values,labels=tmp_taxa,col=rainbow(length(taxa)),main="Pie Chart of relative abundance")
	pie(rel_values,labels="", col=rainbow(length(taxa)),clockwise=TRUE)
	dev.off()
}
