import pickle
from nltk.corpus import wordnet as wn
from nltk.corpus import sentiwordnet as swn

HOME = '/home/vagrant/inner_workspace/sentiment-analysis-code-mix'  # '/home/arshad/workspace/rest/sentiment-analysis'
HF = HOME + '/tools/hindi_wordnet_python/'
MF = HOME + '/tools/marathi_wordnet_python/'
E, H, M = 'E', 'H', 'M'

print 'lOADING SYNSETS..',
word2Synset         = dict(H=pickle.load(open(HF + "WordSynsetDict.pk")), M=pickle.load(open(MF + "WordSynsetDict.pk")))
synset2Onto         = dict(H=pickle.load(open(HF + "SynsetOnto.pk")), M=pickle.load(open(MF + "SynsetOnto.pk")))
synonyms            = dict(H=pickle.load(open(HF + "SynsetWords.pk")), M=pickle.load(open(MF + "SynsetWords.pk")))
synset2Gloss        = dict(H=pickle.load(open(HF + "SynsetGloss.pk")), M=pickle.load(open(MF + "SynsetGloss.pk")))
synset2Hypernyms    = dict(H=pickle.load(open(HF + "SynsetHypernym.pk")), M=pickle.load(open(MF + "SynsetHypernym.pk")))
synset2Hyponyms     = dict(H=pickle.load(open(HF + "SynsetHyponym.pk")), M=pickle.load(open(MF + "SynsetHyponym.pk")))
synset2Hypernyms    = dict(H=pickle.load(open(HF + "SynsetHypernym.pk")), M=pickle.load(open(MF + "SynsetHypernym.pk")))
print 'done.'

def word_synset_synonyms_hindi(synset, pos=None):
    if synonyms[H].has_key(synset):
        if pos:
            return synonyms[H][synset].get(pos, [])
        else:
            return synonyms[H][synset]
    else:
        return {}

def word_synset(word, lang='E'):
    if lang == H:
        if word2Synset[H].has_key(word):
            synsets = word2Synset[H][word]
        else:
            synsets = None
    elif lang == M:
        if word2Synset[M].has_key(word):
            synsets = word2Synset[M][word]
        else:
            synsets = None
    else:
        synsets = wn.synsets(word)
    if not synsets:
        return None
    return synsets


if __name__ == '__main__':
    print '\n'.join(word2Synset[H].keys())
