# Calculation of features

## Dependencies
1. g++ compiler with C+11 support
2. javac compiler 

## Third-party tools
1. RNAfold (https://github.com/ViennaRNA/ViennaRNA/)
2. fasta1line.pl (https://github.com/naturalis/mixed-reads-assembly-Erycina/blob/master/src/Fasta1line.pl)
3. genRNAStats.pl (https://web.bii.a-star.edu.sg/~stanley/Suppl_material4/genRNAStats.pl)

The different features can be calculated by running the programs available in this directory
The programs can be compiled by running make in this folder

```bash
make
```
## Calculation of AU and MFEI values

For a fasta file named fastafile.fa the first step is to convert it to single line format using fasta1line.pl. The RNAfold program is run to generate the secondary structure file in dot-bracket format (.b). 
```
fasta1line.pl fastafile.fa fastafile_1l.fa
RNAfold -d2 --noLP --noPS <fastafile_1l.fa >fastafile_1l.b
calc_AU_MFEI fastafile_1l.b
```

## Calculation of Npb,NQ and ND values

The genRNAStats.pl can be used for calculation of these parameters.

## Calculation of SSR

The number of repeats for SSR can be calculated using the repeats program in this directory.

```
repeats fastafile_1l.fa
```
