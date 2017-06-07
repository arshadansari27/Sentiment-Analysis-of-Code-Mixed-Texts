# -*- coding: utf-8 -*-
"""
Created on Tue May 30 23:36:55 2017

@author: ARSHAD
"""

import pymongo
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder, OneHotEncoder

db = pymongo.MongoClient().sentiment_analysis_new
coll = db.all_input
print (coll.count())

dataset = []

words = set([])
for doc in coll.find({'lang': 'H'}):
    _input = [u.lower() for u in doc['line'].split(' ')]
    output = doc['output']
    for w in _input:
        words.add(w)
    op = [output]
    dataset.append((_input, output))

_words = pd.DataFrame(list([w] for w in words))
labelencoder = LabelEncoder()
transformed_words = labelencoder.fit_transform(_words)
assert len(_words) == len(transformed_words)
word_label_dict = dict(zip(transformed_words, words))
sorted_transformed_words = sorted(transformed_words)

dataset2 = []
count = 0
print (len(dataset))
for ii, oo in dataset:
    if count % 10 is 0:
        print (count)
    count += 1
    ip = []
    __ii = set(ii)
    for i in sorted_transformed_words:
        if word_label_dict[i] in __ii:
            ip.append(1)
        else:
            ip.append(0)
    ip.append(oo)
    dataset2.append(ip)
        
dataset2 = pd.DataFrame(dataset2) 

X = dataset2.iloc[:, :-1].values
y = dataset2.iloc[:, -1].values
                                 
# Splitting the dataset into the Training set and Test set
from sklearn.cross_validation import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.4, random_state = 0)

from sklearn.ensemble import RandomForestClassifier
classifier = RandomForestClassifier(n_estimators = 10, criterion = 'entropy', random_state = 0)
classifier.fit(X, y)

# Predicting the Test set results
y_pred = classifier.predict(X_test)

# Making the Confusion Matrix
from sklearn.metrics import confusion_matrix, accuracy_score
cm = confusion_matrix(y_test, y_pred)
score = accuracy_score(y_test, y_pred)
print(cm)
print(score)
