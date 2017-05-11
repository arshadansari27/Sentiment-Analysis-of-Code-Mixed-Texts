# -*- coding: utf-8 -*-

        print "Word -->", "खाना "
from pymongo import MongoClient
from collections import defaultdict
import sys

conn = MongoClient()
db = conn.sentiment_analysis_db

print "Removing", db.hswn.remove({})

import pickle
path = '../files/hindi/'
word2Synset = pickle.load(open(path + "WordSynsetDict.pk"))
synset2Onto = pickle.load(open(path + "SynsetOnto.pk"))
synonyms = pickle.load(open(path + "SynsetWords.pk"))
synset2Gloss = pickle.load(open(path + "SynsetGloss.pk"))
synset2Hypernyms = pickle.load(open(path + "SynsetHypernym.pk"))
synset2Hyponyms = pickle.load(open(path + "SynsetHyponym.pk"))
synset2Hypernyms = pickle.load(open(path + "SynsetHypernym.pk"))

'''
while True:
    if word2Synset.has_key(word):
        synsets = word2Synset[word]
        print "Word -->", "खाना "
        for pos in synsets.keys():
            print "POS Category -->", pos
            for synset in synsets[pos]:
                print "\t\tSynset -->", synset
                if synonyms.has_key(synset):
                    print "\t\t\t Synonyms -->", synonyms[synset]
                if synset2Gloss.has_key(synset):
                    print "\t\t\t Synset Gloss", synset2Gloss[synset]
                if synset2Onto.has_key(synset):
                    print "\t\t\t Ontological Categories", synset2Onto[synset]
                if synset2Hypernyms.has_key(synset):
                    print "\t\t\t Hypernym Synsets", synset2Hypernyms[synset]
                if synset2Hyponyms.has_key(synset):
                    print "\t\t\t Hyponym Synsets", synset2Hyponyms[synset]
    word = raw_input("Enter a word: ").decode("utf-8", "ignore")

db.csv_input_all.insert({
        'line': obj['line'],
        'output': obj['output'],
        'lang': 'M'
    }

'''

Sentiments = {}

for line in open('../../resources/hswn_wn.txt'):
    words = line.split(' ')
    tag = words[0]
    syn = words[1]

    pos = words[2]
    neg = words[3]
    other = [u.strip() for u in words[4].split(',')]

    if not Sentiments.has_key(syn):
        Sentiments[syn] = {}
    if not Sentiments[syn].has_key(tag):
        Sentiments[syn][tag] = {'pos': [pos], 'neg': [neg]}
    else:
        Sentiments[syn][tag]['pos'].append(pos)
        Sentiments[syn][tag]['neg'].append(neg)

    if len(other) is not 0:
        for o in other:
            _o = o.decode('utf8')
            if word2Synset.has_key(_o):
                o_synsets = word2Synset[_o]
                for o_tag in o_synsets.keys():
                    r_o_tag = ['n', 'a', 'v', 'r'][int(o_tag) - 1]
                    for o_syn in o_synsets[o_tag]:
                        if not Sentiments.has_key(o_syn):
                            Sentiments[o_syn] = {}
                        if not Sentiments[o_syn].has_key(r_o_tag):
                            Sentiments[o_syn][r_o_tag] = {
                                'pos': [pos], 'neg': [neg]
                            }
                        else:
                            Sentiments[o_syn][r_o_tag]['pos'].append(pos)
                            Sentiments[o_syn][r_o_tag]['neg'].append(neg)

for syn, tags in Sentiments.iteritems():
    value = {
        '_id': syn
    }
    for tag in tags.keys():
        value[tag] = [max(tags[tag]['pos']), max(tags[tag]['neg'])]
    db.hswn.insert(value)
