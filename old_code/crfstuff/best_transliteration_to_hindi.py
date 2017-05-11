from random import random
from sanscript import HK, transliterate, DEVANAGARI, SCHEMES
import codecs
import pycrfsuite


schemes = SCHEMES[DEVANAGARI]
CONSONANTS = [u.encode('utf-8') for u in schemes['consonants']]
VOWELS = [u.encode('utf-8') for u in schemes['vowels']]
vowels = set(['a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O' 'U'])
RESOURCE_FOLDER = '../resources'

def ngrams(word):
    words = []
    for N in xrange(1, 5):
        for i in xrange(len(word)):
            if i + N <= len(word):
                words.append(word[i: i + N])
    return words


def esplitclusters(word):
    nword = word
    cluster = []
    for i, w in enumerate(nword):
        if len(cluster) > 0:
            if i > 0 and w in ['h', 'H'] and nword[i - 1] not in vowels:
                cluster.append(word[i])
                continue
            if w not in vowels and len(cluster) > 0:
                yield ''.join(cluster)
                cluster = []
        cluster.append(word[i])
    if len(cluster) > 0:
        yield ''.join(cluster)


def train(train_ratio, test_ratio):
    MFILE = 'sanscript4.crfsuite'
    count = 0
    train_sents = []
    test_sents = []
    with open(RESOURCE_FOLDER+'/Output/all-words-pairs.txt') as infile:
        for line in infile:
            count += 1
            line = line.strip()
            e, h = line.split('\t')
            e = e  # .decode('utf-8')
            h = h.decode('utf-8')
            ie = transliterate(h, DEVANAGARI, HK).encode('utf-8')
            if random() < train_ratio:
                train_sents.append((e, ie))
            if random() > test_ratio:
                test_sents.append((e, h))

    print '[*] NOT TRAINING'
    X_train = [s[0] for s in train_sents]
    y_train = [s[1] for s in train_sents]
    X_test = [s[0] for s in test_sents]
    y_test = [s[1] for s in test_sents]

    print 'Loading trainer...'
    print len(X_train), len(y_train)
    print len(X_test), len(y_test)

    trainer = pycrfsuite.Trainer(verbose=False)

    count = 0
    skipped = 0
    for xseq, yseq in zip(X_train, y_train):
        if count % 100 is 0:
            print count
        try:
            xss = [xs for xs in ngrams(xseq)]
            yss = [ys for ys in ngrams(yseq)]
            for xs in xss:
                for ys in yss:
                    count += 1
                    trainer.append([xs], [ys])
        except Exception, e:
            print str(e)
            skipped += 1

    print ''
    print 'Training len', len(X_train), len(y_train)
    print 'Test len', len(X_test), len(y_test)
    print '[*] Actually trained', (count)

    trainer.set_params({'c1': 1.0, 'c2': 1e-3, 'max_iterations': 50,
                        'feature.possible_transitions': True})

    print 'Training begun...'
    trainer.train(MFILE)
    print '[Done]'
    tagger = pycrfsuite.Tagger()
    tagger.open(MFILE)
    print '[Begin Testing]...'
    count = 0
    print 'Writing to output.txt'
    with codecs.open('output.txt', 'w', encoding='utf-8') as outfile:
        for xseq, yseq in zip(X_test, y_test):
            count += 1
            if count % 100 is 0:
                print count
            xss = [xs for xs in esplitclusters(xseq)]
            ypredicted = tagger.tag(xss)
            ypredicted2 = tagger.tag([xss])
            # print xss, ypredicted
            _ie = transliterate(''.join(ypredicted), HK, DEVANAGARI)
            v1 = "%s\t" % xseq
            v2 = "%s\t" % yseq
            v3 = "%s\t" % [u.decode('utf-8') for u in ypredicted]
            v4 = "%s\t" % ''.join(ypredicted).decode('utf-8')
            v5 = "%s\t" % [u.decode('utf-8') for u in ypredicted2]
            v6 = "%s\t" % ','.join(ypredicted2).decode('utf-8')
            v7 = "%s\t" % _ie
            val = v1 + v2 + v3 + v4 + v5 + v6 + v7 + '\n'
            outfile.write(val)


if __name__ == '__main__':
    train(0.04, 0.2)
    # print ngrams('arshad')
    # print ngrams('something')
    # print ngrams('true')
    # print ngrams('yo')
