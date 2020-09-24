#!/usr/bin/env python

import sys, os
import argparse


#Class annotation with integers
#abvr = {'L':'lncRNA', 'M':'miRNA', 'R':'rRNA', 'SNO':'snoRNA', 'T':'tRNA', 'SN':'snRNA', 'P':'premiRNA'}
abvr = {'L':1000, 'M':2000, 'R':3000, 'SNO':4000, 'T':5000, 'SN':6000, 'P':7000}

def main():
    parser = argparse.ArgumentParser(description='Convert the dataset to libsvm compatible dataset format.',
                                     prog='libsvm_dataset_formating.py', 
                                     usage='%(prog)s [options]')
    parser.add_argument("-i", "--input", required=True, dest="input_file", type=str,
                        help="Input file name [required].")
    args = parser.parse_args()
    input_file = args.input_file

    #checking the input file
    if input_file != "":
        if(os.path.isfile(input_file) == False): #checking input_file
            print ("Error: input location/file: "+input_file+" provided by the user doesn't exist", file=sys.stderr)
            sys.exit(1)
            
    dataset = open(input_file).readlines()
    for line in dataset:
        if line.startswith("Sequence"):
            pass
        else:
            line = line.rstrip().split('\t')
            tmp = [float(line[i]) for i in range(1, len(line)-1)]
            formated_line = []
            for i in range(len(tmp)):
                temp = '%d:%f' %(i+1, tmp[i])
                formated_line.append(temp)
            print (abvr[line[-1]], ' '.join(formated_line), sep=' ')
        
if __name__ == "__main__":
    main()
