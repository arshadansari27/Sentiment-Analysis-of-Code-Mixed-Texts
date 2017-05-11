from pymongo import MongoClient
import os

conn = MongoClient()
db = conn.sentiment_analysis_db


folder = '../../resources/Marathi-Hindi'

db.bilingual_dictionary_mr_hi.remove({})
stuff = []
count = 0

for _file in os.listdir(folder):
    path = folder + '/' + _file
    lines = open(path).read().split('\n')
    for line in lines:
        words = line.strip().split(':')
        if len(words) < 2:
            continue
        mar = words[0].strip()
        hindis = [u.strip() for u in words[1].split(' ')]
        stuff.append({'word': mar, 'dict': hindis})
        count += 1
        if len(stuff) > 10000:
            print 'Inserting in data', count
            db.bilingual_dictionary_mr_hi.insert_many(stuff)
            stuff = []
if len(stuff) > 0:
    db.bilingual_dictionary_mr_hi.insert_many(stuff)
    stuff = []


