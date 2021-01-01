#!/usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import pickle
import math

import argparse
import os, sys

from sklearn import metrics, preprocessing, feature_selection
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import StratifiedKFold, train_test_split
import joblib

from sklearn.neural_network import BernoulliRBM
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, VotingClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.metrics import classification_report, roc_auc_score

    
def meta_classifier():
    clfs = [('knn', KNeighborsClassifier(10)),
    ('svm-lin', SVC(probability=True, kernel="linear", C=0.1)),
    ('decitree', DecisionTreeClassifier()),
    ('rf', RandomForestClassifier(n_estimators=1000)),
    ('ada_boost', AdaBoostClassifier(n_estimators=1000)),
    ('gNB', GaussianNB()),
    ('qda', QuadraticDiscriminantAnalysis()),
    ('svm-rbf', SVC(probability=True, kernel="rbf", C=0.1))
    ]
    ensemble = VotingClassifier(estimators=clfs, voting = 'soft')
    return ensemble
    

def classifiers_list():

    classifiers = [
        KNeighborsClassifier(10),
        SVC(probability=True, kernel="linear", C=0.1),
        DecisionTreeClassifier(),
        RandomForestClassifier(n_estimators=1000),
        AdaBoostClassifier(),
        GaussianNB(),
        QuadraticDiscriminantAnalysis(),
        SVC(probability=True, kernel="rbf", C=0.1),
        meta_classifier()
        ]
    return classifiers

def conditions(cm):
    TP = []
    TN = []
    FP = []
    FN = []
    rows = []
    columns =[]
    targets = len(cm[0])
    for i in range(0, targets):
        TP.append(cm[i][i])
        rows.append(sum(cm[i][j] for j in range(0, targets)))
        columns.append(sum(cm[j][i] for j in range(0, targets)))
    for i in range(0,len(TP)):
        TN.append(sum(TP)-cm[i][i])
        FP.append(rows[i]-cm[i][i])
        FN.append(columns[i]-cm[i][i])
    print (TP, TN, FP, FN)

def plot_confusion_matrix(cm, labels, title, cmap=plt.cm.Blues):
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title, fontname="times new roman", fontsize=14)
    plt.colorbar()
    tick_marks = np.arange(len(labels))
    plt.xticks(tick_marks, labels, rotation=0, fontname="times new roman", fontsize=11)
    plt.yticks(tick_marks, labels, fontname="times new roman", fontsize=11)
    plt.tight_layout()
    plt.ylabel('True label', fontname="times new roman", fontsize=12)
    plt.xlabel('Predicted label', fontname="times new roman", fontsize=12)
    plt.savefig(title+'.png', dpi=300, format='png')
    #plt.show()

def main():
    
    names = ["k-Nearest Neighbors", "Linear SVM",
         "Decision Tree", "Random Forest", "AdaBoost",
         "Naive Bayes", "QDA", "SVM-RBF", "Meta-classifier"]

    parser = argparse.ArgumentParser(prog='model_comparison.py', usage='%(prog)s [options]')
    parser.add_argument("-i", "--input", required=True, dest="input_file", type=str,
                        help="Input file name [required].")
    args = parser.parse_args()
    input_file = args.input_file

    #checking the input file
    if input_file != "":
        if(os.path.isfile(input_file) == False): #checking input_file
            print ("input location/file: "+input_file+" provided by the user doesn't exist", file=sys.stderr)
            sys.exit(1)
    
    array = np.genfromtxt(input_file, delimiter='\t', dtype=None, encoding=None)
    array = np.asarray(array, dtype = None)

    X = array[1:,1:-1]
    y = array[1:,-1]

    labels = ['lncRNA', 'miRNA', 'rRNA', 'snoRNA', 'tRNA', 'snRNA', 'premiRNA']

    x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=42)

    scaler = preprocessing.StandardScaler()
    x_train = scaler.fit_transform(x_train)
    x_test = scaler.transform(x_test)
    classifiers= classifiers_list()
    
    for name, clf in zip(names, classifiers):
        clf.fit(x_train, y_train)

        try:
            y_pred = clf.predict(x_test)
        except AttributeError:
            pass

        cm = metrics.confusion_matrix(y_test, y_pred)
        print (name)
        print (cm)
        np.set_printoptions(precision=2)

        cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print('Normalized confusion matrix')
        print(cm_normalized)
        plt.figure()
        plot_confusion_matrix(cm_normalized, labels, title= name)

        #plt.show()
    
if __name__ =="__main__":
    main()

