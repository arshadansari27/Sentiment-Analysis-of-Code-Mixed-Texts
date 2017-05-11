# -*- coding: utf-8 -*-

from collections import defaultdict
import requests, simplejson as json

hindi_dictionary = defaultdict(lambda: defaultdict(int))

def load_csv(fname):
    lines = []
    for line in open(fname):
        line = line.strip()
        w, x, y, z = line.split('|')
        lines.append((w, x, y, z))
    return lines


HOME = '/home/arshad/workspace/rest/sentiment-analysis'
f = '%s/resources/Output/all-words-pairs.txt' % HOME

for line in open(f):
    line = line.strip()
    if len(line) is 0:
        continue
    e, h = line.split('\t')
    e, h = e.strip().lower(), h.strip()
    hindi_dictionary[h.decode('utf-8')][e.replace('.', '')] += 1

for line in open('%s/resources/crowd_transliterations.hi-en.txt' % HOME):
    line = line.strip()
    vals = line.split('\t')
    if len(vals) < 2:
        continue
    x, y = vals[0], vals[1]
    hindi_dictionary[y.decode('utf-8')][x.lower().replace('.', '')] += 1

for line in load_csv('%s/resources/en-hi.csv' % HOME):
    w, x, y, z = line
    hindi_dictionary[x.decode('utf-8')][w.lower().replace('.', '')] += 1
    hindi_dictionary[x.decode('utf-8')][y.lower().replace('.', '')] += 1
    hindi_dictionary[x.decode('utf-8')][z.lower().replace('.', '')] += 1

for line in load_csv('%s/resources/hi-en.csv' % HOME):
    x, w, y, z = line
    hindi_dictionary[x.decode('utf-8')][w.lower().replace('.', '')] += 1
    hindi_dictionary[x.decode('utf-8')][y.lower().replace('.', '')] += 1
    hindi_dictionary[x.decode('utf-8')][z.lower().replace('.', '')] += 1

counts = defaultdict(int)
english_words = set([])
for ll in open(HOME + "/resources/Output/english-dictionary.txt"):
    ll = ll.strip()
    english_words.add(ll)

counts = defaultdict(int)
nhindi_dictionary = defaultdict(list)

for k, v in hindi_dictionary.iteritems():
    val = max(_v for _k, _v in v.iteritems())
    ll = [_k for _k, _v in v.iteritems() if _v >= val]
    if len(ll) is 0:
        nhindi_dictionary[k] = ''
    else:
        min_length = 999999999999999999999
        selected = 0
        for i, u in enumerate(ll):
            is_english = True if u in english_words else False
            if is_english:
                selected = i
                break
            else:
                if min_length > len(u):
                    min_length = len(u)
                    selected = i
    
        nhindi_dictionary[k] = ll[selected]
    counts[len(v)] += 1

hindi_dictionary = nhindi_dictionary
positives = '%s/resources/Positive.txt' % HOME
negatives = '%s/resources/Negetive.txt' % HOME

def get_best(w):
    if w in hindi_dictionary:
        return hindi_dictionary[w]
    else:
        return ''

def write_file(sign, words, file_id):
    joined = ' '.join(["%s" % get_best(word.replace(u'\u0964', '')) for word in words]).strip()
    if len(joined) is 0:
        return
    stmt = '%s|%s\n' % (sign, joined)
    file_id.write(stmt)

with open(HOME + '/resources/sentiment_input.txt', 'w') as outfile:
    for line in open(positives):
        line = line.strip().decode('utf-8')
        words = line.split(' ')
        write_file('positive', words, outfile)

    for line in open(positives):
        line = line.strip().decode('utf-8')
        words = line.split(' ')
        write_file('negetive', words, outfile)

