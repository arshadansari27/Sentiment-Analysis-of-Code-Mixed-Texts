# -*- coding: utf-8 -*-

import nltk
from nltk.stem import *
from nltk.corpus import sentiwordnet as swn
from collections import defaultdict
from wordnet import word_synset, word_synset_synonyms_hindi
from normalize_bojar_lrec_2010 import normalise
from lemmatiser import lemmatise

import sqlite3

_hswn = defaultdict(lambda: defaultdict(tuple))
hindi_types = set([])

def hw():
    from main import HOME
    print 'Setting hswn...'
    if len(_hswn) is 0:
        conn = sqlite3.connect(HOME + '/resources/NLP_database.sqlite')
        cursor = conn.cursor()
        terms = {}
        for row in cursor.execute('SELECT POS, synset_id, p_score, n_score, terms FROM HSWN'):
            t = row[0]
            p = float(row[2])
            n = float(row[3])
            syn = row[1]
            _terms = set([' '.join(w.split('_')).strip() for w in row[4].strip().split(',')])

            _hswn[syn][t] = (p, n)
            for _term in _terms:
                if not terms.get(_term):
                    terms[_term] = []
                terms[_term].append((syn, t))

        for term, wlist in terms.iteritems():
            synsets = word_synset(term, 'H')
            if not synsets:
                continue
            if len(wlist) is 0:
                continue
            elif len(wlist) is 1:
                syn, pos = wlist[0]
                for ss in synsets.get(pos, []):
                    if ss in _hswn:
                        continue
                    else:
                        _hswn[ss][pos] = _hswn[syn][pos]
            else:
                p_score, n_score = 0., 0.
                
                for syn, pos in wlist:
                    p, n = _hswn[syn][pos]
                    p_score += p
                    n_score += n
                p_score = p_score / (1. * len(wlist))
                n_score = n_score / (1. * len(wlist))
                for ss in synsets.get(pos, []):
                    if ss in _hswn:
                        continue
                    else:
                        _hswn[ss][pos] = (p_score, n_score)

hw()


def english_sentiment(word, tag):
    pscore = 0 
    nscore = 0 
    try:
        z = list(swn.senti_synsets(word, tag))
        if len(z) > 0:
            p, n = z[0].pos_score(), z[0].neg_score()
            pscore+=p
            nscore+=n
    except:
        pass
    return pscore, nscore


def english_sentiments(word):
    pscore = 0 
    nscore = 0 
    ll = 0
    for wt in ['n', 'v', 'r', 'a']:
        z = list(swn.senti_synsets(word, wt))
        if len(z) > 0:
            p, n = z[0].pos_score(), z[0].neg_score()
            pscore+=p
            nscore+=n
            ll + 1
    if ll > 0:
        pscore = float(pscore) / ll
        nscore = float(nscore) / ll
    return pscore, nscore

def all_tags_sentiment(word, lang):
    if lang in ['E', 'S']:
        pscore = 0 
        nscore = 0 
        inverse = False 
        for wt in ['n', 'v', 'r', 'a']:
            z = list(swn.senti_synsets(word, wt))
            if len(z) > 0:
                p, n = z[0].pos_score(), z[0].neg_score()
                pscore+=p
                nscore+=n
        pscore = float(pscore) / 4
        nscore = float(nscore) / 4
    elif lang=='H':
        inverse = False
        pscore = 0.
        nscore = 0.
        
        synsets_to_collect = {}
        ss_lib = [
            word_synset(word, 'H'), 
            word_synset(lemmatise(word)[0], 'H'), 
            word_synset(normalise(word), 'H'), 
            word_synset(normalise(lemmatise(word)[0]), 'H'),  
            word_synset(lemmatise(normalise(word))[0], 'H')
        ]
        ss_count = 0
        synset_collection = []
        for synsets in ss_lib:
            if not synsets:
                continue
            for k, v in synsets.iteritem():
                if len(v) > 0:
                    for u in v:
                        synset_collection.append(u)
        if len(synset_collection) > 0:
                wts = 0
                for u in synset_collection:
                    for wt in [1, 2, 3, 4, '1', '2', '3', '4']:
                        p, n = sentiment_synsets(u, wt)
                        if p > 0. or n > 0.:
                            wts +=1
                    if wts > 0:
                        p = p / wts
                        n = n / wts
                    pscore+=p
                    nscore+=n
                pscore = pscore / len(synset_collection)
                nscore = nscore / len(synset_collection)

    elif lang=='M':
        inverse = False
        pscore = 0.
        nscore = 0.
    else:
        return 0., 0.
    return pscore, nscore



