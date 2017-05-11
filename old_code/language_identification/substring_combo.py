import unicodedata


vowels = set(['a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O' 'U'])


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
