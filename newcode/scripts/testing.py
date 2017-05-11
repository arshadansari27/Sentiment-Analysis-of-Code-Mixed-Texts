import nltk
from nltk import word_tokenize
from nltk.util import ngrams
text = "Hi How are you? i am fine and you"
token=nltk.word_tokenize(text)
for i in range(1, 5) :
    print list(ngrams(token, i))
