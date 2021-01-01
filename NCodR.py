#!/usr/bin/env python3


author__ = "Sunandan Mukherjee, Nithin C"
version__ = "0.9"
maintainer__ = "Sunandan Mukherjee, Nithin C"
email__ = "sunandan2@gmail.com"

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  


import sys, os
import shutil
import time
import RNA
import argparse

from makeFasta1line import make1line


code2name = {'1000': 'lncRNA', '2000': 'miRNA', '3000':'rRNA', '4000':'snoRNA', '5000': 'tRNA', '6000': 'snRNA', '7000': 'premiRNA'}

###################################################
######## Setting up environmental variables #######
###################################################

ncodr_home = os.getenv("NCODR_HOME")

try:
    bin_dir = ncodr_home+'/bin'
    src_dir = ncodr_home+'/src'
except:
    print("NCODR_HOME is not set, please folow the installation instructions")
    exit(0)

def run_SVM(in_file):
    os.system("thundersvm-predict %s %s %s >/dev/null" %(in_file+'.thunder', ncodr_home+"/model/tsvm.model", in_file+".tsvm"))

def run_RNAfold(in_name, out_name):
    rnafoldout = open(out_name, "w")     # Opens an output file
    in_file = open(in_name).readlines()
    
    md = RNA.md()
    md.dangles = 2 
    md.noLonelyPairs = 1
    
    for i in range(len(in_file)):
        if in_file[i].startswith('>'):
            seq_name = in_file[i].strip()
            seq = in_file[i+1].strip()
            # compute minimum free energy (MFE) and corresponding structure
            fc = RNA.fold_compound(seq, md)
            (ss, mfe) = fc.mfe()
            rnafoldout.write("%s\n%s\n%s (%6.2f)\n" % (seq_name, seq, ss, mfe))
    rnafoldout.close()

def libsvm_formattar(file_name):    
    input_file = file_name
    dataset = open(input_file+'.data').readlines()
    output = open(input_file+'.thunder', 'w')
    for line in dataset:
        if line.startswith("Sequence"):
            pass
        else:
            line = line.rstrip().split('\t')
            tmp = [float(line[i]) for i in range(1, len(line))]
            formated_line = []
            for i in range(len(tmp)):
                temp = '%d:%f' %(i+1, tmp[i])
                formated_line.append(temp)
            output.write('0000 '+' '.join(formated_line)+'\n')
    output.close()
    
def run_findAU(in_file, out_file):
    os.system("%s/calc_AU_MFEI %s %s >/dev/null" %(bin_dir, in_file, out_file))

def cal_repeats(file_path, in_file):
    shutil.copy2(src_dir+"/PrintAllKLengthStrings.java", os.getcwd()+'/')
    os.system("%s/repeats %s >/dev/null" %(bin_dir, in_file+".1l.fa"))
    
def run_genRNAStat(file_path, in_file):
    os.system("%s/genRNAStatsNC.pl -i %s -o %s >/dev/null" %(src_dir, in_file+".1l.fa", in_file+".genstats.tsv"))
    
def run_formattar(file_path, in_file):
    os.system("%s/run_formatter.sh %s >/dev/null" %(ncodr_home, in_file))
    
def run_seq_filter(file_path, in_file):
    os.system("%s/collapse_hash %s %s >/dev/null" %(bin_dir, in_file+".1l.fa", in_file+".colla"))
    
def run_cleaner(file_path, file_name):
    file_exts = [".genstats.tsv", ".1l.fa", ".fold", ".tsv", "_temp1", ".tsvm",
                 "_temp2", "_temp3", ".ids", ".data", "_data.csv", ".thunder"]
    for ext in file_exts:
        os.remove(file_name+ext)
    other_files = ["windowsize1.tsv", "windowsize3.tsv", "windowsize5.tsv",
                   "windowsize2.tsv", "windowsize4.tsv", "windowsize6.tsv",
                   "PrintAllKLengthStrings.class", "PrintAllKLengthStrings.java"]
    for f in other_files:
        os.remove(f)

def main():
    parser = argparse.ArgumentParser(prog='NCodR.py', usage='%(prog)s [options]',
                                    description="NCodR: A multi-class SVM classification \
                                    to distinguish between non-coding RNAs in Viridiplantae")
    parser.add_argument("input", type=str,
                        help="Input file name [RNA sequences in fasta format].")
    parser.add_argument("-r", "--redundant", required=False, action='store_true',
                            help="remove redundant sequence [default = OFF]")
    parser.add_argument("-c", "--clean", required=False, action='store_true',
                            help="clean the intermediate files [default = ON]")
    parser.add_argument("-o", "--output", required=False, type=str,
                            help="Output file name [<input>.pred if not provided]")
                            
    args = parser.parse_args()
    input_file = args.input
    
    file_path = os.path.dirname(input_file)+'/'
    if file_path == '/':
        file_path = os.path.abspath(os.getcwd())+'/'
    file_name = os.path.basename(input_file)
    curr_path = os.getcwd()
    
    if args.output:
        out_file = open(args.output, 'w')
    else:
        out_file = open(file_name+".ncodr", 'w') 
    
    make1line(input_file, file_name+".1l.fa")
    
    if args.redundant:
        run_seq_filter(file_path, file_name)
        os.rename(file_name+".colla", file_name+".1l.fa")
    
    run_RNAfold(file_name+".1l.fa", file_name+".fold")
    run_findAU(file_name+".fold", file_name+".tsv")
    cal_repeats(file_path, file_name)
    run_genRNAStat(file_path, file_name)

    run_formattar(file_path, file_name)
    libsvm_formattar(file_name)

    run_SVM(file_name)
    
    svm_pred = open(file_name+".tsvm").readlines()
    id_list = open(file_name+'.ids').readlines()
    out_file.write('%s\t%s\n' %("Names (ids)", "Predicted class"))
    out_file.write("-"*50)
    out_file.write("\n")
    
    print ('\n\n%s\t%s' %("Names", "Predicted class"))
    print ("-"*50)
    
    for name, svm in zip(id_list, svm_pred):
        print ('%s\t%s\n' %(name.rstrip(), code2name[svm.rstrip()]))
        out_file.write('%s\t%s\n' %(name.rstrip(), code2name[svm.rstrip()]))
    out_file.close()
    
    if not args.clean:
        run_cleaner(file_path, file_name)
    
if __name__ == "__main__":
    main()
