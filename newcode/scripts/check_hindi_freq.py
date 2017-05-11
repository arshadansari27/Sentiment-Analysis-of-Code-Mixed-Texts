from pymongo import MongoClient
from collections import defaultdict
from sanscript import transliterate, HK, DEVANAGARI
from utils import strip_non_ascii
from Levenshtein import distance
import fuzzy
import sys

conn = MongoClient()
db = conn.sentiment_analysis_db

soundex = fuzzy.Soundex(4)

for line in open('../../resources/word-frequency-hindi.txt'):
    line = line.strip()
    word, freq = line.split('\t')
    word = word.decode('utf-8') # .replace('\0xef', '')
    found = db.hindi_dictionary.find_one({'word': word})
    if not found:
        transliterated = transliterate(word, DEVANAGARI, HK)
        transliterated = strip_non_ascii(transliterated)
        found = db.hindi_dictionary.find_one({'transliterated': transliterated})
        if not found:
            sound = soundex(transliterated)
            sounding_same = list(db.hindi_dictionary.find({'sound': sound}))
            if len(sounding_same) > 0:
                found = sorted([(i['word'], distance(word, i['word'])) for i in sounding_same], key=lambda x: x[1])[0][0]
        else:
            found = found['word']
    else:
        found = found['word']
    print word, found
