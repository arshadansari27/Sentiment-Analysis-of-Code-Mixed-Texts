import sys
import random
import time
import os
import codecs
import nltk
import simplejson as json
import pymongo
from multiprocessing import Pool
import threading
import pandas
from bson.objectid import ObjectId
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.feature_extraction import DictVectorizer
from sklearn import svm
from sklearn.metrics import classification_report


db = pymongo.MongoClient().sentiment_analysis_db

HOME = '/home/arshad/workspace/rest/sentiment-analysis'


def train_test(db_features):
    data = []
    for obj in db[db_features].find({}):
        _input = obj['words']
        _output = obj['output']
        data.append((_input, _output))
    max_accuracy = 0
    ranges = range(40, 100, 10)
    ranges.append(95)
    for tp in ranges:
        train_percent = tp / 100.
        for i in xrange(1):
            random.shuffle(data)
            train_data = []
            train_labels = []
            test_data = []
            test_labels = []
            count = 0
            __d = {}
            for _input, _output in data:
                count += 1
                sentence = ''
                pscore, nscore = 0, 0
                for w, p, n in _input:
                    sentence += ' ' + w
                    if w not in __d:
                        __d[w] = 0
                    __d[w] += 1
                    pscore += p
                    nscore += -1 * n
                #__d['sentence'] = sentence.strip() 
                __d['score'] = pscore + nscore
                __d['pscore'] = pscore 
                __d['nscore'] = nscore

                if len(_input) is 0:
                    continue
                if random.random() <= train_percent:
                    train_data.append(__d)
                    train_labels.append(_output)
                else:
                    test_data.append(__d)
                    test_labels.append(_output)

            vectorizer = DictVectorizer()
            train_vectors = vectorizer.fit_transform(train_data)
            test_vectors = vectorizer.transform(test_data)
            classifier_liblinear = svm.SVC(kernel='linear') #  svm.LinearSVC()
            t0 = time.time()
            classifier_liblinear.fit(train_vectors, train_labels)
            t1 = time.time()
            prediction_liblinear = classifier_liblinear.predict(test_vectors)
            accuracy = sum(1.0 for i, p in enumerate(prediction_liblinear) if p == test_labels[i])
            t2 = time.time()
            time_liblinear_train    = t1 - t0
            time_liblinear_predict  = t2 - t1
        
            #print "Results for LinearSVC With Training Percent", train_percent, 'with accuracy', accuracy, (accuracy / len(prediction_liblinear)), '', 'out of', len(prediction_liblinear)
            max_accuracy = max(float(accuracy)/len(prediction_liblinear), max_accuracy)
            #print("Training time: %fs; Prediction time: %fs" % (time_liblinear_train, time_liblinear_predict))
            #print(classification_report(test_labels, prediction_liblinear))
            print '\t[Training %f%%, Accuracy %f%%]' % (train_percent * 100, max_accuracy * 100)
    result = max_accuracy
    print 'Average Improvements', result
    _id = db_features.replace('ss_', '').replace('_db', '')
    db.results_linear_svm.update_one({'_id': _id}, {'$set': {'result': result}}, upsert=True)


if __name__ == '__main__':
    print '[1] Machine learning report generation for Plain Hindi directly after language identification'
    train_test('ss_li_hindi_db')
    print '[2] Machine learning report generation for Mixed Hindi directly after language identification'
    train_test('ss_li_hindi_mix_db')
    print '[3] Machine learning report generation for Marathi directly after language identification'
    train_test('ss_li_marathi_db')
    print '[4] Machine learning report generation for Plain Hindi after plain POS Tagging'
    train_test('ss_pos_hindi_db')
    print '[5] Machine learning report generation for Mixed Hindi after plain POS Tagging'
    train_test('ss_pos_hindi_mix_db')
    print '[6] Machine learning report generation for Plain Hindi after merged POS Tagging'
    train_test('ss_pos_merged_hindi_db')
    print '[7] Machine learning report generation for Mixed Hindi after merged POS Tagging'
    train_test('ss_pos_merged_hindi_mix_db')
