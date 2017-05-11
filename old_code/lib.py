# -*- coding: utf-8 -*-
import simplejson as json
from collections import defaultdict
import time


PAIR_DICT = json.loads(open('resources/hed.json').read())
SPELL_DATA = json.loads(open('resources/spell.json').read())
RSPELL_DATA = json.loads(open('resources/espell.json').read())


class EnglishAlphabets(object):

    def __init__(self):
        vowels = open('resources/vowels.txt').read().strip()
        self.vowels = set([u.decode('utf-8') for u in vowels.split(',')
                       if len(u) > 0])
        consonants = open('resources/consonants.txt').read().strip()
        self.consonants = set([u.decode('utf-8')
                           for u in consonants.split(',') if len(u) > 0])

    def syllable_pairs(self, word):
        pair = []
        current = ''
        for w in word:
            w = w.lower()
            if w in self.consonants and len(current) > 0:
                if unicode('h') == w and len(current) > 0 \
                        and current[-1] in self.consonants:
                    current += w
                    continue
                pair.append(current)
                current = w
                continue
            current += w
        pair.append(current)
        return pair


class HindiAlphabets(object):

    def __init__(self):
        matra = open('resources/matra.txt').read().strip()
        self.matra = set([u.decode('utf-8') for u in matra.split(',')
                      if len(u) > 0])
        akshar = open('resources/akshar.txt').read().strip()
        self.akshar = set([u.decode('utf-8') for u in akshar.split(',')
                       if len(u) > 0])

    def syllable_pairs(self, word):
        characters = []
        current = []
        for i, w in enumerate(word):
            if w in self.akshar:
                characters.append(w)
            else:
                current.append(w)
                if i == len(word) - 1 or word[i + 1] in self.akshar:
                    characters.append(current)
                    current = []
        return characters


def load_spell():
    global SPELL_DATA
    SPELL_DATA = json.loads(open('resources/spell.json').read())


def get_transliterated(word):
    pairs = HindiAlphabets().syllable_pairs(word)
    words = []
    for pair in pairs:
        pair = ''.join(pair)
        options = SPELL_DATA.get(pair, [])
        if len(options) is 0:
            return u'UNKNOWN '
        option = sorted([(v, k) for k, v in options.iteritems()],
                        key=lambda u: u[0], reverse=True)[0]
        words.append(option[1])

    created_words = []
    temp_words = []
    for word in words:
        if len(created_words) is 0:
            temp_words.append(word)
        else:
            for created_word in created_words:
                temp_words.append(created_word + word)

        created_words = [u for u in temp_words]
        temp_words = []

    return created_words[0]


def get_all_syllabus(word, max_length):
    called = set([])
    all_syllabus = []

    def ngramtree(prev, current, next, max_length):
        args = tuple([tuple(sorted(prev)), current, next])
        if args in called:
            return
        called.add(args)
        if len(next) is 0:
            all_syllabus.append([u for u in prev] + [current])
            return
        max_length = 5 if len(next) > 5 else len(next)
        if current and len(current) > 0:
            nprev = [u for u in prev] + [current]
        else:
            nprev = [u for u in prev]
        for i in xrange(max_length):
            nnext = next[i + 1:]
            ncurrent = next[: i + 1]
            if max_length > 0 and len(nprev) > max_length and len(nnext) > 0:
                return
            ngramtree(nprev,  ncurrent, nnext, max_length)
    ngramtree([], '', word, max_length)
    return all_syllabus


def save_spell():
    data = defaultdict(lambda: defaultdict(int))
    print 'Total Words', len(PAIR_DICT)
    count = 0
    for key, values in PAIR_DICT.iteritems():
        count += 1
        if count % 1000 is 0:
            print '...', count
        eObj = EnglishAlphabets()
        hObj = HindiAlphabets()
        hindi_pairs = hObj.syllable_pairs(key)
        for value in values:
            all_syllables = get_all_syllabus(value, len(hindi_pairs))
            for english_pairs in all_syllables:
                if len(english_pairs) != len(hindi_pairs):
                    continue
                ll = len(english_pairs)
                i = 0
                while i < ll:
                    hp = ''.join(hindi_pairs[i])
                    ep = english_pairs[i]
                    i += 1
                    if ''.join(hp) not in hObj.akshar and ep[0] in eObj.consonants:
                        continue
                    if ''.join(hp) in hObj.akshar and ep[0] not in eObj.consonants:
                        continue
                    data[hp][ep] += 1
                    data[hp][ep] += 1


    newdata = defaultdict(lambda: defaultdict(int))
    max_count = 0
    for k, d in sorted([(ci, cj) for ci, cj in data.iteritems()]):
        sorted_d = sorted([(dv, dk) for dk, dv in d.iteritems()], reverse=True)
        if len(sorted_d) < 4:
            threshold = min(u[0] for u in sorted_d)
        else:
            threshold = sum([u[0] for u in sorted_d])/len(sorted_d)
        max_count = max(max(u[0] for u in sorted_d), max_count)
        sorted_d = [u for u in sorted_d if u[0] > threshold][:5]
        newdata[k] = sorted_d
    with open('resources/spell.json', 'w') as _f:
        _f.write(json.dumps(newdata))
    print max_count


def show_stuff():
    data = json.loads(open('resources/spell.json').read())
    for k, d in sorted([(ci, cj) for ci, cj in data.iteritems()]):
        print k
        s = sum(x[0] for x in d)
        for sort_d in d:
            print '\t', sort_d[1], "%3.2f" % (sort_d[0] * 100./s)

def reverse_spell():
    data = json.loads(open('resources/spell.json').read())
    newdata = defaultdict(lambda: defaultdict(int))
    for k, d in sorted([(ci, cj) for ci, cj in data.iteritems()]):
        for sort_d in d:
            newdata[sort_d[1]][k] += sort_d[0]
    with open('resources/espell.json', 'w') as _f:
        _f.write(json.dumps(newdata))
    data = json.loads(open('resources/espell.json').read())
    for k, d in sorted([(ci, cj) for ci, cj in data.iteritems()]):
        print k
        s = sum(y for y in d.values())
        for sort_k, sort_v in d.iteritems():
            print '\t', sort_k, "%3.2f" % (sort_v * 100./s)





if __name__ == '__main__':
    start = time.clock()
    # save_spell()
    # show_stuff()
    # reverse_spell()
    b = "chalaki"
    all_syllables = get_all_syllabus(b, 0)
    for syllables in all_syllables:
        word = []
        for char in syllables:
            options = sorted([(v, k) for k, v in RSPELL_DATA.get(char, {}).iteritems()], reverse=True)
            if len(options) is 0:
                continue
            option = options[0][1]
            word.append(option)
        print ','.join(syllables), word, ''.join(word)







    print 'Time taken:', time.clock() - start
    '''
    e, h = 'khushboo', u'खुशबू'
    pairs = HindiAlphabets().syllable_pairs(h)
    for p in pairs:
        print p
    '''
