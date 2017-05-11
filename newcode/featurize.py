from pymongo import MongoClient
from collections import defaultdict
from nltk.corpus import wordnet as wn
from transliteration import transliterate_word
import nltk
from nltk import word_tokenize
from nltk.util import ngrams as ngrams_creator


conn = MongoClient()
db = conn.sentiment_analysis_db
import pickle
path = 'files/hindi/'
word2Synset = pickle.load(open(path + "WordSynsetDict.pk"))

def replace_emoticon(word):
    smiley = db.smiley.find_one({'word': word})
    if smiley:
        return smiley['text']
    return word

def is_slang(word):
    slang = db.slang.find_one({'word': word})
    if slang:
        return slang['pos'], slang['neg']
    else:
        return False

def get_ngrams(text):
    ngrams = {}
    token=nltk.word_tokenize(text)
    for i in range(1, 5) :
        ngrams[i] = list(ngrams_creator(token, i))
    return ngrams

def get_other_dictionary(lang='H'):
    return db.hindi_dictionary if lang == 'H' else db.marathi_dictionary

def english_sentiment(word):
    pscore = 0
    nscore = 0
    for tag in ['n', 'r', 'v', 'a']:
        try:
            z = list(swn.senti_synsets(word, tag))
            if len(z) > 0:
                p, n = z[0].pos_score(), z[0].neg_score()
                pscore+=p
                nscore+=n
        except:
            pass
    return pscore, nscore



def identify(text, lang='H'):
    text = ' '.join([replace_emoticon(u) for u in text.split(' ')])
    ngrams = get_ngrams(text)
    slangs = {}
    other = {}
    english = {}
    for i in xrange(4, 0, -1):
        ngram = ngrams[i]
        for word_set in ngram:
            ntext = ' '.join(word_set)
            for p in ",.><?/+=-_}{[]*&^%$#@!~`\"\\|:;()":
                ntext = ntext.replace(p, '')
            # print ntext
            slang_check = is_slang(ntext.lower())
            if slang_check:
                slangs[ntext] = slang_check[0], slang_check[1]

            # ntext = handle_slang_words(ntext)
            transliterations = transliterate_word(ntext)
            check_hswn_words = []
            for other_word in transliterations:
                if len(other_word.split(u' ')) < len(ntext.split(' ')):
                    continue
                if lang == 'M':
                    mar_other = db.bilingual_dictionary_mr_hi.find_one({'word': other_word})
                    if mar_other:
                        check_hswn_words.extend(mar_other['dict'])
                else:
                    check_hswn_words.append(other_word)
            for hswn_word in check_hswn_words:
                if word2Synset.has_key(hswn_word):
                    synsets = word2Synset[hswn_word]
                    hswn_found = False
                    for pos_tag in synsets.keys():
                        synset = synsets[pos_tag]
                        hswn_value = db.hswn.find_one({'_id': synset})
                        if hswn_value:
                            hswn_found = True
                            for k in hswn_value.keys():
                                if k == '_id': continue
                                other[hswn_word] = hswn_value[k][0], hswn_value[k][1]
                    if not hswn_found:
                        other[ntext] = 0., 0., hswn_word


            synsets = wn.synsets(ntext)
            if synsets:
                eng_scores = english_sentiment(ntext)
                if eng_scores:
                    english[ntext] = eng_scores[0], eng_scores[1]
    return slangs, other, english



def handle_slang_words(w):
    if w == 'h':
        return 'hai'
    elif w == 'n':
        return 'na'
    elif w == 'da':
        return 'the'
    elif w == 'wid':
        return 'with'
    elif w == 'pr':
        return 'par'
    elif w == 'mattt':
        return 'mat'
    elif w == 'vo':
        return 'woh'
    elif w == 'ki':
        return 'kee'
    elif w == 'ap':
        return 'aap'
    elif w == 'bs':
        return 'bas'
    elif w == 'goood':
        return 'very good'
    elif w == 'tera':
        return 'teraa'
    elif w == 'cnfsn':
        return 'confusion'
    elif w == 'ka':
        return 'kaa'
    elif w == 'thts':
        return 'thats'
    elif w == 'cald':
        return 'called'
    elif w == 'tabhe':
        return 'tabhi'
    elif w == 'pta':
        return 'pata'
    elif w == 'b':
        return 'bhi'
    elif w == 'nai':
        return 'nahi'
    elif w == 'f':
        return 'of'
    elif w == 'd':
        return 'the'
    else:
        return w

def feature_generation(text, language):
    slangs, other, english  = identify(text, 'H')
    features = []
    for s, val in slangs.items():
        if not val[0]:
            val = 0, val[1]
        if not val[1]:
            val = val[0], 0
        p, n = float(val[0]), float(val[1])
        p, n = p / (p + n) if (p + n) > 0. else 0., n / (p + n) if (p + n) > 0. else 0.
        features.append((s, 'slang', p, n))

    for s, val in other.items():
        features.append((s, 'english', val[0], val[1]))

    for s, val in english.items():
        features.append((s, 'hindi', val[0], val[1]))

    return features

if __name__ == '__main__':
    print 'Beginning script.....'
    texts = [
            'Yeh dil mange more. I would love this. Kya baat hai jaane man',
            'Bahot bakwas thi movie. I cannot bear it']
    for text in texts:
        print '*' * 100
        print text
        f = feature_generation(text, 'H')
        for i in f:
            print i
