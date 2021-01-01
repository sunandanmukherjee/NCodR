#!/usr/bin/python3

author__ = "Sunandan Mukherjee"
email__ = "sunandan2@gmail.com"
'''
Name
====
    makeFasta1line.py
    
Description
===========
    Convert multiline fasta format to one line fasta.
    
    E.g 
    >sample protein
    ADFPPALLFPPGNSLFKKALWALCITRH
    KLLADDESCPAM
    
    to
    
    >sample protein
    ADFPPALLFPPGNSLFKKALWALCITRHKLLADDESCPAM
    
Dependencies
============
    python version 3.0 or above
    
'''

import sys

def make1line(in_name, out_name):

    with open(in_name) as f_input, open(out_name, 'w') as f_output:
        block = []

        for line in f_input:
            if line.startswith('>'):
                if block:
                    f_output.write(''.join(block) + '\n')
                    block = []
                f_output.write(line)
            else:
                block.append(line.strip())

        if block:
            f_output.write(''.join(block) + '\n')
    
    f_input.close()
    f_output.close()

def main():
    infile = sys.argv[1]
    outfile = sys.argv[2]
    make1line(infile, outfile)
    
if __name__ == "__main__":
    main()
