import pymongo
import nltk
import sys
#from ..language_identification import emoticons
sys.path.append('..')
from wordnet import word_synset
from language_identification import identify, emoticons
db = pymongo.MongoClient().sentiment_analysis_db

HOME = '/home/arshad/workspace/rest/sentiment-analysis'


def handle_word(lang='H'):
    def _handle_word(word):
        if len(word) == 0:
            return (word, '', '')
        if word in ",.><?/+=-_}{[]*&^%$#@!~`\"\\|:;":
            return word, '', '' 
        u, v, w = identify(word, lang)
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
    return _handle_word


def language_identify(db_name_csv, db_name_li, lang='H'):
    db[db_name_li].drop()
    count = 0
    for doc in db[db_name_csv].find({}):
        if not doc:
            continue
        output = doc['output']
        line  = doc['line']
        count += 1
        if not line or len(line) is 0:
            continue
        if count % 10 is 0: 
            print count
        for k, v in emoticons().iteritems():
            if k == line or k in line:
                line = line.replace(k, v)
        for p in ",.><?/+=-_}{[]*&^%$#@!~`\"\\|:;":
            line = line.replace(p, ' ')
        words = map(handle_word(lang), [word for word in nltk.word_tokenize(line)])
        db[db_name_li].insert({'words': words, 'output': output})

if __name__ == '__main__':
    language_identify('csv_hindi_db', 'li_hindi_db')
    language_identify('csv_hindi_mix_db', 'li_hindi_mix_db')
    language_identify('csv_marathi_db', 'li_marathi_db', lang='M')


