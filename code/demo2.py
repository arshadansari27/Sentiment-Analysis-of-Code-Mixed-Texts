# -*- coding: utf-8 -*-

"""
Demo program of Hindi WordNet in Python. 

Here I demonstrate all the functionalities of the libraries, but note you can load only the pickle files which are necessary for your task rather than loading every pickle file. Loading of pickle files takes time and memory. But once loaded, all your WordNet operations are just O(1) which means your WordNet lookup is no longer a bottleneck.

Developer: Siva Reddy <siva@sivareddy.in>
Please point http://sivareddy.in/downloads for others to find these python libraries.

"""

import pickle
from main import HOME
HF = HOME + '/tools/hindi_wordnet_python/'
MF = HOME + '/tools/marathi_wordnet_python/'
H, M = 'H', 'M'

word2Synset         = dict(H=pickle.load(open(HF + "WordSynsetDict.pk")), M=pickle.load(open(MF + "WordSynsetDict.pk")))
synset2Onto         = dict(H=pickle.load(open(HF + "SynsetOnto.pk")), M=pickle.load(open(MF + "SynsetOnto.pk")))
synonyms            = dict(H=pickle.load(open(HF + "SynsetWords.pk")), M=pickle.load(open(MF + "SynsetWords.pk")))
synset2Gloss        = dict(H=pickle.load(open(HF + "SynsetGloss.pk")), M=pickle.load(open(MF + "SynsetGloss.pk")))
synset2Hypernyms    = dict(H=pickle.load(open(HF + "SynsetHypernym.pk")), M=pickle.load(open(MF + "SynsetHypernym.pk")))
synset2Hyponyms     = dict(H=pickle.load(open(HF + "SynsetHyponym.pk")), M=pickle.load(open(MF + "SynsetHyponym.pk")))
synset2Hypernyms    = dict(H=pickle.load(open(HF + "SynsetHypernym.pk")), M=pickle.load(open(MF + "SynsetHypernym.pk")))

word = "खाना".decode('utf-8', 'ignore')
if word2Synset[H].has_key(word):
    synsets = word2Synset[H][word]
    print "Word -->", "खाना "
    for pos in synsets.keys():
        print "POS Category -->", pos
        for synset in synsets[pos]:
            print "\t\tSynset -->", synset
            if synonyms[H].has_key(synset):
                print "\t\t\t Synonyms -->", synonyms[synset]
                
