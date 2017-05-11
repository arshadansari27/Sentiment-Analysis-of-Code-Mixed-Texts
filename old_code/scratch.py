from lib import HindiAlphabets


e, h = 'khushboo', u'खुशबू'
pairs = HindiAlphabets().syllable_pairs(h)

print pairs
for syllables in all_syllables:
    if len(syllables) != len(pairs):
        continue
    print 'Possible Pairs'
    print syllables
