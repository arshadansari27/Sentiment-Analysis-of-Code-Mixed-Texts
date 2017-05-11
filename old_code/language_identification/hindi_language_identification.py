from sanscript import transliterate as _transliterate, HK, DEVANAGARI
import pycrfsuite
import main
import simplejson as json
from espellcheck import hspell
from substring_combo import esplitclusters


nsuffixes = json.loads(
    open(main.RESOURCE_FOLDER + '/hindi_stemming_code.json').read())
suffixes = {}
for k, v in nsuffixes.iteritems():
        suffixes[int(k)] = [u for u in v]

MFILE = main.RESOURCE_FOLDER + '/transliteration.crfsuite'
tagger = pycrfsuite.Tagger()
tagger.open(MFILE)


def hi_stem(word):
    for L in 5, 4, 3, 2, 1:
        if len(word) > L + 1:
            for suf in suffixes[L]:
                if word.endswith(suf):
                    return word[:-L]
    return word


HINDI_DICTIONARY = set(
    [u.strip().decode('utf-8') for u in open(
        main.RESOURCE_FOLDER + '/hindi-word-list.txt'
    ).readlines() if len(u.strip()) > 0]
)
WORD_PAIRS = {}

for u in open(main.RESOURCE_FOLDER + '/Output/wordpairs.txt').readlines():
    u = u.strip()
    if len(u) is 0:
        continue
    i = u.index(':')
    eng = u[:i].strip()
    hin = u[i + 1:].strip()
    WORD_PAIRS[eng] = hin.decode('utf-8')


def dict_check(hword):
    if hword in HINDI_DICTIONARY:
        return True
    try:
        if hword in HINDI_DICTIONARY:
            return True
    except Exception, e:
        print 'dict_check', str(e)
    return False


def try_variations(hword):
    if dict_check(hword):
        return (hword, 1.)
    try:
        hw = hi_stem(hword)
        if dict_check(hw):
            return (hword, 0.95)
    except Exception, e:
        pass
    try:
        hs = hspell.correct(hword.encode('utf-8')).decode('utf-8')
        if dict_check(hs):
            return hword, 0.99
    except Exception, e:
        pass
    return hword, 0.7


def transliterate(word):
    if word in WORD_PAIRS:
        return WORD_PAIRS[word], 1.0

    intermediate = ''.join(tagger.tag(
        [u for u in esplitclusters(word)]))

    words = [word, intermediate]
    u, n = None, 0
    for w in words:
        tr = _transliterate(w, HK, DEVANAGARI)
        _u, _n = try_variations(tr)
        if n < _n:
            u = _u
            n = _n
    return u, n
