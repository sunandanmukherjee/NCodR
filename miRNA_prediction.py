#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
#import pandas as pd
import pickle
import argparse
import os, sys

from sklearn import svm, metrics, preprocessing, feature_selection
from sklearn.pipeline import Pipeline
#from sklearn.grid_search import GridSearchCV //old version
from sklearn.model_selection import GridSearchCV 
#from sklearn.cross_validation import StratifiedKFold, train_test_split //old version
from sklearn.model_selection import StratifiedKFold, train_test_split
#from sklearn.externals import joblib //old version
import joblib

parser = argparse.ArgumentParser(prog='miRNA_prediction.py', usage='%(prog)s [options]')
parser.add_argument("-i", "--input", required=True, dest="input_file", type=str,
                    help="Input file name [required].")
parser.add_argument("-n", "--no-of-jobs", required=False, dest="number_of_jobs", default=3, type=int,
                        help="Number of jobs [default = 3].")
args = parser.parse_args()
input_file = args.input_file
number_of_jobs = args.number_of_jobs

#checking the input file
if input_file != "":
    if(os.path.isfile(input_file) == False): #checking input_file
        print ("input location/file: "+input_file+" provided by the user doesn't exist", file=sys.stderr)
        sys.exit(1)

def plot_confusion_matrix(cm, labels, title='Confusion matrix', cmap=plt.cm.Blues):
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title, fontname="times new roman", fontsize=16)
    plt.colorbar()
    tick_marks = np.arange(len(labels))
    plt.xticks(tick_marks, labels, rotation=0, fontname="times new roman", fontsize=10)
    plt.yticks(tick_marks, labels, fontname="times new roman", fontsize=10)
    plt.tight_layout()
    plt.ylabel('True label', fontname="times new roman", fontsize=14)
    plt.xlabel('Predicted label', fontname="times new roman", fontsize=14)
    plt.savefig('norm2_cm_poly.png', dpi=600, format='png')
    #plt.show()
    
def read_tsv(fn):
        f= open(fn).readlines()
        array = []
        for ele in range(1,len(f)):
                arr = []
                line = f[ele].rstrip().split('\t')
                
                for each in range(1, len(line)-1):
                        arr.append(float(line[each]))
                arr = arr + list(line[-1])
                array.append(arr)

        return array

def main():
	array = np.genfromtxt(input_file, delimiter='\t', dtype=None, encoding=None)
	#array = read_tsv("training_all.tsv")
	array = np.asarray(array, dtype = None)
	X = array[1:,1:-1]
	y = array[1:,-1]
	ids = array[1:,0]
	results=[]
	
	labels = ['lncRNA', 'miRNA', 'rRNA', 'snoRNA', 'tRNA', 'snRNA', 'premiRNA']

	x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.05, random_state=42)

	scaler = preprocessing.StandardScaler()
	x_train = scaler.fit_transform(x_train)
	x_test = scaler.transform(x_test)
	
	param_grid = {"C": np.logspace(-2, 5, 8), 'gamma': [1,0.1,0.01,0.001,0.0001], 'kernel': ['rbf']}
	#param_grid = {"C": np.logspace(-1, 3, 2), 'gamma': [0.01,0.001], 'kernel': ['rbf']}
	#param_grid = {'C': [0.01, 0.1, 1, 10, 100, 1000], 'gamma': [1,0.1,0.01,0.001,0.0001], 'kernel': ['rbf']}
	#cv = StratifiedKFold(y_train, n_folds=2) #old version
	skf = StratifiedKFold(n_splits=4, random_state=1, shuffle=True)
	clf = svm.SVC()
	grid = GridSearchCV(clf, param_grid=param_grid, cv=skf, refit=True, verbose=3, n_jobs=number_of_jobs)
	grid.fit(x_train, y_train)
	print ("Best parameters = ")
	print(grid.best_params_)
	#clf.fit(x_train, y_train)
	
	joblib.dump(grid, open('NCodR2_py3_rbf.pkl', 'wb'))
	
	y_pred = grid.predict(x_test)
	#clf1 = joblib.load('NCodR.pkl')
	#y_pred = clf.predict(x_test)

	cm = metrics.confusion_matrix(y_test, y_pred)
	print(np.sum(y_pred == y_test) / float(len(y_pred)))

	np.set_printoptions(precision=2)
	print('Confusion matrix, without normalization')
	print(cm)
	plt.figure()
	plot_confusion_matrix(cm, labels)

	cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
	print('Normalized confusion matrix')
	print(cm_normalized)
	plt.figure()
	plot_confusion_matrix(cm_normalized, labels, title='Normalized confusion matrix')

	#plt.show()
	
	
if __name__ =="__main__":
	main()

