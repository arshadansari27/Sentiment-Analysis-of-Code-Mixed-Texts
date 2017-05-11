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
from bson.objectid import ObjectId
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.feature_extraction import DictVectorizer
from sklearn import svm
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import classification_report
from featurize import feature_generation
from sklearn.metrics import f1_score


db = pymongo.MongoClient().sentiment_analysis_db

def transform_features(feature):
    dic = {}
    words = []
    for w, t, p, n in feature:
        if dic.get(w) and dic[w] != 'slang':
            continue
        dic[w] = (t, p, n)
        words.append(w)
    nfeatures = []
    for w in words:
        t, p, n = dic[w]
        nfeatures.append((w, t, p, n))
    return nfeatures


def get_updated_features(lang):
    data = []
    total = db['csv_input_all'].find({'lang': lang}).count()
    count = 0.
    last_printed = None
    for obj in db['csv_input_all'].find({'lang': lang}):
        count += 1.
        _input = obj['line']
        _output = obj['output']
        ## Featurize
        feature_obj = db.feature_list.find_one({'_id': obj['_id']})
        if not feature_obj:
            features = feature_generation(_input, lang)
            db.feature_list.insert({'_id': obj['_id'], 'lang': lang, 'features': features})
        else:
            features = feature_obj['features']

        data.append((transform_features(features), _output))
        percent_completed = (count / total) * 100
        if last_printed != int(percent_completed) and int(percent_completed) % 10 is 0:
            print "Completed loading.. %.2f%%" % (percent_completed)
            last_printed = int(percent_completed)
    return data

def run_classifier_test(
        classifier,
        train_vectors,
        train_labels,
        test_vectors,
        test_labels,
        train_total,
        total):
    # vectorizer = DictVectorizer()
    # train_vectors = vectorizer.fit_transform(train_data)
    # test_vectors = vectorizer.transform(test_data)
    t0 = time.time()
    classifier_fit = classifier.fit(train_vectors, train_labels)
    t1 = time.time()
    prediction = classifier_fit.predict(test_vectors)
    t2 = time.time()
    time_train = t1 - t0
    time_test = t2 - t1
    # print("Training time: %fs; Prediction time: %fs; F1 Score: %.2f" % (time_train, time_test, f1score))
    # print(classification_report(test_labels, prediction))
    correct_sum = sum(1.0 for i, p in enumerate(prediction) if p == test_labels[i])
    if correct_sum > 0:
        f1score = f1_score(test_labels, prediction, average='weighted')
    else:
        f1score = 0.
    total_tested = len(prediction)
    accuracy = correct_sum / total_tested
    return accuracy, f1score

def run_nb_test(train_vectors, train_labels, test_vectors, test_labels, train_total, total):
    train_vectors = train_vectors.todense()
    test_vectors = test_vectors.todense()
    return run_classifier_test(GaussianNB(), train_vectors, train_labels, test_vectors, test_labels, train_total, total)


def run_svm_rbf_test(train_vectors, train_labels, test_vectors, test_labels, train_total, total):
    return run_classifier_test(svm.SVC(), train_vectors, train_labels, test_vectors, test_labels, train_total, total)

def run_svm_linear_test(train_vectors, train_labels, test_vectors, test_labels, train_total, total):
    return run_classifier_test(svm.SVC(kernel='linear'), train_vectors, train_labels, test_vectors, test_labels, train_total, total)


def run_train_test(train_data, train_labels, test_data, test_labels, train_total, total):
    vectorizer = DictVectorizer()
    train_vectors = vectorizer.fit_transform(train_data)
    test_vectors = vectorizer.transform(test_data)
    svm_linear = run_svm_linear_test(train_vectors, train_labels, test_vectors, test_labels, train_total, total)
    svm_rbf = run_svm_rbf_test(train_vectors, train_labels, test_vectors, test_labels, train_total, total)
    nb = run_nb_test(train_vectors, train_labels, test_vectors, test_labels, train_total, total)
    return nb, svm_linear, svm_rbf


def train_test(lang='H'):
    db.results_percentwise.remove({'lang': lang})
    db.results_overall.remove({'lang': lang})
    data = get_updated_features(lang)
    overall_accuracy = 0., 0.
    ranges = range(4, 50, 4)
    ndata = []
    for _input, _output in data:
        if len(_input) is 0:
            continue
        __d = {}
        pscore, nscore = 0, 0
        sentence = []
        for w, t, p, n in _input:
            pscore += p
            nscore += -1 * n
            sentence.append(w)
            __d[w] = 1
        __d['sentence'] = ' '.join(sentence) #.strip()
        __d['score'] = pscore + nscore
        __d['pscore'] = pscore
        __d['nscore'] = nscore
        ndata.append((__d, _output))
    for tp in ranges:
        ranged_overall_accuracy = 0., 0.
        train_percent = tp / 100.
        for xli in range(10):
            random.shuffle(ndata)
            while len(set([u[1] for u in ndata])) < 3:
                random.shuffle(ndata)
                print set([u[1] for u in ndata])
            train_data = []
            train_labels = []
            test_data = []
            test_labels = []

            for __d, _output in ndata:
                if random.random() <= train_percent:
                    train_data.append(__d)
                    train_labels.append(_output)
                else:
                    test_data.append(__d)
                    test_labels.append(_output)
            nb, svm_linear, svm_rbf = run_train_test(train_data, train_labels, test_data, test_labels, len(train_data), len(ndata))
            max_accuracy = max(svm_linear, svm_rbf, nb, key=lambda u: u[0])
            ranged_overall_accuracy = max(max_accuracy, ranged_overall_accuracy, key=lambda u: u[0])
            overall_accuracy = max(max_accuracy, overall_accuracy, key=lambda u: u[0])
        display_accuracy = "%.2f%%" % (ranged_overall_accuracy[0] * 100)
        display_train_percent = "%.2f%%" % (((len(train_data) * 1.) / len(ndata)) * 100)
        print "\tResults for NB with accuracy", display_accuracy, display_train_percent
        db.results_percentwise.insert({
            'lang': lang,
            'train_percent': tp,
            'total': len(ndata),
            'max_accuracy': ranged_overall_accuracy,
            'linear_svm': svm_linear,
            'rbf_svm': svm_rbf,
            'nb': nb
        })
    db.results_overall.insert({
        'lang': lang,
        'accuracy': overall_accuracy[0],
        'f1_score': overall_accuracy[1]
    })
    print '[Training %.2f%%, Accuracy %.2f%%]' % ( tp, overall_accuracy[0] * 100)
    # _id = db_features.replace('ss_', '').replace('_db', '')
    # db.results_linear_svm.update_one({'_id': _id}, {'$set': {'result': result}}, upsert=True)


if __name__ == '__main__':
    # print '[1] Machine learning report generation for Hindi Code Mix'
    # train_test('H')
    print '[2] Machine learning report generation for Marathi Code Mix'
    train_test('M')
