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
from sklearn.metrics import classification_report


db = pymongo.MongoClient().sentiments2

RESOURCE_FOLDER = '../resources'
from nltk.tokenize import RegexpTokenizer
# HOME = '/home/arshad/workspace/rest/sentiment-analysis'
HOME = '/home/vagrant/inner_workspace/sentiment-analysis-code-mix'

tokenizer = RegexpTokenizer(r'\w+')


def load_seed():
    count = 0
    lines = []
    for line in open(HOME + '/resources/sentiment_input.txt'):
        line  = line.strip().decode('utf-8')
        count += 1
        if count % 10 is 0: 
            print count
        line = line.strip()
        if len(line) is 0:
            continue
        x = line.split('|')
        u, v = x[0], x[1]
        u, v = u.strip(), v.strip()
        if len(u) == 0 or len(v) == 0:
            continue
        lines.append((v, u))
    db.lines.insert_many([{'line': u, 'output': v} for (u, v) in lines])
    print db.lines.count()

def start_tagging(other_lang='H'):
    global pool
    print 'Start Tagging...'
    from language_identification import emoticons
    from pos_tag import tag_words_english, tag_words_hindi
    from sentiment import sentiment as stmt
    
    E_TAGS = set(['JJ', 'JJR', 'JJS', 'IN', 'RB', 'RBR', 'RBS', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ', 'WRB'])
    H_TAGS = set(['V', 'VM', 'VAUX', 'INTF', 'NEG', 'QT', 'QTC', 'QTF', 'QTO'])

    count = 0
    lines = []
    for obj in db.lines.find({}):  # {"_id" : ObjectId("575ca51699eb7b1c9bee02a9")}
        line = obj['line']
        if obj.get('status', None) == 'done':
            print 'Skipping...'
            continue
        lines.append((obj['_id'], line))
    for _id, line in lines:
        for k, v in emoticons().iteritems():
            if k == line or k in line:
                line = line.replace(k, v)
        for p in ",.><?/+=-_}{[]*&^%$#@!~`\"\\|:;":
            line = line.replace(p, ' ')
        words = map(handle_word, [word for word in nltk.word_tokenize(line)])
        pos_s = dict(H=[], E=[])
        e_statement = ' '.join(u[2] if len(u[2]) > 0 and u[1] == 'S' else u[0] for u in words)
        h_statement = ' '.join(u[2] if len(u[2]) > 0 else u[0] for u in words)
        pos_s['E'] = tag_words_english(e_statement)
        pos_s[other_lang] = tag_words_hindi(h_statement)
        db.lines.update_one({'_id': _id}, {'$set': {'words': words, 'epos': pos_s['E'], 'opos': pos_s[other_lang], 'status': 'done'}}, upsert=False)


def assign_senti_scores():
    global pool
    print 'Assign Scores...'
    from language_identification import emoticons
    from pos_tag import tag_words_english, tag_words_hindi
    from sentiment import sentiment as stmt
    
    count = 0
    lines = []
    for obj in db.lines.find({}):  
        w, e, o = obj['words'], obj['epos'], obj['opos']
        if False and obj.get('status', None) == 'assigned':
            print 'Skipping...'
            continue
        lines.append((obj['_id'], w, e, o))
    count, total = 0, 0
    for _id, words, epos, opos in lines:
        print _id
        scores = []
        if len(epos) != len(opos):
            continue

        index = 0
        complete_tag = []
        for i in xrange(len(epos)):
            word, tag = epos[i]
            oword, otag1, otag2 = opos[i]
            for x in xrange(index, len(words)):
                if words[x][0] == word:
                    if words[x][1] == 'O':
                        complete_tag.append((oword, 'O', (otag1, otag2)))
                    else:
                        complete_tag.append((word, 'E', tag))
                    break

        scores = [(word, lang, tag, stmt((word, tag), lang) if lang in ['E', 'S'] else stmt((word, tag[0], tag[1]), 'H')) for (word, lang, tag) in complete_tag]
        for score in scores:
            if score[3][0] > 0. or score[3][1] > 0.:
                print '\t', score[0], score[2], score[3]
            else:
                count += 1
            total += 1
        db.lines.update_one({'_id': _id}, {'$set': {'pos_tags': complete_tag, 'sores': scores, 'status': 'assigned'}}, upsert=False)
    print total, count


def collect_words():
    print 'Collect words...'
    from sentiment import sentiment as stmt
    count = 0
    lines = []
    for obj in db.lines.find({}):
        scores = obj.get('sores', [])
        lines.append((obj['_id'], scores))
    db.words.remove({}) 
    for _id, scores in lines:
        words = [(word, lang, stmt((word, tag[0], tag[1]), 'H')) for (word, lang, tag, polarity) in scores if lang == 'O']
        for word in words:
            print [word[0]], word[2][0], word[2][1]
            db.words.insert({'word': word[0], 'lang': word[1], 'polarity': word[2]})

def generate_features():
    lines = []
    db.features.remove({}) 
    for obj in db.lines.find({}):
        scores = obj.get('sores', [])
        words = [(word, polarity[0], polarity[1], scores[i - 1][0] if i > 0 else '') for i, (word, lang, tag, polarity) in enumerate(scores)]
        output = obj['output']
        db.features.insert({'input': words, 'output': output}) 

def handle_word(word):
    from wordnet import word_synset
    from language_identification import identify, emoticons
    if len(word) == 0:
        return (word, '', '')
    if word in ",.><?/+=-_}{[]*&^%$#@!~`\"\\|:;":
        return word, '', '' 
    u, v, w = identify(word)
    if len(u) is 0 and (len(w) is 0 or all(len(w_) is 0 for w_ in w)):
        return (word, '', '')
    if v == 'S' and len(w) > 0 and len(w[0]) > 0:
        return u, v, w[0]
    elif v == 'O' and len(w) > 0:
        consider = []
        for _w in w:
            synsets = word_synset(_w, v)
            if synsets and len(synsets) > 0:
                consider.append(_w)
        if len(consider) is 0:
            w = w[0]
        else:
            w = consider[0]
    else:
        w = ''
    if isinstance(w, list) and len(w) is 0:
        w = ''
    return (u, v, w)


def train_test():
    data = []
    for obj in db.features.find({}):
        _input = obj['input']
        _output = obj['output']
        data.append((_input, _output))
    accuracy_average = 0
    accuracy_total = 0

    for tp in xrange(20, 100, 5):
        train_percent = tp / 100.
        for i in xrange(1):
            random.shuffle(data)
            train_data = []
            train_labels = []
            test_data = []
            test_labels = []
            summation_accuracy = 0.
            for _input, _output in data:
                if len(_input) is 0:
                    continue
                __d = {
                }
                pscore =  0.
                nscore = 0.
                sentence = ''
                for w, p, n, pr in _input:
                    sentence += ' ' + w
                    if w not in __d:
                        __d[w] = 0
                    __d[w] += 1
                    if pr not in __d:
                        __d[pr] = 0
                    pscore += p
                    nscore += -1 * n
                __d['sentence'] = sentence.strip() 
                #__d['pscore'] = pscore * 1. / len(_input)
                #__d['nscore'] = nscore * 1. / len(_input)
                __d['score'] = pscore + nscore
                summation = __d['score']  # __d['pscore'] + __d['nscore']
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
        
            print "Results for LinearSVC With Training Percent", train_percent, 'with accuracy', accuracy, (accuracy / len(prediction_liblinear)), '', 'out of', len(prediction_liblinear)
            accuracy_average += accuracy 
            accuracy_total += len(prediction_liblinear)
            #print("Training time: %fs; Prediction time: %fs" % (time_liblinear_train, time_liblinear_predict))
            #print(classification_report(test_labels, prediction_liblinear))
    print 'Average Improvements',  (accuracy_average / accuracy_total)


if __name__ == '__main__':
    load_seed()
    start_tagging()
    assign_senti_scores()
    generate_features()
    train_test()
