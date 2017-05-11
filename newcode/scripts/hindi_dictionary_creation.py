# -*- coding: utf-8 -*-

from pymongo import MongoClient
from collections import defaultdict
from sanscript import transliterate, HK, DEVANAGARI
from utils import strip_non_ascii
import fuzzy
import sys

conn = MongoClient()
db = conn.sentiment_analysis_db

import pickle
path = '../files/hindi/'
word2Synset = pickle.load(open(path + "WordSynsetDict.pk"))

# dmetaphone = fuzzy.DMetaphone()
soundex = fuzzy.Soundex(4)

print db.hindi_dictionary.drop_indexes()
print db.hindi_dictionary.remove({})

words = []

for word in word2Synset.keys():
    transliterated = strip_non_ascii(transliterate(word, DEVANAGARI, HK))
    synsets = []
    for vv in word2Synset[word].values():
        synsets.extend(vv)

    lower = transliterated.lower()
    sound = soundex(lower.decode('ascii', errors='ignore'))
    words.append({'word': word, 'synsets': synsets, 'transliteration': lower, 'sound': sound})
    if len(words) > 1000:
        db.hindi_dictionary.insert_many(words)
        words = []

if len(words) > 1000:
    db.hindi_dictionary.insert_many(words)

db.hindi_dictionary.ensure_index('word')
db.hindi_dictionary.ensure_index('transliteration')
db.hindi_dictionary.ensure_index('sound')
