#!/usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import pandas as pd
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
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.metrics import classification_report, roc_auc_score

names = ["k-Nearest Neighbors", "Linear SVM",
         "Decision Tree", "Random Forest", "Neural Net", "AdaBoost",
         "Naive Bayes", "QDA"]

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
'''
names = ["Nearest Neighbors", "Linear SVM"]
'''
classifiers = [
    KNeighborsClassifier(10),
    SVC(kernel="linear", C=[0.1, 1, 10, 100]),
    DecisionTreeClassifier(),
    RandomForestClassifier(n_estimators=1000),
    BernoulliRBM(),
    AdaBoostClassifier(),
    GaussianNB(),
    QuadraticDiscriminantAnalysis()]

def conditions(cm):
    TP = []
    TN = []
    FP = []
    FN = []
    rows = []
    columns =[]
    targets = len(cm[0])
    #cm = np.array(cm)
    for i in range(0, targets):
        TP.append(cm[i][i])
        rows.append(sum(cm[i][j] for j in range(0, targets)))
        columns.append(sum(cm[j][i] for j in range(0, targets)))
    for i in range(0,len(TP)):
        TN.append(sum(TP)-cm[i][i])
        FP.append(rows[i]-cm[i][i])
        FN.append(columns[i]-cm[i][i])
    print (TP, TN, FP, FN)
    '''
    avg_tp = np.sum(TP)#/len(TP)
    avg_tn = np.sum(TN)#/len(TN)
    avg_fp = np.sum(FP)#/len(FP)
    avg_fn = np.sum(FN)#/len(FN)
    npv = avg_tn/(avg_tn+avg_fn)  # negative predictive value (NPV)
    ppv = avg_tp/np.sum(TP,FP)  # precision or positive predictive value (PPV)
    trp = avg_tp/(avg_tp+avg_fn)  # sensitivity, recall, hit rate, or true positive rate (TPR)
    f_score = 2*(ppv*trp)/(ppv+trp) # harmonic mean of precision and sensitivity
    #mcc = (avg_tp*avg_tn)-(avg_fp*avg_fn)/math.sqrt((avg_tp+avg_fp)(avg_tp*avg_fn)(avg_tn*avg_fn)(avg_tn*avg_fn))
    
    print npv, ppv, trp, f_score
    '''
def plot_confusion_matrix(cm, labels, title, cmap=plt.cm.Blues):
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title, fontname="times new roman", fontsize=24)
    plt.colorbar()
    tick_marks = np.arange(len(labels))
    plt.xticks(tick_marks, labels, rotation=0, fontname="times new roman", fontsize=19)
    plt.yticks(tick_marks, labels, fontname="times new roman", fontsize=19)
    plt.tight_layout()
    plt.ylabel('True label', fontname="times new roman", fontsize=22)
    plt.xlabel('Predicted label', fontname="times new roman", fontsize=22)
    plt.savefig(title+'.png', dpi=600, format='png')
    #plt.show()

