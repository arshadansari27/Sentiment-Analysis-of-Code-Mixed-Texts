import pycrfsuite
from random import random
from substring_combo import splitclusters, esplitclusters, manage_length
import codecs

RESOURCE_FOLDER = '../../resources'
MFILE = RESOURCE_FOLDER + '/transliteration.crfsuite'

tagger = pycrfsuite.Tagger()
tagger.open(MFILE)
print '[Begin Testing]...'
with codecs.open('output.txt', 'w', encoding='utf8') as outfile:
    xseq = 'maange'
    xss = [u for u in esplitclusters(xseq)]
    ypredicted = tagger.tag(xss)
    v4 = "%s\t\n" % ''.join(ypredicted).decode('utf-8')
    outfile.write(xseq + '\t' + v4 )
