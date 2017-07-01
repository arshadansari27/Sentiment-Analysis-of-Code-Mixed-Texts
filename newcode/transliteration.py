import os
from collections import defaultdict
from sanscript import transliterate, HK, DEVANAGARI
from utils import strip_non_ascii
from Levenshtein import distance
import fuzzy, requests, simplejson as json

import pymongo

db = pymongo.MongoClient().sentiment_analysis_db

hindi_dictionary = db.hindi_dictionary
marathi_dictionary = db.marathi_dictionary

soundex = fuzzy.Soundex(4)

def transliterate_word(text, lang='H'):
    for p in ",.><?/+=-_}{[]*&^%$#@!~`\"\\|:;()":
        text = text.replace(p, '')
    if text in ",.><?/+=-_}{[]*&^%$#@!~`\"\\|:;()":
        return []
    text = text.encode('utf-8')
    dict_to_use = hindi_dictionary if lang == 'H' else marathi_dictionary

    found_direct = False

    immediate_tranlisteration = transliterate(text, HK, DEVANAGARI)
    attempt = list(dict_to_use.find({'word': immediate_tranlisteration}))
    if attempt:
        return [attempt[0]['word']]

    attempt = list(dict_to_use.find({'transliterated': {'$in': [text, text.lower()]}}))
    if attempt:
        return [attempt[0]['word']]

    google_transliteration = google_transliterate(text, lang)
    for tr in google_transliteration:
        ll = list(dict_to_use.find({'word': tr}))
        if ll and len(ll) > 0:
            return [li['word'] for li in ll]

    sound = soundex(text)
    attempt = list(dict_to_use.find({'sound': sound}))
    neighbors = sorted([(i['word'], distance(text, i['transliteration'])) for i in attempt], key=lambda x: x[1])
    return [u[0] for u in neighbors if u[1] < 3]

def get_by_key(text, lang):
    doc = db.google_transliterate.find_one({'_id': '%s|%s' % (lang, text)})
    if not doc:
        return None
    return doc['value']

def set_by_key(text, lang, value):
    db.google_transliterate.update_one({'_id': '%s|%s' % (lang, text)}, {'$set': {'value': value}}, upsert=True)

def google_transliterate(text, lang='H'):
    val = get_by_key(text, lang)
    if val:
        return val
    olang = 'hi' if lang == 'H' else 'mr'
    url = 'http://www.google.com/inputtools/request?text=%s&ime=transliteration_en_%s&num=10&cp=0&cs=0&ie=utf-8&oe=utf-8&app=jsapi'
    try:
        _text = text.replace(' ', ',')
        url = url % (_text, olang)
        response = requests.get(url)
        jresponse = json.loads(response.text)
    except:
        jresponse = ['Failed']
    if jresponse[0] == 'SUCCESS':
        transliterations = jresponse[1][0][1]
    else:
        transliterations = []
    set_by_key(text, lang, transliterations)
    return transliterations

if __name__ == '__main__':
    from bson import ObjectId # '_id': ObjectId('58f751471d41c821034ad783')
    texts = [(u['_id'], u['line'], u['lang']) for u in db.csv_input_all.find({})]
    total = len(texts)
    count = 0
    for _id, text, lang in texts:
        count += 1.
        if db.csv_input_all_tested.find_one({'_id': _id}):
            continue
        for word in text.split(' '):
            print(word, ','.join(transliterate_word(word.decode("utf-8"), lang)))
        print('\n')
        db.csv_input_all_tested.insert({'_id': _id})
