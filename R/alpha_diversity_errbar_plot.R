library(gtools,lib.loc="/data/cctm/apps/R_Home/");
library(gdata,lib.loc="/data/cctm/apps/R_Home/");
library(gplots,lib.loc="/data/cctm/apps/R_Home/");


file_list<-read.table("../output/AlphaDiversity/AlphaDiversity_plotList.txt", colClasses="character");
inputlist<-file_list[[1]];
outputlist<-file_list[[2]];
mainlist<-file_list[[3]];
ylablist<-file_list[[4]];
xlist<-as.numeric(file_list[[5]]);
ylist<-as.numeric(file_list[[6]]);
glist1<-file_list[[7]];
glist2<-file_list[[8]];
for(i in 1:length(inputlist)){
      infile<-inputlist[i];
      print(infile);
      #Load data from Mac
      data<-read.table(infile,header=TRUE);

      #data[[1]] is reads number
      #data[[2]] and data[[5]] are mean value
      #data[[3]] and data[[6]] are SD value
      #data[[4]] and data[[7]] are Err value
      outfile<-outputlist[i];
      pdf(file=outfile);
	  plotCI(x=data[[1]],y=data[[2]],uiw=data[[3]],pch=".:",col="blue",lty=1,type="l",gap=0,xlab="#seq/sample",ylab=ylablist[i],main=mainlist[i],ylim=c(0,ylist[i]),xlim=c(0,xlist[i]),cex.lab=1.5,cex.axis=1.5,cex.main=1.5,cex.sub=1.5);
      
      plotCI(x=data[[1]],y=data[[5]],uiw=data[[6]],pch=".:",col="red",lty=1,type="l",gap=0,add=TRUE);
      
      xsite=0.6*xlist[i]
      ysite=0.1*ylist[i]
	  legend(xsite,ysite, c(glist1[i],glist2[i]), cex=1.2, col=c("blue","red"), pch=c(20,20), lty=1:1,bty="n");
      dev.off();
}