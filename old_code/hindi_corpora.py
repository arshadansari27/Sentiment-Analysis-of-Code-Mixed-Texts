import os
folder = 'resources/hin_corp_unicode'
files = os.listdir(folder)
files = [f for f in files if f.endswith('txt')]

print 'Files', len(files)
words = set([])
for file in files:

    chars = [
        '~', '`', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_',
        '+', '=', '{', '}', ':', ';', "'", '"', '<', '>', '.', ',', '?', '/',
        '\\', '|'
    ]
    data = open("%s/%s" % (folder, file)).read()
    data = data.decode('utf8')
    for c in chars:
        data = data.replace(c, ' ')

    data = [d.strip() for d in data.split(' ') if len(d.strip()) > 0]
    for d in data:
        words.add(d)

print 'Words', len(words)
with open('resources/hindi-wordlist.txt', 'w') as _f:
    _f.write('\n'.join([w.encode('utf-8') for w in words]))
