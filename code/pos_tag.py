# -*- coding: utf-8 -*-

from normalize_bojar_lrec_2010 import normalise
from lemmatiser import lemmatize_word
import subprocess, re, os, time, nltk
from nltk.tag import pos_tag, map_tag
from nltk.corpus import wordnet

def tag_words_marathi(text):
    return []


def tag_words_hindi(text):
    tags = []
    text = normalise(text.encode("utf-8", 'replace'))
    text = text.replace('।', '')
    text = text.replace(' ', '\n')
    try:
        with open('../hindi.tmp.words', 'w') as outfile: 
            outfile.write(text)

        process = subprocess.Popen("../tnt -v0 -H ../models/hindi ../hindi.tmp.words", stdout=subprocess.PIPE, shell=True)
        text = process.communicate()[0].strip()
        lines = lemmatize_word(text)
        for line in lines:
            line = re.sub('\t+','\t', line)
            parts = [u for u in line.split('\t') if len(u) > 0]
            if len(parts) is 0:
                continue
            tag_parts = parts[1].split('.')
            tags.append((parts[0].strip(), tag_parts[0], tag_parts[1]))
    finally:
        if os.path.exists('../hindi.tmp.words'):
            os.remove('../hindi.tmp.words')
    return tags

def get_wordnet_pos(treebank_tag):

    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return ''

def tag_words_english(text):
    text = nltk.word_tokenize(text)
    tagged_sent = nltk.pos_tag(text)
    updated_tagged= [(word, get_wordnet_pos(tag).lower()) for word, tag in tagged_sent]
    return updated_tagged

if __name__ == '__main__':
    print '\n'.join("%s -> %s" % (u, v) for u, v in tag_words_english("this is my test subject, which is awesome"))
    # print '\n'.join("%s -> %s %s" % (u, v, w) for u, v, w in tag_words_hindi(open('hindi.input.txt').read().decode('utf-8')))