def main():
    array = np.genfromtxt("All_ncRNAs.tsv", delimiter='\t', dtype=None)
    array = np.asarray(array, dtype = None)

    X = array[1:,1:-1]
    y = array[1:,-1]

    labels = ['lncRNA', 'miRNA', 'rRNA', 'snoRNA', 'tRNA', 'snRNA', 'premiRNA']

    x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.05, random_state=42)

    scaler = preprocessing.StandardScaler()
    x_train = scaler.fit_transform(x_train)
    x_test = scaler.transform(x_test)
    
    '''
    x_min, x_max = X[:, 0].min() - .5, X[:, 0].max() + .5
    y_min, y_max = X[:, 1].min() - .5, X[:, 1].max() + .5
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                         np.arange(y_min, y_max, h))

    # plot the dataset 
    figure = plt.figure(figsize=(27, 3))
    cm = plt.cm.RdBu
    cm_bright = ListedColormap(['#FF0000', '#0000FF'])
    ax = plt.subplot(1, len(classifiers) + 1, 1)

    # Plot the training points
    ax.scatter(X_train[:, 0], X_train[:, 1], c=y_train, cmap=cm_bright,
               edgecolors='k')
    # and testing points
    ax.scatter(X_test[:, 0], X_test[:, 1], c=y_test, cmap=cm_bright, alpha=0.6,
               edgecolors='k')
    ax.set_xlim(xx.min(), xx.max())
    ax.set_ylim(yy.min(), yy.max())
    ax.set_xticks(())
    ax.set_yticks(())

    # iterate over classifiers
    for name, clf in zip(names, classifiers):
        ax = plt.subplot(len(datasets), len(classifiers) + 1, i)
        clf.fit(X_train, y_train)
        score = clf.score(X_test, y_test)

        # Plot the decision boundary. For that, we will assign a color to each
        # point in the mesh [x_min, x_max]x[y_min, y_max].
        if hasattr(clf, "decision_function"):
            Z = clf.decision_function(np.c_[xx.ravel(), yy.ravel()])
        else:
            Z = clf.predict_proba(np.c_[xx.ravel(), yy.ravel()])[:, 1]
        
        # Put the result into a color plot
        Z = Z.reshape(xx.shape)
        ax.contourf(xx, yy, Z, cmap=cm, alpha=.8)

        # Plot also the training points
        ax.scatter(X_train[:, 0], X_train[:, 1], c=y_train, cmap=cm_bright,
                   edgecolors='k')
        # and testing points
        ax.scatter(X_test[:, 0], X_test[:, 1], c=y_test, cmap=cm_bright,
                   edgecolors='k', alpha=0.6)

        ax.set_xlim(xx.min(), xx.max())
        ax.set_ylim(yy.min(), yy.max())
        ax.set_xticks(())
        ax.set_yticks(())

        ax.set_title(name)
        ax.text(xx.max() - .3, yy.min() + .3, ('%.2f' % score).lstrip('0'),
                size=15, horizontalalignment='right')

    plt.tight_layout()
    plt.show()

    '''
    #param_grid = {"C": np.logspace(-2, 5, 8), "kernel": ["rbf"]}
    #cv = StratifiedKFold(y_train, n_folds=2)
    #clf = SVC()
    for name, clf in zip(names, classifiers):
        #grid = GridSearchCV(clf, param_grid=param_grid, cv=cv)
        #grid = GridSearchCV(clf)
        #grid.fit(x_train, y_train)
        clf.fit(x_train, y_train)
        
        #joblib.dump(clf, 'NCodR.pkl')
        
        #y_pred = grid.predict(x_test)
        
        #clf1 = joblib.load('NCodR.pkl')
        try:
            y_pred = clf.predict(x_test)
        except AttributeError:
            pass
        #print name, (np.sum(y_pred == y_test) / float(len(y_pred)))
        #print(classification_report(y_test, y_pred, target_names=labels))
        cm = metrics.confusion_matrix(y_test, y_pred)
        print (name)
        print (cm)
        #conditions(cm)
        
        
        #cm = metrics.confusion_matrix(y_test, y_pred)
        #print(np.sum(y_pred == y_test) / float(len(y_pred)))
        #cm_norm = pd.crosstab(y_test, y_pred, rownames=['True'], colnames=['Predicted'], margins = True)
        #print(cm_norm)
        np.set_printoptions(precision=2)
        #print('Confusion matrix, without normalization')
        #print(cm)
        #plt.figure()
        #plot_confusion_matrix(cm, labels)

        cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        #print('Normalized confusion matrix')
        #print(cm_normalized)
        plt.figure()
        plot_confusion_matrix(cm_normalized, labels, title= name)

        #plt.show()
    '''    
    param_grid = {"C": np.logspace(-2, 5, 8), "kernel": ["rbf"]}
    cv = StratifiedKFold(y_train, n_folds=2)
    clf1 = SVC()
    grid = GridSearchCV(clf1, param_grid=param_grid, cv=cv)
    #grid.fit(x_train, y_train)
    clf1.fit(x_train, y_train)
    y_pred = clf1.predict(x_test)
    cm = metrics.confusion_matrix(y_test, y_pred)
    np.set_printoptions(precision=2)
    cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    plt.figure()
    plot_confusion_matrix(cm_normalized, labels, title= "SVM RBF")
    plt.show()
    '''
    
if __name__ =="__main__":
    main()

