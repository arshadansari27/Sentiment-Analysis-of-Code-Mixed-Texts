import requests, simplejson as json, os
from collections import defaultdict
from main import HOME
from wordnet import word_synset
import atexit

import pymongo

db = pymongo.MongoClient().sentiment_analysis_db

TRANSLITERATED_DAT = 'transliterated.data'


def get_by_key(text, lang):
    doc = db.google_transliterate.find_one({'_id': '%s|%s' % (lang, text)})
    if not doc:
        return None
    return doc['value']

def set_by_key(text, lang, value):
    db.google_transliterate.update_one({'_id': '%s|%s' % (lang, text)}, {'$set': {'value': value}}, upsert=True)

# atexit.register(write_to_file_known_transliterations)

hindi_dictionary = defaultdict(set)

f = '%s/resources/Output/all-words-pairs.txt' % HOME
for line in open(f):
    line = line.strip()
    e, h = line.split('\t')
    e, h = e.strip().lower(), h.strip()
    hindi_dictionary[e].add(h.decode('utf-8'))

def load_csv(fname):
    lines = []
    for line in open(fname):
        line = line.strip()
        w, x, y, z = line.split('|')
        lines.append((w, x, y, z))
    return lines


for line in open('%s/resources/crowd_transliterations.hi-en.txt' % HOME):
    line = line.strip()
    vals = line.split('\t')
    if len(vals) < 2:
        continue
    x, y = vals[0], vals[1]
    hindi_dictionary[x.lower()].add(y.decode('utf-8'))


for line in load_csv('%s/resources/en-hi.csv' % HOME):
    w, x, y, z = line
    hindi_dictionary[w.lower()].add(x.decode('utf-8'))
    hindi_dictionary[y.lower()].add(x.decode('utf-8'))
    hindi_dictionary[z.lower()].add(x.decode('utf-8'))

for line in load_csv('%s/resources/hi-en.csv' % HOME):
    x, w, y, z = line
    hindi_dictionary[w.lower()].add(x.decode('utf-8'))
    hindi_dictionary[y.lower()].add(x.decode('utf-8'))
    hindi_dictionary[z.lower()].add(x.decode('utf-8'))

marathi_dictionary = defaultdict(set)
for line in load_csv('%s/resources/en-mr.csv' % HOME):
    w, x, y, z = line
    marathi_dictionary[w.lower()].add(x.decode('utf-8'))
    marathi_dictionary[y.lower()].add(x.decode('utf-8'))
    marathi_dictionary[z.lower()].add(x.decode('utf-8'))

for line in load_csv('%s/resources/mr-en.csv' % HOME):
    x, w, y, z = line
    marathi_dictionary[w.lower()].add(x.decode('utf-8'))
    marathi_dictionary[y.lower()].add(x.decode('utf-8'))
    marathi_dictionary[z.lower()].add(x.decode('utf-8'))

def transliterate(text, lang='H'):
    for p in ",.><?/+=-_}{[]*&^%$#@!~`\"\\|:;()":
        text = text.replace(p, '')
    if text in ",.><?/+=-_}{[]*&^%$#@!~`\"\\|:;()":
        return []
    dict_to_use = hindi_dictionary if lang == 'H' else marathi_dictionary
    tr = list(dict_to_use.get(text.lower(), []))
    if not tr:
        tr = google_transliterate(text, lang)
    return tr


def get_and_check_synsets(tr, lang='H'):
    if tr and len(tr) > 0:
        ntr = [(_tr, word_synset(_tr, lang=lang)) for _tr in tr]
        if not ntr or len(ntr) is 0:
            ntr = [(_tr, None) for _tr in tr]
        return ntr
    else:
        return None


count = 0

def google_transliterate(text, lang='H'):
    global count
    '''
    if hindi is false, marathi is chosen
    '''
    if not text or len(text) is 0:
        return []
    val = get_by_key(text, lang)
    if val:
        return val
    
    olang = 'hi' if lang == 'H' else 'mr'
    url = 'http://www.google.com/inputtools/request?text=%s&ime=transliteration_en_%s&num=10&cp=0&cs=0&ie=utf-8&oe=utf-8&app=jsapi'
    '''
    '''
    try:
        _text = text.replace(' ', ',')
        response = requests.get(url % (_text, olang))
        print 'GETTING FROM GOOGLE', text, '...', olang
        jresponse = json.loads(response.text)
    except:
        jresponse = ['Failed']
    if jresponse[0] == 'SUCCESS':
        transliterations = jresponse[1][0][1]
    else:
        transliterations = []
    set_by_key(text, lang, transliterations)
    return transliterations
