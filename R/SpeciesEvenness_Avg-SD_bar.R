#http://monkeysuncle.stanford.edu/?p=485
error.bar <- function(x, y, upper, lower=upper, length=0.1,...){
    if(length(x) != length(y) | length(y) !=length(lower) | length(lower) != length(upper))
    stop("vectors must be same length")
    arrows(x,y+upper, x, y-lower, angle=90, code=3, length=length, ...)
}


infile="../output/AlphaDiversity/SpeciesEvenness_Avg-SD.txt"
outfile='../output/AlphaDiversity/SpeciesEvenness_Avg-SD.pdf';
pdf(file=outfile,width = 18, height = 8);
row_num=2
y_max=4
x<-read.table(file=infile,header=T)
ee<-matrix(c(x[[3]]),1,row_num,byrow=TRUE)
yy<-matrix(c(x[[2]]),1,row_num,byrow=TRUE)
barx <- barplot(yy, width = 0.5,beside=T,col=NULL, ylim=c(0,y_max), names.arg=x[[1]], axis.lty=1, xlab="", ylab="Shannon Entropy")
error.bar(barx,yy,ee)
dev.off();
