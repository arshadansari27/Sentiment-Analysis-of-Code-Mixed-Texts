import pymongo
import nltk
import sys
#from ..language_identification import emoticons
sys.path.append('..')
from wordnet import word_synset
from language_identification import identify, emoticons
from pos_tag import tag_words_hindi
from sentiment import english_sentiment, hindi_sentiment
db = pymongo.MongoClient().sentiment_analysis_db

HOME = '/home/arshad/workspace/rest/sentiment-analysis'


def sentiscores(db_name_pos, db_name_ss):
    db[db_name_ss].drop()
    count = 0
    for doc in db[db_name_pos].find({}):
        if not doc:
            continue
        output = doc['output']
        words = doc['pos']
        count += 1
        if not words or len(words) is 0:
            continue
        if count % 10 is 0: 
            print count
        scores = []
        for i in xrange(len(words)):
            word, tag1, tag2 = words[i]
            if (not tag1 or len(tag1) is 0) and (not tag2 or len(tag2) is 0):
                scores.append((word, 0., 0.))
                continue
            p_score, n_score = 0., 0.
            scores.append((word, p_score, n_score))
            e_p_score, e_n_score = english_sentiment(word, tag1.lower())
            h_p_score, h_n_score = hindi_sentiment(word, tag2.lower())
            m_p_score, m_n_score = 0., 0.
            score_point = 0
            if e_p_score > 0. or e_n_score > 0.:
                score_point += 1
                p_score += e_p_score
                n_score += e_n_score
            if h_p_score > 0. or h_n_score > 0.:
                score_point += 1
                p_score += h_p_score
                n_score += h_n_score
            if m_p_score > 0. or m_n_score > 0.:
                score_point += 1
                p_score += m_p_score
                n_score += m_n_score
            if score_point > 0:
                p_score = p_score / score_point
                n_score = n_score / score_point

            scores.append((word, p_score, n_score))
        db[db_name_ss].insert({'words': scores, 'output': output})

def hindi_tag_to_num(wt):
    if 'nn' == wt:
        wt = 'n'
    elif wt == 'adj':
        wt = 'a'
    elif wt == 'adv':
        wt = 'r'
    else:
        wt = 'v'
    if wt == 'n':
        return '1'
    elif wt == 'v':
        return '2'
    elif wt == 'a':
        return '3'
    else:
        return '4'

if __name__ == '__main__':
    sentiscores('pos_hindi_db', 'ss_pos_hindi_db')
    sentiscores('pos_hindi_mix_db', 'ss_pos_hindi_mix_db')
    sentiscores('pos_merged_hindi_db', 'ss_pos_merged_hindi_db')
    sentiscores('pos_hindi_mix_db', 'ss_pos_merged_hindi_mix_db')