def sentiment(tagged, lang='E'):
    if lang in ['E', 'S']:
        pscore = 0 
        nscore = 0 
        inverse = False 
        wt = tagged[1]
        if wt in ['n', 'v', 'r', 'a']:
            ww = tagged[0]
            z = list(swn.senti_synsets(ww, wt))
            if len(z) > 0:
                p, n = z[0].pos_score(), z[0].neg_score()
                pscore+=p
                nscore+=n
            # print '\t\tE | score', pscore, nscore
        else:
            pass
            #print '\t\tE | no score'
    elif lang=='H':
        inverse = False
        pscore = 0.
        nscore = 0.
        wd = tagged[0]
        wt = tagged[2].lower()
        if 'NEG' == tagged[1]:
            inverse = True
        if 'nn' in [wt, tagged[1].lower()]:
            wt = 'n'
        elif wt == 'adj':
            wt = 'a'
        elif wt == 'adv':
            wt = 'r'
        else:
            wt = 'v'
        if wt == 'n':
            pos = 1
        elif wt == 'v':
            pos = 2
        elif wt == 'a':
            pos = 3
        else:
            pos = 4
        synsets_to_collect = {}
        found = False
        ss_lib = [
            word_synset(wd, 'H'), 
            word_synset(lemmatise(wd)[0], 'H'), 
            word_synset(normalise(wd), 'H'), 
            word_synset(normalise(lemmatise(wd)[0]), 'H'),  
            word_synset(lemmatise(normalise(wd))[0], 'H')
        ]
        print '****', ss_lib
        for ss in ss_lib:
            if ss:
                for _kk, _ss in ss.iteritems():
                    if not synsets_to_collect.get(_kk):
                        synsets_to_collect[_kk] = []
                    for __ss in _ss:
                        if __ss not in synsets_to_collect[_kk]:
                            synsets_to_collect[_kk].append(__ss)
        if not synsets_to_collect:
            print '\t\tH | no score'
            pass
        else:
            pscore, nscore = sentiment_synsets(synsets_to_collect, pos)
            # print '\t\tH | score', pscore, nscore
    elif lang=='M':
        inverse = False
        pscore = 0.
        nscore = 0.
    else:
        return 0., 0.
    return pscore, nscore


def sentiment_synsets(synsets, pos):
    scores = []
    synscores = []
    for k, sss in synsets.iteritems():
        for ss in sss:
            for polarity in _hswn.get(ss, {}).iteritems():
                scores.append(polarity[1])
                    
            synonyms = word_synset_synonyms_hindi(ss, pos)
            for v in synonyms:
                _synsets = word_synset(v, 'H')
                if not _synsets:
                    continue
                for _k, _sss in _synsets.iteritems():
                    for _ss in _sss:
                        for polarity in _hswn.get(ss, {}).iteritems():
                            assert len(polarity[1]) == 2
                            #if polarity[0] == pos:
                            # print '\t\t\t\tFound Synonym polarity', polarity[1]
                            synscores.append(polarity[1])
    
    if len(scores) > 0:
        print '**** Hindi senti found'
        return float(sum([u[0] for u in scores]))/len(scores), float(sum([u[1] for u in scores]))/len(scores)
    elif len(synscores) > 0:
        print '**** Hindi senti found through synonyms'
        return float(sum([u[0] for u in synscores]))/len(synscores), float(sum([u[1] for u in synscores]))/len(synscores)
    else:
        print '**** Hindi senti not found'
        # print '\tFound No Polarity'
        return 0., 0.

def hindi_sentiment(word, tag):
    synsets = word_synset(word, 'H')
    p_score = 0
    n_score = 0
    polarity_count = 0
    if not synsets:
        return 0., 0.
    for pos, ss in synsets.iteritems():
        if pos != tag:
            continue
        for s in ss:
            for polarities in _hswn.get(s, {}).iteritems():
                (t, (p, n)) =  polarities
                if p > 0. or n > 0.:
                    polarity_count += 1
                    p_score += p
                    n_score += n
    if polarity_count > 0:
        return p_score / polarity_count, n_score/polarity_count
    else:
        return 0., 0.



def hindi_sentiments(word):
    synsets = word_synset(word, 'H')
    p_score = 0
    n_score = 0
    polarity_count = 0
    if not synsets:
        return 0., 0.
    for pos, ss in synsets.iteritems():
        for s in ss:
            for polarities in _hswn.get(s, {}).iteritems():
                (t, (p, n)) =  polarities
                if p > 0. or n > 0.:
                    polarity_count += 1
                    p_score += p
                    n_score += n
    if polarity_count > 0:
        return p_score / polarity_count, n_score/polarity_count
    else:
        return 0., 0.





if __name__ == '__main__':
    SCORES = []
    word = "खाना".decode('utf-8', 'ignore')
    synsets = word_synset(word, 'H')
    pos = '3'
    for ss in synsets[pos]:
        print '\t', ss
        for polarities in _hswn.get(ss, {}).iteritems():
            print '\t-->', polarities
        synonyms = word_synset_synonyms_hindi(ss, pos)
        for v in synonyms:
            print '\t\t', [v]
            _synsets = word_synset(v, 'H')
            if not _synsets:
                continue
            for _ss in _synsets.get(pos, []):
                print '\t\t\t', _ss
                for _polarities in _hswn.get(_ss, {}).iteritems():
                    print '\t\t\t-->', _polarities
                
            print '+++++++++++++++++++++++++++++++++++++'
        print '-----------------------------------'




    print SCORES
