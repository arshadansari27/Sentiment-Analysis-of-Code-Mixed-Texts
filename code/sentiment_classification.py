# You need to install scikit-learn:
# sudo pip install scikit-learn
#
# Dataset: Polarity dataset v2.0
# http://www.cs.cornell.edu/people/pabo/movie-review-data/
#
# Full discussion:
# https://marcobonzanini.wordpress.com/2015/01/19/sentiment-analysis-with-python-and-scikit-learn


import sys
import os
import time
import random

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.feature_extraction import DictVectorizer
from sklearn import svm
from sklearn.metrics import classification_report
import pymongo

db = pymongo.MongoClient().sentiments

if __name__ == '__main__':

    # Read the data
    train_data = []
    train_labels = []
    test_data = []
    test_labels = []
    lines = []
    for obj in db.features.find({}):
        _input = obj['input']
        _output = obj['output']

        __d = {
            'pscore': 0.,
            'nscore': 0.,
        }

        for w, p, n, pr in _input:
            __d[w] = 1
            __d['pscore'] += p
            __d['nscore'] += n
            # __d['pwords'][pr] = 1 


        if random.random() > .7:
            test_data.append(__d)
            test_labels.append(_output)
        else:
            train_data.append(__d)
            train_labels.append(_output)

    '''
    vectorizer = TfidfVectorizer(min_df=5,
                                 max_df = 0.8,
                                 sublinear_tf=True,
                                 use_idf=True)
    '''
    vectorizer = DictVectorizer()
    train_vectors = vectorizer.fit_transform(train_data)
    test_vectors = vectorizer.transform(test_data)

    # Perform classification with SVM, kernel=rbf
    classifier_rbf = svm.SVC()
    t0 = time.time()
    classifier_rbf.fit(train_vectors, train_labels)
    t1 = time.time()
    prediction_rbf = classifier_rbf.predict(test_vectors)
    t2 = time.time()
    time_rbf_train = t1-t0
    time_rbf_predict = t2-t1

    # Perform classification with SVM, kernel=linear
    classifier_linear = svm.SVC(kernel='linear')
    t0 = time.time()
    classifier_linear.fit(train_vectors, train_labels)
    t1 = time.time()
    prediction_linear = classifier_linear.predict(test_vectors)
    t2 = time.time()
    time_linear_train = t1-t0
    time_linear_predict = t2-t1

    # Perform classification with SVM, kernel=linear
    classifier_liblinear = svm.LinearSVC()
    t0 = time.time()
    classifier_liblinear.fit(train_vectors, train_labels)
    t1 = time.time()
    prediction_liblinear = classifier_liblinear.predict(test_vectors)
    t2 = time.time()
    time_liblinear_train = t1-t0
    time_liblinear_predict = t2-t1

    # Print results in a nice table
    print("Results for SVC(kernel=rbf)")
    print("Training time: %fs; Prediction time: %fs" % (time_rbf_train, time_rbf_predict))
    print(classification_report(test_labels, prediction_rbf))
    print("Results for SVC(kernel=linear)")
    print("Training time: %fs; Prediction time: %fs" % (time_linear_train, time_linear_predict))
    print(classification_report(test_labels, prediction_linear))
    print("Results for LinearSVC()")
    print("Training time: %fs; Prediction time: %fs" % (time_liblinear_train, time_liblinear_predict))
    print(classification_report(test_labels, prediction_liblinear))
