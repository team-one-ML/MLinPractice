#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Train or evaluate a single classifier with its given set of hyperparameters.

Created on Wed Sep 29 14:23:48 2021

@author: lbechberger
"""

import argparse, pickle
from numpy import true_divide
from sklearn.svm import LinearSVC
from sklearn.dummy import DummyClassifier
from sklearn.metrics import accuracy_score, cohen_kappa_score, balanced_accuracy_score, matthews_corrcoef, f1_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier

# setting up CLI
parser = argparse.ArgumentParser(description = "Classifier")
parser.add_argument("input_file", help = "path to the input pickle file")
parser.add_argument("-s", '--seed', type = int, help = "seed for the random number generator", default = None)
parser.add_argument("-e", "--export_file", help = "export the trained classifier to the given location", default = None)
parser.add_argument("-i", "--import_file", help = "import a trained classifier from the given location", default = None)
parser.add_argument("-m", "--majority", action = "store_true", help = "majority class classifier", default = None)
parser.add_argument("-q", "--frequency", action = "store_true", help = "label-frequency class classifier", default = None)
parser.add_argument("--svm", action = "store_true", help = "Support-Vector-Machine classifier", default = None)
parser.add_argument("--mlp", action = "store_true", help = "Multi-Layered-Perceptron classifier", default = None)
parser.add_argument("-a", "--accuracy", action = "store_true", help = "evaluate using accuracy")
parser.add_argument("-b", "--balanced_accuracy", action = "store_true", help = "evaluate using balanced accuracy")
parser.add_argument("-n", "--informedness", action = "store_true", help = "evaluate using informedness")
parser.add_argument("-k", "--kappa", action = "store_true", help = "evaluate using Cohen's kappa")
parser.add_argument("-f", "--f1_score", action = "store_true", help = "evaluate using the F1 score (or F-measure)")
parser.add_argument("--knn", action = "store_true", help = "use KNN classifier", default=None)
parser.add_argument("--mcc", action = "store_true", help = "evaluate using Mathews Correlation coefficient")
args = parser.parse_args()

# load data
with open(args.input_file, 'rb') as f_in:
    data = pickle.load(f_in)

if args.import_file is not None:
    # import a pre-trained classifier
    with open(args.import_file, 'rb') as f_in:
        classifier = pickle.load(f_in)

else:   # manually set up a classifier
    
    if args.majority:
        # majority vote classifier
        print("    majority vote classifier")
        classifier = DummyClassifier(strategy = "most_frequent", random_state = args.seed)
        classifier.fit(data["features"], data["labels"])

    elif args.frequency:
        # label-frequency classifier
        print("    label-frequency classifier")
        classifier = DummyClassifier(strategy = "stratified", random_state = args.seed)
        classifier.fit(data["features"], data["labels"])

    elif args.svm:
        #  Support Vector Machine
        print("    SVM classifier")
        classifier = LinearSVC(dual=False, class_weight='balanced', random_state = args.seed)
        classifier.fit(data["features"], data["labels"].ravel())

    elif args.knn:
        # KNN classifier
        print("    KNN classifier")
        classifier = KNeighborsClassifier(algorithm="auto", weights="distance", n_neighbors=10, random_state = args.seed)
        classifier.fit(data["features"], data["labels"].ravel())

    elif args.mlp:
        #MLP classifier
        print("    MLP classifier")
        classifier = MLPClassifier(random_state = args.seed, verbose = True)
        classifier.fit(data["features"], data["labels"].ravel())


# now classify the given data
prediction = classifier.predict(data["features"])

# collect all evaluation metrics
evaluation_metrics = []
if args.accuracy:
    evaluation_metrics.append(("Accuracy", accuracy_score))
if args.balanced_accuracy:
    evaluation_metrics.append(("Balanced accuracy", balanced_accuracy_score))
if args.informedness:
    evaluation_metrics.append(("Informedness", lambda x,y: balanced_accuracy_score(x,y, adjusted=True)))
if args.kappa:
    evaluation_metrics.append(("Cohen's kappa score", cohen_kappa_score))
if args.f1_score:
    evaluation_metrics.append(("F1 score", f1_score))
if args.mcc:
    # Division by zero may happen in this function, which produces a warning
    # see https://en.wikipedia.org/wiki/Matthews_correlation_coefficient
    evaluation_metrics.append(("MCC", matthews_corrcoef))

# compute and print them
for metric_name, metric in evaluation_metrics:
    print("    {0}: {1}".format(metric_name, metric(data["labels"], prediction)))
    
# export the trained classifier if the user wants us to do so
if args.export_file is not None:
    with open(args.export_file, 'wb') as f_out:
        pickle.dump(classifier, f_out)
        
        