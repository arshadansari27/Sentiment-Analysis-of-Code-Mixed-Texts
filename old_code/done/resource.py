import os
import itertools
from collections import defaultdict

extra_chars = set([
    '!', '@', '#', '$', '%', '^', '&', '(', ')', '_', '=', '-', '+',
    '{', '}', '[', ']', '|', '\\', '/', '<', '>', ',', '.', '?'
])

RESOURCE_FOLDER = '../resources'

archive = RESOURCE_FOLDER + '/hindi-pairs'
files = []
for u in os.listdir(archive):
    if '_' in u:
        continue
    for j in os.listdir(archive + '/' + u):
        if not j.endswith('.txt'):
            continue
        files.append(archive + '/' + u + '/' + j)

files = [f for f in files if os.path.exists(f)]
lines = []
for f in files:
    _lines = filter(lambda u: len(u) > 3,
                    (l.strip() for l in open(f).readlines()))
    if not len(_lines) % 2 is 0:
        _lines = _lines[:-1]
    for line in _lines:
        lines.append(line.decode('utf-8'))

hh = open(RESOURCE_FOLDER + '/Output/pairs.txt', 'w')
for line in lines:
    hh.write("%s\n" % (line.encode('utf-8')))
hh.close()

lines = open(RESOURCE_FOLDER + '/Output/pairs.txt').readlines()
hh = open(RESOURCE_FOLDER + '/Output/pairs2.txt', 'w')
ll = len(lines)
word_pairs = defaultdict(set)
for i in xrange(0, ll, 2):
    if i + 1 > ll - 1:
        continue
    e = lines[i].strip()
    h = lines[i + 1].strip()
    hh.write("%s|%s\n" % (e, h))
    ewords = e.split(';')
    hwords = h.split(';')
    min_len = min(len(ewords), len(hwords))
    for i in xrange(min_len):
        word_pairs[ewords[i]].add(hwords[i])

ww = open(RESOURCE_FOLDER + '/Output/wordpairs.txt', 'w')

for key, words in word_pairs.iteritems():
    if not key or len(key) is 0:
        continue
    if any(c in key for c in extra_chars):
        for c in extra_chars:
            key = key.replace(c, ' ')
    for u in words:
        if any(c in u for c in extra_chars):
            for c in extra_chars:
                u = u.replace(c, ' ')
        if '*' in u:
            continue
        ww.write("%s:%s\n" % (key, u))

hh.close()
ww.close()
