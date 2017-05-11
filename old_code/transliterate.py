# -*- coding: UTF-8 -*-

def toL(ip):
    out=""
    la=len(ip)
    da=False
    for i in xrange(la):
        print i
        nC1=ip[i]
        nC2=ip[i+1] if (i + 1) < la else ''
        nC3=ip[i+2] if (i + 2) < la else ''

        if nC1 ==  '०':
            lC='0'
        elif nC1 ==  '१' :
            lC='1'
        elif nC1 ==  '२' :
            lC='2'
        elif nC1 ==  '३' :
            lC='3'
        elif nC1 ==  '४' :
            lC='4'
        elif nC1 ==  '५' :
            lC='5'
        elif nC1 ==  '६' :
            lC='6'
        elif nC1 ==  '७' :
            lC='7'
        elif nC1 ==  '८' :
            lC='8'
        elif nC1 ==  '९' :
            lC='9'
        elif nC1 ==  'ॐ' :
            lC='OmSymbol'
        elif nC1 ==  'ः' :
            lC='H'
        elif nC1 ==  'अ' :
            lC='A'
        elif nC1 ==  'आ' :
            lC='AA'
        elif nC1 ==  'ऐ' :
            lC='AI'
        elif nC1 ==  'औ' :
            lC='AO'
        elif nC1 ==  'ऍ' :
            lC='AE'
        elif nC1 ==  'ऑ' :
            lC='AW'
        elif nC1 ==  'इ' :
            lC='I'
        elif nC1 ==  'ई' :
            lC='EE'
        elif nC1 ==  'ए' :
            lC='E'
        elif nC1 ==  'उ' :
            lC='U'
        elif nC1 ==  'ऊ' :
            lC='OO'
        elif nC1 ==  'ओ' :
            lC='O'
        elif nC1 ==  'ऋ' :
            lC='RI'
        elif nC1 ==  'ृ' :
            lC='Ri'
        elif nC1 ==  'र्‍' :
            lC='R'
        elif nC1 ==  'ा' :
            lC='aa'
        elif nC1 ==  'ै' :
            lC='ai'
        elif nC1 ==  'ौ' :
            lC='ao'
        elif nC1 ==  'ॅ' :
            lC='ae'
        elif nC1 ==  'ॉ' :
            lC='aw'
        elif nC1 ==  'ि' :
            lC='i'
        elif nC1 ==  'ी' :
            lC='ee'
        elif nC1 ==  'े' :
            lC='e'
        elif nC1 ==  'ु' :
            lC='u'
        elif nC1 ==  'ू' :
            lC='oo'
        elif nC1 ==  'ो' :
            lC='o'
        elif nC1 ==  'ख' :
            da=True
            if (nC2=='़') :
                lC='Kh'
                i+=1
            else:
                lC='kh'
        elif nC1 ==  'क' :
            da=True
            if (nC2=='़') :
                lC='Q'
                i+=1
            else:
                lC='k'
        elif nC1 ==  'घ' :
            da=True
            lC='gh'
        elif nC1 ==  'ग' :
            da=True
            if (nC2=='़') :
                lC='G'
                i+=1
            else:
                lC='g'
        elif nC1 ==  'छ' :
            da=True
            lC='chh'
        elif nC1 ==  'च' :
            da=True
            lC='ch'
        elif nC1 ==  'झ' :
            da=True
            lC='jh'
        elif nC1 ==  'ज' :
            da=True
            if (nC2=='़') :
                lC='Z'
                i+=1
            elif ((nC2=='्') and (nC3=='ञ')) :
                da=False
                lC='gNy'
                i+=2
            else:
                lC='j'
        elif nC1 ==  'ठ' :
            da=True
            lC='Th'
        elif nC1 ==  'ट' :
            da=True
            lC='T'
        elif nC1 ==  'ढ' :
            da=True
            if (nC2=='़') :
                lC='Ddh'
                i+=1
            else:
                lC='Dh'
        elif nC1 ==  'ड' :
            da=True
            if (nC2=='़') :
                lC='Dd'
                i += 1
            else:
                lC='D'
        elif nC1 ==  'थ' :
            da=True
            lC='th'
        elif nC1 ==  'त' :
            da=True
            lC='t'
        elif nC1 ==  'ध' :
            da=True
            lC='dh'
        elif nC1 ==  'द' :
            da=True
            lC='d'
        elif nC1 ==  'फ' :
            da=True
            if (nC2=='़') :
                lC='F'
                i += 1
            else:
                lC='ph'
        elif nC1 ==  'प' :
            da=True
            lC='p'
        elif nC1 ==  'भ' :
            da=True
            lC='bh'
        elif nC1 ==  'ब' :
            da=True
            lC='b'
        elif nC1 ==  'य' :
            da=True
            lC='y'
        elif nC1 ==  'र' :
            da=True
            lC='r'
        elif nC1 ==  'ल' :
            da=True
            lC='l'
        elif nC1 ==  'व' :
            da=True
            lC='v'
        elif nC1 ==  'श' :
            da=True
            lC='sh'
        elif nC1 ==  'स' :
            da=True
            lC='s'
        elif nC1 ==  'ष' :
            da=True
            lC='Sh'
        elif nC1 ==  'ह' :
            da=True
            lC='h'
        elif nC1 ==  'म' :
            da=True
            lC='m'
        elif nC1 ==  'न' :
            da=True
            lC='n'
        elif nC1 ==  'ङ' :
            da=True
            lC='NG'
        elif nC1 ==  'ञ' :
            da=True
            lC='NJ'
        elif nC1 ==  'ण' :
            da=True
            lC='NN'
        elif nC1 ==  'ढ़' :
            da=True
            lC='Ddh'
        elif nC1 ==  'ड़' :
            da=True
            lC='Dd'
        elif nC1 ==  'ज़' :
            da=True
            lC='J'
        elif nC1 ==  'फ़' :
            da=True
            lC='F'
        elif nC1 ==  'ख़' :
            da=True
            lC='Kh'
        elif nC1 ==  'ग़' :
            da=True
            lC='G'
        elif nC1 ==  'क़' :
            da=True
            lC='Q'
        elif nC1 ==  'ळ' :
            da=True
            lC='L'
        elif nC1 ==  'ँ' :
            lC='Nn'
        elif nC1 ==  'ं' :
            lC='N'
        elif nC1 ==  '।' :
            lC=''
        elif nC1 ==  '\r' :
            lC=nC1
            if (nC2=='\n') :
                lC='\r\n'
                i += 1
        else:
            lC=nC1

        if (da==True):
            if (nC2=='़'):
                nC2=nC3
                if nC2 in  ['ृ'  , 'ा'  , 'ै'  , 'ौ'  , 'ॅ'  , 'ॉ'  , 'ि'  , 'ी' , 'े'  , 'ु'  , 'ू'  , 'ो'  ]:
                    da=False
                    continue
                if nC2 ==  '्' :
                    da=False
                    i+=1
                if nC2 in [' ',  ',',  '.' ,  '।' ,  '\r' ,  ')' ,  ']' ,  '\t' ]:
                    if not ( (nC1=='य') or (nC1=='र') ):
                        da=False
                out +=lC
        if (da==True) :
            out += 'a'
            da=False
    return out

print toL('आप कैसे हैं?')
