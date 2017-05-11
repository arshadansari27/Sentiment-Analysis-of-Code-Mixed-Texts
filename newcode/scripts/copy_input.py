from pymongo import MongoClient

conn = MongoClient()
db = conn.sentiment_analysis_db

for obj in db.csv_hindi_db.find({}):
    if obj['output'] == 'negetive':
        obj['output'] = 'negative'
    db.csv_input_all.insert({
        'line': obj['line'],
        'output': obj['output'],
        'lang': 'H'
    })

for obj in db.csv_hindi_mix_db.find({}):
    if obj['output'] == 'negetive':
        obj['output'] = 'negative'
    db.csv_input_all.insert({
        'line': obj['line'],
        'output': obj['output'],
        'lang': 'H'
    })

for obj in db.csv_marathi_db.find({}):
    if obj['output'] == 'negetive':
        obj['output'] = 'negative'
    db.csv_input_all.insert({
        'line': obj['line'],
        'output': obj['output'],
        'lang': 'M'
    })
