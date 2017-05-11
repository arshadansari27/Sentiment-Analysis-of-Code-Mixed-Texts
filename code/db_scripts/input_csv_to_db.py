import pymongo
db = pymongo.MongoClient().sentiment_analysis_db

HOME = '/home/arshad/workspace/rest/sentiment-analysis'

def load_seed(file_name, db_name):
    db[db_name].drop()
    count = 0
    lines = []
    for line in open(HOME + '/resources/input_csv/%s' % file_name):
        line  = line.strip().decode('utf-8')
        count += 1
        if count % 10 is 0: 
            print count
        line = line.strip()
        if len(line) is 0:
            continue
        x = line.split('|')
        u, v = x[0], x[1]
        u, v = u.strip(), v.strip()
        if len(u) == 0 or len(v) == 0:
            continue
        lines.append((v, u))
    db[db_name].insert_many([{'line': u, 'output': v} for (u, v) in lines])
    print db[db_name].count()

if __name__ == '__main__':
    load_seed('hindi.csv', 'csv_hindi_db')
    load_seed('hindi_mix.csv', 'csv_hindi_mix_db')
    load_seed('marathi.csv', 'csv_marathi_db')
