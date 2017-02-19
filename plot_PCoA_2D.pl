#!/usr/bin/perl -w
use strict;

#################
#March 25, 2014
#Input: PCoA table from mothur
#Output: (Middle)selected data for PCoA, R script for plot 2D
#Output: (Final) 2D plot of PCoA from R
########################################
if(!$ARGV[0] or !$ARGV[1] or !$ARGV[2] or !$ARGV[3] or !$ARGV[4] or !$ARGV[5]){
    print "Type parameters as follows:\n";
    print "PCoA table: 0.03Cluster_RepresentSeq4OTUs_Filter.tree1.weighted.phylip.pcoa.axes\n";
    print "Two columns for plot: 1-2\n";
    print "Design file: CLP_WT-KO.design\n";
    print "Two groups for comparison: WT-KO\n";
    print "Plot directory: ./Plot_PCoA/\n";
    print "UniFract type: UniFrac_Weighted\n";
    exit;
}

my $pcoafile=$ARGV[0];
my $pcoaname=$ARGV[5];
my ($pcoa1,$pcoa2)=split(/-/,$ARGV[1]);
my $designfile=$ARGV[2];
my ($g1,$g2)=split(/-/,$ARGV[3]);
my $outdir=$ARGV[4];
#system("mkdir $outdir");

my $outtable=$outdir.$pcoaname.'_PC'.$pcoa1.'-PC'.$pcoa2.'_'.$g1.'-'.$g2.'.txt';
my $outr=$outdir.$pcoaname.'_PC'.$pcoa1.'-PC'.$pcoa2.'_'.$g1.'-'.$g2.'.R';
my $plotfile=$outdir.$pcoaname.'_PC'.$pcoa1.'-PC'.$pcoa2.'_'.$g1.'-'.$g2.'.pdf';
open(TXT,">$outtable") or die "$outtable:$!\n";
print TXT "Group\tSampleID\tPCoA$pcoa1\tPCoA$pcoa2\n";
open(R,">$outr") or die;

#Get group information from design table
#Only keep the samples belongs to $g1 or $g2
#Key:sampleID
#Values:group
my %hash_sample=();
get_sample_info($designfile,\%hash_sample,$g1,$g2);

#Get PCoA information for PCoA $pcoa1, & PCoA $pcoa2
#Key:sampleID
#Values:groupID/pcoa1/pcoa2
my %hash=();
my ($max,$min)=get_PCoA_info($pcoafile,\%hash_sample,$pcoa1,$pcoa2,\%hash);

#Print out the PCoA table
my $num_g1=0;
my $num_g2=0;
foreach my $sid (sort {$hash{$a}[0] cmp $hash{$b}[0]} keys %hash){
    print TXT "$hash{$sid}[0]\t$sid\t$hash{$sid}[1]\t$hash{$sid}[2]\n";
    if($hash{$sid}[0] eq $g1){
	$num_g1++;
    }else{
	$num_g2++;
    }	
}
close(TXT);

#Make R script for plot
print "$max\t$min\t$num_g1\t$num_g2\n";
print R "data<-read.table(\"$outtable\",header=TRUE);\n";
print R "pdf(\"$plotfile\");\n";
#Plot first group
$max=1;
$min=-1;
my $xlab="PCoA".$pcoa1;
my $ylab="PCoA".$pcoa2;
my $mainlab=$g1." vs. ".$g2;
print R "plot(data\$PCoA$pcoa1";
print R "[data\$Group==\"$g1\"],data\$PCoA$pcoa2";
print R "[data\$Group==\"$g1\"],pch=20,col=\"blue\",xlim=c($min,$max),ylim=c($min,$max),xlab=\"$xlab\",ylab=\"$ylab\",main=\"$mainlab\");\n";
#Plot second group
print R "par(new=TRUE);\n";
print R "plot(data\$PCoA$pcoa1";
print R "[data\$Group==\"$g2\"],data\$PCoA$pcoa2";
print R "[data\$Group==\"$g2\"],pch=17,col=\"red\",xlim=c($min,$max),ylim=c($min,$max),xlab=\"\",ylab=\"\");\n";
#Print out legend
my $legend_x=$max-0.5;
my $legend_y=$min+0.3;
#print R "legend($legend_x,$legend_y,c(\"$g1\",\"$g2\"),cex=1.0,col=c(\"blue\",\"red\"),pch=c(20,17),bty=\"n\");\n";
print R "legend($legend_x,$legend_y,c(\"$g1\",\"$g2\"),cex=1.0,col=c(\"blue\",\"red\"),pch=c(20,17));\n";
print R "dev.off();\n";
close(R);
system("R CMD BATCH $outr");
system("rm -rf *.Rout");
print "Done!\n";
exit;

##################
sub get_sample_info{
    my ($file,$H,$g1,$g2)=@_;
    open(FH,"$file") or die;
    while(my $line=<FH>){
	chomp($line);
	my ($sid,$gid)=split(/\t/,$line);
	if($gid eq $g1 or $gid eq $g2){
	    $$H{$sid}=$gid;
	}
    }
    close(FH);
    return;
}


sub get_PCoA_info{
    my ($file,$Hs,$p1,$p2,$H)=@_;
    open(FH,"$file") or die "Can't find the file $file:$!\n";
    my $count=0;
    my $min=10;
    my $max=-1;
    while(my $line=<FH>){
	$count++;
	if($count==1){
	    next;
	}
	chomp($line);
	my @array=split(/\t/,$line);
	#$array[0] is sampleID
	if(exists $$Hs{$array[0]}){
	    if($array[$p1]>=$array[$p2]){
		if($array[$p1]>=$max){
		    $max=$array[$p1];
		}
		if($array[$p2]<=$min){
		    $min=$array[$p2];
		}
	    }else{
		if($array[$p2]>=$max){
		    $max=$array[$p2];
		}
		if($array[$p1]<=$min){
		    $min=$array[$p1];
		}
	    }
#	    print TXT "$$Hs{$array[0]}\t$array[0]\t$array[$p1]\t$array[$p2]\n";
	    $$H{$array[0]}=[$$Hs{$array[0]},$array[$p1],$array[$p2]];
	}
    }
    close(FH);
    return($max,$min);
}
