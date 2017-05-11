from collections import defaultdict
import simplejson as json
from slice import Slice

RESOURCE_FOLDER = '../resources'

consonants = ['b', 'c', 'd', 'f', 'g', 'j', 'k', 'l', 'm',
              'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'y', 'z']

hsyllable_representations = defaultdict(lambda: defaultdict(int))
hsyllable_prev_combination_count = defaultdict(lambda: defaultdict(int))
hsyllable_count = defaultdict(int)
esyllable_count = defaultdict(int)
word_dict = defaultdict(set)

diff_length, total_length = 0, 0


def update_on(english_syll, hindi_syll):
    neng = []
    if 'n' in english_syll and any(u'\u0902' in x for x in hindi_syll):
        i = 0
        while i < len(english_syll):
            if i + 1 < len(english_syll) and english_syll[i + 1] == u'n':
                neng.append(english_syll[i] + english_syll[i + 1])
                i += 1
            else:
                neng.append(english_syll[i])
            i += 1
    else:
        neng = english_syll

    return neng, hindi_syll


incorrect_pairings = []

with open(RESOURCE_FOLDER+'/Output/all-words-pairs.txt') as infile:
    with open('diff.txt', 'w') as outfile:
        for line in infile:
            line = line.strip()
            e, h = line.split('\t')
            e = e.decode('utf-8')
            h = h.decode('utf-8')
            word_dict[h].add(e)
            el = [u for u in Slice(e, len(e)).morphemes]
            hl = [u for u in Slice(h, len(h), True).morphemes]
            el, hl = update_on(el, hl)

            total_length += 1
            if len(el) == len(hl):
                for i in xrange(len(el)):
                    hsyllable_representations[hl[i]][el[i]] += 1
                    if i + 1 < len(el) and i > 0:
                        hsyllable_prev_combination_count[hl[i]][hl[i - 1]] += 1
                    hsyllable_count[hl[i]] += 1
                    esyllable_count[el[i]] += 1
            else:
                diff_length += 1
                incorrect_pairings.append((el, hl))

        for el, hl in incorrect_pairings:
            nel = []
            for ihl in hl:
                el_list = hsyllable_representations.get(ihl)
                if el_list:
                    el_elem = max(((u, v) for u, v in el_list.iteritems()),
                                  key=lambda _u: _u[1])[0]
                    nel.append(el_elem)

            el = nel
            outfile.write("%s\t%s\n" % (','.join(u.encode('utf-8')
                                                 for u in el),
                                        ','.join(u.encode('utf-8')
                                                 for u in hl)))

with open(RESOURCE_FOLDER + "/Output/probability_count.json", 'w') as outfile:
    outfile.write(json.dumps(dict(count=hsyllable_count,
                                  sequence=hsyllable_prev_combination_count,
                                  condition=hsyllable_representations,
                                  ecount=esyllable_count),
                             indent=4))

with open(RESOURCE_FOLDER + '/Output/word_dict.json', 'w') as outfile:
    _word_dict = {}
    for k, v in word_dict.iteritems():
        _word_dict[k] = list(v)
    outfile.write(json.dumps(_word_dict, indent=4))

print total_length, diff_length
