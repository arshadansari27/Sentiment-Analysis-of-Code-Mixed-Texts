import pymongo
import nltk
import sys
#from ..language_identification import emoticons
sys.path.append('..')
from wordnet import word_synset
from language_identification import identify, emoticons
from pos_tag import tag_words_hindi, tag_words_english
db = pymongo.MongoClient().sentiment_analysis_db

HOME = '/home/arshad/workspace/rest/sentiment-analysis'

E_TAGS = set(['JJ', 'JJR', 'JJS', 'IN', 'RB', 'RBR', 'RBS', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ', 'WRB'])
H_TAGS = set(['V', 'VM', 'VAUX', 'INTF', 'NEG', 'QT', 'QTC', 'QTF', 'QTO'])

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
        e_statement = ' '.join(u[2] if len(u[2]) > 0 and u[1] == 'S' else u[0] for u in words)
        h_statement = ' '.join(u[2] if len(u[2]) > 0 else u[0] for u in words)
        pos_h = tag_words_hindi(h_statement)
        pos_e = [(u, v, v) for u, v in  tag_words_english(e_statement)]
        pos = []
        pos.extend(pos_h)
        pos.extend(pos_e)
        db[db_name_pos].insert({'pos': pos, 'output': output})

if __name__ == '__main__':
    pos_tag('li_hindi_mix_db', 'pos_merged_hindi_mix_db')
    pos_tag('li_hindi_db', 'pos_merged_hindi_db')
