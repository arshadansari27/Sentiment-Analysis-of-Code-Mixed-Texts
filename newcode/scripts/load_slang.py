from pymongo import MongoClient
import os

conn = MongoClient()
db = conn.sentiment_analysis_db


folder = '../../resources'

db.slang.remove({})
count = 0
for _file in os.listdir(folder):
    if not _file.startswith('urbandict'):
        continue
    path = folder + '/' + _file
    lines = open(path).read().split('\n')
    print path
    data = lines[:]
    stuff = []
    for line in data:
        words = line.strip().split(',')
        if len(words) < 3:
            continue
        entry = words[0]
        if len(entry) > 125:
            continue
        pos = words[1]
        neg = words[2]
        stuff.append({'word': entry, 'pos': pos, 'neg': neg})
        count += 1
        if len(stuff) > 10000:
            print 'Inserting in data', count
            db.slang.insert_many(stuff)
            stuff = []
if len(stuff) > 0:
    db.slang.insert_many(stuff)
    stuff = []


