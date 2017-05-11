from pymongo import MongoClient
import os

conn = MongoClient()
db = conn.sentiment_analysis_db


folder = '../../resources'
stuff = []
db.smiley.drop_indexes()
db.smiley.remove({})
count = 0
for line in open(folder + '/smiley.txt'):
    line = line.strip()
    while '\t' in line:
        line = line.replace('\t', ' ')
    while '  ' in line:
        line = line.replace('  ', ' ')
    words = line.strip().split(' ')
    if len(words) < 2:
        continue
    smiley = words[0]
    text = ' '.join(words[1:])
    stuff.append({'smiley': smiley, 'text': text})
    count += 1
    if len(stuff) > 10000:
        print 'Inserting in data', count
        db.smiley.insert_many(stuff)
        stuff = []
if len(stuff) > 0:
    db.smiley.insert_many(stuff)
    stuff = []

db.smiley.ensure_index('smiley')
