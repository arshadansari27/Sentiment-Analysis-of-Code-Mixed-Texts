# -*- coding: utf-8 -*-

import codecs
from sanscript import HK, DEVANAGARI, transliterate
# import pycrfsuite
from collections import defaultdict


vowels = set(['a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O' 'U'])
RESOURCE_FOLDER = '../resources'

pointers = defaultdict(lambda: defaultdict(int))
x_previous_tags = defaultdict(lambda: defaultdict(int))
x_next_tags = defaultdict(lambda: defaultdict(int))
y_previous_tags = defaultdict(lambda: defaultdict(int))
y_next_tags = defaultdict(lambda: defaultdict(int))


def start():
    size_diff, total = 0, 0
    sum_total = defaultdict(int)

    with open(RESOURCE_FOLDER+'/Output/all-words-pairs.txt') as infile:
        for line in infile:
            total += 1
            line = line.strip()
            e, h = line.split('\t')
            e = e.decode('utf-8')
            h = h.decode('utf-8')
            op = transliterate(h, DEVANAGARI, HK)
            xss = [u for u in ngrams(e)]
            yss = [u for u in ngrams(op)]

            if total > 2000:
                break

            for _u in xss:
                for _v in yss:
                    # print _u
                    # print _v
                    u = _u[0]
                    u_prev = _u[1]
                    u_next = _u[2]
                    v = _v[0]
                    v_prev = _v[1]
                    v_next = _v[2]
                    pointers[u][v] += 1
                    for i in xrange(len(u_prev)):
                        x_previous_tags[u][u_prev[i:]] += 1
                    for j in xrange(1, len(u_next)):
                        x_next_tags[u][u_next[:j]] += 1
                    for i in xrange(len(v_prev)):
                        y_previous_tags[v][v_prev[i:]] += 1
                    for j in xrange(1, len(v_next)):
                        x_next_tags[v][v_next[:j]] += 1


                    sum_total[u] += len(yss)
            if total % 1000 is 0:
                print total
    print len(pointers), '...'
    print 'Normalizing and saving probabilities'
    with codecs.open('probabilities.txt', 'w', encoding='utf8') as outfile:
        for k, vdict in pointers.iteritems():
            tot = sum_total[k]
            values = sorted([(u, (v * factor(k, u))/tot) for (u, v) in vdict.iteritems()], reverse=True, key=lambda x: x[1])
            ll = int(len(vdict) * .3)
            if ll > 10:
                ll = 10
            values = values[:ll]
            for value in values:
                u, v = value
                if v < 0.001:
                    continue
                outfile.write("%s\t%s\t%f\n" % (k, u, v))
            outfile.flush()

    print 'Writing x previous'
    with codecs.open('x_previous.txt', 'w', encoding='utf8') as outfile:
        for k, vdict in x_previous_tags.iteritems():
            for u, v in vdict.iteritems():
                outfile.write("%s\t%s\t%f\n" % (k, u, v))
            outfile.flush()
    print 'Writing x next'
    with codecs.open('x_next.txt', 'w', encoding='utf8') as outfile:
        for k, vdict in x_next_tags.iteritems():
            for u, v in vdict.iteritems():
                outfile.write("%s\t%s\t%f\n" % (k, u, v))
            outfile.flush()
    print 'Writing y previous'
    with codecs.open('y_previous.txt', 'w', encoding='utf8') as outfile:
        for k, vdict in y_previous_tags.iteritems():
            for u, v in vdict.iteritems():
                outfile.write("%s\t%s\t%f\n" % (k, u, v))
            outfile.flush()
    print 'Writing y next'
    with codecs.open('y_next.txt', 'w', encoding='utf8') as outfile:
        for k, vdict in y_next_tags.iteritems():
            for u, v in vdict.iteritems():
                outfile.write("%s\t%s\t%f\n" % (k, u, v))
            outfile.flush()




    print 'Total:', total

def factor(k, u):
    counts = 0
    i_matches = set([])
    j_matches = set([])
    for idx, i in enumerate(k):
        for jdx, j in enumerate(u):
            if i == j and idx not in i_matches and jdx not in j_matches:
                counts += 1.
                i_matches.add(idx)
                j_matches.add(jdx)
    return counts / (1 + abs(len(k) - len(u)))


def ngrams(word):
    words = []
    for N in xrange(1, 5):
        for i in xrange(len(word)):
            if i + N <= len(word):
                _prev = word[:i] if i >= 0 else ''
                _next = word[i + N:] if (i + N) < len(word)  else ''
                words.append((word[i: i + N], _prev, _next))
    return words


if __name__ == '__main__':
    start()
