import pymongo
import nltk
import sys
#from ..language_identification import emoticons
sys.path.append('..')
from wordnet import word_synset
from language_identification import identify, emoticons
from pos_tag import tag_words_hindi
db = pymongo.MongoClient().sentiment_analysis_db

HOME = '/home/arshad/workspace/rest/sentiment-analysis'


def pos_tag(db_name_li, db_name_pos):
    db[db_name_pos].drop()
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
        statement = ' '.join(u[2] if len(u[2]) > 0 else u[0] for u in words)
        pos = tag_words_hindi(statement)
        db[db_name_pos].insert({'pos': pos, 'output': output})

if __name__ == '__main__':
    pos_tag('li_hindi_db', 'pos_hindi_db')
    pos_tag('li_hindi_mix_db', 'pos_hindi_mix_db')
