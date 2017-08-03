import sys
import random
import time
import os
import codecs
import nltk
import json
import pymongo
from multiprocessing import Pool
import threading
from bson.objectid import ObjectId
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.feature_extraction import DictVectorizer
from sklearn import svm
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import classification_report
from sklearn.metrics import f1_score
from pymongo import MongoClient
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import os

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
            from featurize import feature_generation
            features = feature_generation(_input, lang)
            db.feature_list.insert({'_id': obj['_id'], 'lang': lang, 'features': features})
        else:
            features = feature_obj['features']

        data.append((transform_features(features), _output))
        percent_completed = (count / total) * 100
        if last_printed != int(percent_completed) and int(percent_completed) % 10 is 0:
            print ("Completed loading.. %.2f%%" % (percent_completed))
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
                print (set([u[1] for u in ndata]))
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
        print( "\tResults for NB, SVM (linear and RBF) with max accuracy", display_accuracy, display_train_percent)
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
    print('[Training %.2f%%, Accuracy %.2f%%]' % ( tp, overall_accuracy[0] * 100))
    # _id = db_features.replace('ss_', '').replace('_db', '')
    # db.results_linear_svm.update_one({'_id': _id}, {'$set': {'result': result}}, upsert=True)


def generate_reports(lang='H'):
    if not os.path.exists("../reports"):
        os.mkdir("../reports")

    conn = MongoClient()
    db = conn.sentiment_analysis_db

    fields = [
            ('lang', "%s"),
            ('train_percent', "%d"),
            ('total', "%d"),
            ('max_accuracy', "%.2f"),
            ('linear_svm', "%.2f"),
            ('rbf_svm', "%.2f"),
            ('nb', "%.2f")
            ]

    HNB = []
    HRBFSVM = []
    HLSVM = []
    MNB = []
    MRBFSVM = []
    MLSVM = []
    
    
    hindi_overall = db.results_overall.find_one({'lang': 'H'})
    marathi_overall = db.results_overall.find_one({'lang': 'M'})
    
    with open('../reports/output.csv', 'w') as outfile:
        outfile.write("Lang, Overall Accuracy, Overall F1 Score, Train Percent, Total, Max Accuracy, Max F1 Score, SVM (linear) Accuracy, SVM (linear) F1 Score, SVM (RBF) Accuracy, SVM (RBF) F1 Score, Naive Bayes Accuracy, Naive Bayes F1 Score\n")
        for data in db.results_percentwise.find({}):
            
            overall = hindi_overall if 'H' in str(data['lang']) else marathi_overall
            print (data['lang'], overall['accuracy'], 'H' in str(data['lang']))
            d = [
                    data['lang'],
                    "%.2f" % overall['accuracy'],
                    "%.2f" % overall['f1_score'],
                    "%d" % data['train_percent'],
                    "%d" % data['total'],
                    "%.2f" % data['max_accuracy'][0],
                    "%.2f" % data['max_accuracy'][1],
                    "%.2f" % data['linear_svm'][0],
                    "%.2f" % data['linear_svm'][1],
                    "%.2f" % data['rbf_svm'][0],
                    "%.2f" % data['rbf_svm'][1],
                    "%.2f" % data['nb'][0],
                    "%.2f" % data['nb'][1]
                ]
            outfile.write(','.join(d) + '\n')
            if data['lang'] == 'H':
                HNB.append((data['train_percent'], (data['max_accuracy'][0] * 100, data['nb'][0] * 100)))
                HRBFSVM.append((data['train_percent'], (data['max_accuracy'][0] * 100, data['rbf_svm'][0] * 100)))
                HLSVM.append((data['train_percent'], (data['max_accuracy'][0] * 100, data['linear_svm'][0] * 100)))
            else:
                MNB.append((data['train_percent'], (data['max_accuracy'][0] * 100, data['nb'][0] * 100)))
                MRBFSVM.append((data['train_percent'], (data['max_accuracy'][0] * 100, data['rbf_svm'][0] * 100)))
                MLSVM.append((data['train_percent'], (data['max_accuracy'][0] * 100, data['linear_svm'][0] * 100)))

    HNB = sorted(HNB)
    HRBFSVM = sorted(HRBFSVM)
    HLSVM = sorted(HLSVM)
    MNB = sorted(MNB)
    MRBFSVM = sorted(MRBFSVM)
    MLSVM = sorted(MLSVM)
    
    if lang == 'H':
        charts = [
            ("hindi-nb", "Naive Bayes", HNB),
            ("hindi-lsvm", "Linear SVM", HLSVM),
            ("hindi-svm", "RBF SVM", HRBFSVM)
            ]
    else:
        charts = [
            ("marathi-nb", "Naive Bayes", MNB),
            ("marathi-lsvm", "Linear SVM", MLSVM),
            ("marathi-svm", "RBF SVM", MRBFSVM)
            ]
    

    # No Display
    matplotlib.use('Agg')
    
    
    for filename, algorithm, data in charts:
        xaxis = np.array([u[0] for u in data])
        yaxis_max_accuracy = np.array([u[1][0] for u in data])
        yaxis_specific = np.array([u[1][1] for u in data])
        
        fig = plt.figure()
        ax = fig.add_subplot(111)
        lns1 = ax.plot(xaxis, yaxis_max_accuracy, '-', label='Max Accuracy')
        lns2 = ax.plot(xaxis, yaxis_specific, '-', label=algorithm)
        ax.legend(loc=0)
        ax.grid()
        ax.set_xlabel("Training Data (%)")
        ax.set_ylabel("Accuracy (%)")
        ax.set_ylim(0, 100)
        plt.savefig("../reports/" + filename + ".png", format='png')
        #plt.show()
        plt.clf()

if __name__ == '__main__':
    # print ('[1] Machine learning report generation for Hindi Code Mix')
    # train_test('H')
    for lang in ['H', 'M']:
        print ('[*] Machine learning report generation for %s Code Mix' % 'Hindi' if lang == 'H' else 'Marathi')
        train_test(lang)
        generate_reports(lang)