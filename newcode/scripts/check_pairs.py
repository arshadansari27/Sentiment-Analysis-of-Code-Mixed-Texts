# -*- coding: utf-8 -*-

from pymongo import MongoClient
from collections import defaultdict
import sys

conn = MongoClient()
db = conn.sentiment_analysis_db

import pickle
path = '../files/hindi/'
word2Synset = pickle.load(open(path + "WordSynsetDict.pk"))
# synset2Onto = pickle.load(open(path + "SynsetOnto.pk"))
# synonyms = pickle.load(open(path + "SynsetWords.pk"))
# synset2Gloss = pickle.load(open(path + "SynsetGloss.pk"))
# synset2Hypernyms = pickle.load(open(path + "SynsetHypernym.pk"))
# synset2Hyponyms = pickle.load(open(path + "SynsetHyponym.pk"))
# synset2Hypernyms = pickle.load(open(path + "SynsetHypernym.pk"))

total, notfound = 0, 0
for line in open('../../resources/transliteration-pairs-hi-en.txt'):
    total += 1
    tword, hword = line.strip().split('\t')
    if word2Synset.has_key(hword.decode('iso-8859-1').encode('utf-8')):
        print tword
    else:
        notfound += 1

print total, notfound

