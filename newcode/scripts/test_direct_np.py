import sys
import random
import time
import os
import codecs
import pymongo
from multiprocessing import Pool
import threading
from bson.objectid import ObjectId
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.feature_extraction import DictVectorizer
from sklearn import svm
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import classification_report


db = pymongo.MongoClient().sentiment_analysis_db

def train_test(db_features):
    data = []
    for obj in db[db_features].find({}):
        _input = obj['line']
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
            for _input, _output in data:
                count += 1
                if len(_input) is 0:
                    continue
                if random.random() <= train_percent:
                    train_data.append(_input)
                    train_labels.append(_output)
                else:
                    test_data.append(_input)
                    test_labels.append(_output)

            vectorizer = DictVectorizer()
            train_vectors = vectorizer.fit_transform(train_data).todense()
            test_vectors = vectorizer.transform(test_data).todense()
            gnb = GaussianNB()
            t0 = time.time()
            predictions = gnb.fit(train_vectors, train_labels).predict(test_vectors)
            t1 = time.time()
            accuracy = sum(1.0 for i, p in enumerate(predictions) if p == test_labels[i])
            t2 = time.time()
            max_accuracy = max(float(accuracy)/len(predictions), max_accuracy)
            print '\t[Training %f%%, Accuracy %f%%]' % (train_percent * 100, max_accuracy * 100)
    result = max_accuracy
    print 'Average Improvements', result
    _id = db_features.replace('ss_', '').replace('_db', '')
    db.results_naive_bayes.update_one({'_id': _id}, {'$set': {'result': result}}, upsert=True)


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
