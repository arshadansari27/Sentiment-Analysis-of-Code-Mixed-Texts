from pymongo import MongoClient

conn = MongoClient()
db = conn.sentiment_analysis_db

for line in open('../../resources/codemix_tweets.txt'):
    ll = line.strip().split('|')
    sentiment, line = ll[0], ' '.join(ll[1:])
    db.csv_input_all.insert({
        'line': line,
        'output': sentiment,
        'lang': 'H'
    })
