from nltk.stem.porter import PorterStemmer
import hindi_language_identification as hli
from espellcheck import spell
import main


stemmer = PorterStemmer()

RF = main.RESOURCE_FOLDER
print 'RESOURCE', RF

_u = open(RF + '/Output/english-dictionary.txt').readlines()
edict = set([v.strip() for v in _u if len(v.strip()) > 0])


def lookup(word):
    ew, ex, ey, ez = lookup_english(word)
    hw, hx, hy, hz = lookup_hindi(word)
    if ex == 'O':
        return hy, hx, hz
    elif ez < hz:
        return hy, hx, hz
    else:
        return ey, ex, ez


def lookup_english(word):
    try:
        if word in edict:
            return word, 'E', word, 1.
        stemmed = stemmer.stem(word)
        if stemmed in edict:
            return word, 'E', stemmed, 0.90
        corrected = spell.correct(word)
        if corrected in edict:
            return word, 'E', corrected, 0.85
        return word, 'O', word, 0.5
    except:
        return word, 'O', word, 0.3


def lookup_hindi(word):
    try:
        word, num = hli.transliterate(word)
        return word, 'H', word, num
    except Exception, e:
        print '[*] Lookup', str(e)
        return word, 'O', word, 0.4
