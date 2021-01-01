#!/usr/bin/perl -w -I/usr/share/perl5/RNA -I/usr/share/perl5
############################################################################
# AUTHOR:  	Stanley NG Kwang Loong, stanley@bii.a-star.edu.sg
# DATE:		31/07/2005
# DESCRIPTION: Generates stats from fasta

#Modified by Nithin C with the help of Amal Thomas to reduce the verbosity
############################################################################
use warnings;
use strict;
use Getopt::Long;
use RNA;

############################################################################
# Global Parameters and initialization if any.
############################################################################

my $inFile="&STDIN";
my $outFile="&STDOUT";
my $gi="NULL";
#Define the monomers and dimers
my %gl_monomers = ('A' => 0,'C' => 0, 'G' => 0, 'U' => 0);
my %gl_dimers = ('AA' => 0, 'AC' => 0, 'AG' => 0, 'AU' => 0,
                 'CA' => 0, 'CC' => 0, 'CG' => 0, 'CU' => 0,
                 'GA' => 0, 'GC' => 0, 'GG' => 0, 'GU' => 0,
                 'UA' => 0, 'UC' => 0, 'UG' => 0, 'UU' => 0);
my $numseqs = 0;
############################################################################
# File IO
# Parse the command line.
############################################################################
Getopt::Long::Configure ('bundling');
GetOptions (
	'i|input_file=s' => \$inFile, 
	'o|output_file=s' => \$outFile
);

if(scalar(@ARGV) == 1 || !defined($inFile) || !defined($outFile)) { 
	die ("USAGE: $0 -i <input file> -o <output file>\n");
}

open (INFILE, "<$inFile") or die( "Cannot open input file $inFile: $!" );
open (OUTFILE, ">$outFile") or die ("Cannot open output file $outFile: $!");

# ID Len A C G U G+C A+U AA AC AG AU CA CC CG CU GA GC GG GU UA UC UG UU %A %C %G %U %G+C %A+U %AA %AC %AG %AU %CA %CC %CG %CU %GA %GC %GG %GU %UA %UC %UG %UU bp %bp mfe Nmfe Q D Subopt_size  
print (OUTFILE "ID\t");
print (OUTFILE "Npb\t");
#print (OUTFILE "mfe\tNmfe\t");
print (OUTFILE "NQ\t");
print (OUTFILE "ND\t");

# Read line by line.
while (my $line = <INFILE>) {

	chomp($line);
	$line =~ s/T/U/g if($line !~ m/^>/);
	
	# Fasta First Line
    if ($line =~ m/^>/) {
	 $gi = $line;
	 }
    
    # Fasta Second Line i.e. RNA sequence
    elsif ($line =~ m/^[AaCcUuGg]/) {	    

		$line=uc($line);
		$numseqs++;

		#remove white space etc
		$line =~ s/[^AaCcUuGg]//g;

		my $seqLen = length($line);
		print(OUTFILE "\n$gi\t");
		
		my ($bp, $mfe, $Q, $D, $SS) = rnaAnalysis($line);
		printf(OUTFILE "%.4f\t", $bp/$seqLen);
		printf(OUTFILE "%.4f\t", $Q/$seqLen);
		printf(OUTFILE "%.4f", $D/$seqLen);

    }
	
    else { }
  
}#end of while loop

print (OUTFILE "\n");
close (INFILE) or die( "Cannot close input file $inFile: $!" );
close (OUTFILE) or die( "Cannot close output file $outFile: $!");
exit;

sub rnaAnalysis {
	my ($seq) = shift;
	my ($seqLen, $struct, $mfe) = (length($seq), RNA::fold($seq)); 
	my $bp = $struct =~ tr/(//; 
	my $Q = 0;
	my $D = 0;
		
	$RNA::pf_scale = exp((-1)*1.2*$mfe/(0.6163207755*$seqLen)) if ($seqLen > 2); 

	# compute partition function and pair pobabilities matrix
	RNA::pf_fold($seq);   				
	# compute sum-of-entropy and bp-distance
	foreach my $j (1..$seqLen-1) {
		foreach my $k ($j+1..$seqLen) {
			my $p = RNA::get_pr($j, $k); # points to the computed pair probabilities
			if ($p > 0) {
				$Q += (-1)*$p*(log($p)/log(2));
				$D += $p*(1 - $p);
			}
		}
	}
	
	return ($bp, $mfe, $Q, $D, 0);
}
