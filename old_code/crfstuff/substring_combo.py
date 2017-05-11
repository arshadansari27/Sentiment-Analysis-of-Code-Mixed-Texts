import unicodedata
from sanscript import DEVANAGARI, SCHEMES
VOWELS = SCHEMES[DEVANAGARI]['vowels']
CONSONANTS = SCHEMES[DEVANAGARI]['consonants']


HALFLING = u'\u094d'
vowels = set(['a', 'e', 'i', 'o', 'u'])


def clusterify_machine_transliterated(nword, oword=None):
    clusters = [u.replace(HALFLING, u'') for u in splitclusters(nword)]
    i, j = 0, 1
    word = []
    while i < len(clusters):
        word.append(clusters[i])
        if j < len(clusters) and clusters[j] in VOWELS and len(word) > 0:
            word[-1] += clusters[j]
            i += 1
            j += 1
        i += 1
        j += 1
    if oword:
        oclusters = [u for u in splitclusters(oword)]
        if len(word) > len(oclusters):
            word = word[: len(oclusters)]
        elif len(word) < len(oclusters):
            diff = len(oclusters) - len(word)
            word.extend(['.'] * diff)
    return word


def manage_length(eword, hword):
    xss, yss = eword, hword
    if len(xss) == len(yss) + 1:
        if len(xss[-1]) is 1:
            if xss[-1] == 'n' and xss[-2][-1] == 'o':
                xss[-2] = xss[-2] + xss[-1]
                xss = xss[:-1]
    if len(xss) > len(yss):
        try:
            i = xss.index('n')
            j = xss.index('g')
            if i > -1 and j > -1 and i + 1 == j:
                xss[i] = 'ng'
            xss = [u for l, u in enumerate(xss) if l != j]
        except:
            pass
    return xss


def esplitclusters(word):
    nword = word
    cluster = []
    for i, w in enumerate(nword):
        if len(cluster) > 0:
            if w not in vowels and len(cluster) > 0:
                yield ''.join(cluster)
                cluster = []
        cluster.append(word[i])
    if len(cluster) > 0:
        yield ''.join(cluster)


def substrings(s, l):
    if l == 1:
        return [tuple([s])]
    combos1 = _substring(s)
    combos2 = _substring(s[::-1], reverse=True)
    if len(combos1) is 0 and len(combos2) is 0:
        combos = []
    elif len(combos1) > 0 and len(combos2) is 0:
        combos = list(combos1)
    elif len(combos1) is 0 and len(combos2) > 0:
        combos = list(combos2)
    else:
        _c = list(combos1)
        _c.extend(list(combos2))
        combos = list(set(_c))
    return [c for c in combos if len(c) == l]


def _substring(s, reverse=False):
    combos = set([])
    curr = []
    for i in xrange(len(s)):
        for j in xrange(i + 1, len(s)):
            if i > 0:
                for l in xrange(i):
                    curr.append(s[l])
            u = s[i:j]
            if reverse:
                u = u[::-1]
            curr.append(u)
            for k in xrange(j, len(s)):
                curr.append(s[k])
            if reverse:
                curr = curr[::-1]
            combos.add(tuple(curr))
            curr = []
    return combos


def splitclusters(s):
    virama = u'\N{DEVANAGARI SIGN VIRAMA}'
    cluster = u''
    last = None
    for c in s:
        cat = unicodedata.category(c)[0]
        if cat == 'M' or cat == 'L' and last == virama:
            cluster += c
        else:
            if cluster:
                yield cluster
            cluster = c
        last = c
    if cluster:
        yield cluster


if __name__ == '__main__':
    x = 'rukenge'
    print x
    cbs = substrings(x, 5)
    for c in cbs:
        print c
