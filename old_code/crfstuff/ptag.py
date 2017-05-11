import codecs


lines = []
errorw = None
with open('test_cases.txt') as infile:
    for line in infile:
        line = line.decode('utf-8')
        words = line.split(' ')
        nwords = []
        for word in words:
            try:
                errorw = word
                word = word.strip()
                if '\\' in word:
                    _word = word.split('\\')
                    if len(_word) > 2:
                        continue
                    ww, t = _word
                    if t.startswith('E'):
                        ww = ww
                    elif t.startswith('H'):
                        ww = word.split('=')[-1]
                elif '=' in word:
                    ww = word.split('=')[-1]
                else:
                    ww = word.replace('[', '').replace(']', '')
                nwords.append(ww)
            except Exception, e:
                print '[*]', str(e), errorw
                raise
        lines.append(' '.join(nwords))

with codecs.open('transformed.txt', 'w', encoding='utf-8') as outfile:
    for line in lines:
        outfile.write(line + '\n')
