import pymongo
import nltk
import sys
#from ..language_identification import emoticons
sys.path.append('..')
from wordnet import word_synset
from language_identification import identify, emoticons
from pos_tag import tag_words_hindi
from sentiment import english_sentiments, hindi_sentiments
db = pymongo.MongoClient().sentiment_analysis_db

HOME = '/home/arshad/workspace/rest/sentiment-analysis'


def sentiscores(db_name_li, db_name_ss):
    db[db_name_ss].drop()
    count = 0
    for doc in db[db_name_li].find({}):
        if not doc:
            continue
        output = doc['output']
        words = doc['words']
        count += 1
        if not words or len(words) is 0:
            continue
        if count % 10 is 0: 
            print count
        scores = []
        for i in xrange(len(words)):
            word, lang, other_word  = words[i]
            p_score, n_score = 0., 0.
            if lang == 'E':
                p_score, n_score = english_sentiments(word)
            elif lang == 'S':
                if ' ' in word:
                    ww = word.split(' ')
                    for w in ww:
                        ps, ns = english_sentiments(w)
                        p_score += ps
                        n_score += ns
                    p_score = p_score / len(ww)
                    n_score = n_score / len(ww)
                else:
                    p_score, n_score = english_sentiments(word)
            elif lang == 'H':
                p_score, n_score = hindi_sentiment(word.decode('utf-8'))
            else:
                p_score, n_score = 0., 0.
            scores.append((word, p_score, n_score))
        db[db_name_ss].insert({'words': scores, 'output': output})

if __name__ == '__main__':
    sentiscores('li_hindi_db', 'ss_li_hindi_db')
    sentiscores('li_hindi_mix_db', 'ss_li_hindi_mix_db')
    sentiscores('li_marathi_db', 'ss_li_marathi_db')
