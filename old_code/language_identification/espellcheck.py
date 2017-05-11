# -*- coding: utf-8 -*-
import re
import collections


RESOURCE_FOLDER = '../resources'
EPATH = '/Output/english-dictionary.txt'
ealphabet = 'abcdefghijklmnopqrstuvwxyz'


class SpellDict(object):

    def __init__(self, path, alphabet):
        self.NWORDS = self.train(
            self.words(file(RESOURCE_FOLDER + path).read()))
        self.alphabet = alphabet

    def words(self, text):
        return re.findall('[a-z]+', text.lower())

    def train(self, features):
        model = collections.defaultdict(lambda: 1)
        for f in features:
            model[f] += 1
        return model

    def edits1(self, word):
        splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        deletes    = [a + b[1:] for a, b in splits if b]
        transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
        replaces   = [a + c + b[1:]
                      for a, b in splits for c in self.alphabet if b]
        inserts    = [a + c + b
                      for a, b in splits for c in self.alphabet]
        return set(deletes + transposes + replaces + inserts)

    def known_edits2(self, word):
        return set(e2 for e1 in self.edits1(word)
                   for e2 in self.edits1(e1) if e2 in self.NWORDS)

    def known(self, words):
        return set(w for w in words if w in self.NWORDS)

    def correct(self, word):
        candidates = (self.known([word]) or self.known(self.edits1(word))
                      or self.known_edits2(word) or [word])
        return max(candidates, key=self.NWORDS.get)


HPATH =  '/Output/hindiwords.txt'
akshar = open(RESOURCE_FOLDER + '/akshar.txt').read().strip()
matra = open(RESOURCE_FOLDER + '/matra.txt').read().strip()
halphabets = [u for u in akshar]
halphabets.extend([u for u in matra])

spell = SpellDict(EPATH, ealphabet)
hspell = SpellDict(HPATH, halphabets)

if __name__ == '__main__':
    print spell.correct('speling')
    print spell.correct('whatevr')
    # \u0928\u094d
    w = u'\u0905\u0901\u0927\u0947\u0928\u0940'
    v = u'\u092e\u0901\u0917\u0947'
    # w1 = u'\u0901\u0927'
    print [u for u in w]
    print ','.join(u for u in w)
    print [u for u in v]
    print ','.join(u for u in v)
    # print hspell.correct(w.encode('utf-8'))
