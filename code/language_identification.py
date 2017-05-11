from collections import defaultdict
from wordnet import word_synset
from transliteration import transliterate


_slang_dictionary = {}
_top_english = set([])
_top_other = dict(H=set([]), M=set([]))


def top_other_words(oword, lang='H'):
    from main import HOME
    # TODO: Use this to select marathi file
    # TODO: Change this to use word frequency for better results, use quantiles
    ff = "/resources/Output/hindiwords.txt" if lang == 'H' else '/resources/hindi-1000-words.txt'
    if len(_top_other[lang]) is 0:
        for ll in open(HOME + ff):
            ll = ll.strip().decode('utf-8') 
            _top_other[lang].add(ll)
    return oword if oword in _top_other[lang] else None


def top_english_words(word):
    from main import HOME
    # TODO: Change this to use word frequency for better results, use quantiles
    if len(_top_english) is 0:
        for ll in open(HOME + "/resources/Output/english-dictionary.txt"):
            ll = ll.strip()
            _top_english.add(ll)
    return word in _top_english 


def slang_dictionary():
    from main import HOME
    if len(_slang_dictionary) is 0:
        for ll in open(HOME + "/resources/slang_dictionary.csv"):
            ll = [l.strip() for l in ll.strip().split('|')]
            key, val = ll[0], ll[1]
            _slang_dictionary[key] = val
    return _slang_dictionary


_emoticons = {}
def emoticons():
    from main import HOME
    if len(_emoticons) is 0:
        for ll in open(HOME + "/resources/emoticons.txt"):
            ll = [l.strip() for l in ll.strip().split('\t')]
            key, val = ll[0], ll[1]
            _emoticons[key] = val
    return _emoticons

def identify(word, lang='H'):
    word = word.lower().replace(',', '').replace('.', '')
    english_probability     = 1.
    other_probability       = 1.
    slang_probability       = 1.

    word = handle_slang_words(word)

    # print '***', word, slang_dictionary()[word] if word in slang_dictionary() else False

    if word in slang_dictionary():
        slang_probability   *= 0.8
        english_probability *= 0.1
        other_probability   *= 0.1
    e_syn_set = word_synset(word)

    o_best_words = []
    o_words = transliterate(word, lang)
    # print o_words
    for ow in o_words:
        o_synsets = word_synset(ow, lang=lang)
        o_top_word = top_other_words(ow, lang)
        if o_synsets and len(o_synsets) > 0 and o_top_word:
            o_best_words.append((ow, o_synsets, True))
        elif o_synsets and len(o_synsets) > 0:
            o_best_words.append((ow, o_synsets, False))
        elif o_top_word:
            o_best_words.append((ow, None, None))

    if o_best_words and len(o_best_words) > 0:
        o_best_words = sorted(o_best_words, key=lambda item: len(item[1]) if item[1] else 0, reverse=True)


    if o_best_words and len(o_best_words) > 0:
        slang_probability   *= 0.30
        english_probability *= 0.30
        other_probability   *= 0.40
        if any(u[2] for u in o_best_words):
            slang_probability   *= 0.25
            english_probability *= 0.25
            other_probability   *= 0.5
        elif sum(1 for u in o_best_words if u[1] is not None) > 0:
            slang_probability   *= 0.30
            english_probability *= 0.30
            other_probability   *= 0.40
    
    if e_syn_set is not None:
        slang_probability   *= 0.30
        english_probability *= 0.40
        other_probability   *= 0.30
    if top_english_words(word):
        slang_probability   *= 0.15
        english_probability *= 0.7
        other_probability   *= 0.15
    if slang_probability > english_probability and slang_probability > other_probability:
        return word, 'S', [slang_dictionary()[word]]
    elif english_probability > other_probability:
        return word, 'E', []
    else:
        values = word, 'O', [u[0] for u in o_best_words]
        return values


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
        return 'good'
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

if __name__ == '__main__':
    print 'Beginning script.....'
    for line in open('lines.txt'):
        # words = ['Yeh', 'dil', 'maange', 'mange', 'more', 'now', 'lols', 'lol']
        line = line.strip()
        for word in line.split(' '):
            u, v, w = identify(word)
            print u, v
            print '\t', ','.join(w)
            print '---------------'
