#!/usr/bin/env python

import numpy as np
import pickle
import warnings

from sys import argv
import joblib
from sklearn import preprocessing

abvr = {'L':'lncRNA', 'M':'miRNA', 'R':'rRNA', 'SNO':'snoRNA', 'T':'tRNA', 'SN':'snRNA', 'P':'premiRNA'}

#clf = joblib.load('NCodR.pkl') #old version
clf = joblib.load(open('NCodR_py3_rbf.pkl',"rb"))

fn = argv[1]
f= open(fn).readlines()

array = []
seqid = []
result = []

for ele in range(1, len(f)):
	arr = []
	line = f[ele].rstrip().split('\t')
	seqid.append(line[0])

if __name__ == "__main__":        
	X = np.genfromtxt(fn, delimiter='\t', dtype=None)
	
	array = np.asarray(X, dtype = None)
	#print(array)
	#array = X[0:, 1:]
	array = array[1:,1:]

	#print(array)

	scaler = preprocessing.StandardScaler()
	params = scaler.fit_transform(array)

	pred = clf.predict(params)
	result.append(pred)
        
	output = np.vstack([seqid, result]).T

	for line in output:
		try:
			print ('{}: {}'.format(line[0], abvr[line[1]]))
		except:
			pass
