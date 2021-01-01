# NCodR
Prediction model for non-coding RNA using Support Vector Machine (SVM)

## Dependencies
1. Python 3
2. g++  (with  C++ Standard Template Library C++20)
3. Java 
4. Perl
5. Argparse (python library)


## Third-party tools
1. ThunderSVM (https://github.com/Xtra-Computing/thundersvm)

2. RNAfold (https://github.com/ViennaRNA/ViennaRNA/)
        For installation, please refer to https://github.com/ViennaRNA/ViennaRNA/#installation
        ```NCodR``` calls ViennaRNA as a python library. Therefore, after installation of ViennaRNA it is
        important to make sure that ```RNA``` module is included in the ```PYTHONPATH```.
        Generally ```RNA``` directory is located at ```/usr/local/lib/python3.8/site-packages/```.
        In that case, please include the following path in ```.bashrc``` (or in ```.bash_profile```)
        
3. genRNAStats.pl (https://web.bii.a-star.edu.sg/~stanley/Suppl_material4/genRNAStats.pl)
        ```genRNAStats.pl``` is modified (to reduce the verbosity) and provided with the package.
        Therefore, it is not necessary to download the original souce code.


## Installation
1. Download or clone the NCodR from the gitlab repository (https://gitlab.com/sunandanmukherjee/ncodr.git)
2. If downloaded, extract the ncodr folder.
3. Open a terminal, and navigate to ncodr folder
4. Type ```make``` in the terminal. Upon successful complilation it will create a new ```bin``` directory.
5. Add the path to your ```.bashrc``` as ```NCODR_HOME```. This can be done using the following command from the ```ncodr``` directory:

```
echo "export NCODR_PATH=`pwd`" >> ~/.bashrc

```
6. For accessing ```NCodR``` from elsewhere, it's path should be added to ```.bashrc```.

## Running NCodR locally
NCodR can be used as a standalone tool. However, to run it locally, the dependencies and the thrid party tools should be installed/downloaded.

Usage:

```
        positional arguments:
          input                 Input file name [RNA sequences in fasta format].

        optional arguments:
          -h, --help            show this help message and exit
          -r, --redundant       remove redundant sequence [default = OFF]
          -c, --clean           clean the intermediate files [default = ON]
          -o OUTPUT, --output OUTPUT
                                Output file name [<input>.ncodr if not provided]

```



Example:
```
        ./NCodR.py <input file>
```
Input file should be provided in fasta format. Upon successful completion, the program will print
the output in the terminal. Additionally, output will also be saved in a text file with ```.ncodr```
extension. 

##Test run

A sample dataset is provided in the ```examples/``` directory, which can be used for a test run. For a quick test run, type the following command from the terminal:
```
./NCodR.py examples/test.fa
```
This should print the prediction results on the screen, as well as generate a file ```(test.fa.ncodr)``` with the prediction results.

## Training and testing
Both training and testing of the final model is done using ThunderSVM.

## Comparison between different machine learning techniques
Eight different classification algorithms were compared to select the best approach. It is implemented in ```model_comparison.py``` script. Classification algorithms are used as implemented in Scikit learn module.
Following python libraries needed to be installed to run these scripts:
1. Numpy 
2. Scikit learn
3. Pickle
4. Joblib
5. Matplotlib


# Calculation of features

## Dependencies
1. g++ compiler with C+11 support
2. javac compiler 


The programs can be compiled by running make. The binaries will be available in the bin folder.

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

