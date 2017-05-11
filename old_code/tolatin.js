function toL() {

document.f.lOut.value="";
la=document.f.nIn.value.length;
da=false;

for (i=0; i<la; i++) {

    nC1=document.f.nIn.value.charAt(i);
    nC2=document.f.nIn.value.charAt(i+1);
    nC3=document.f.nIn.value.charAt(i+2);
    switch (nC1) {
        case '०' : lC='0'; break;
        case '१' : lC='1'; break;
        case '२' : lC='2'; break;
        case '३' : lC='3'; break;
        case '४' : lC='4'; break;
        case '५' : lC='5'; break;
        case '६' : lC='6'; break;
        case '७' : lC='7'; break;
        case '८' : lC='8'; break;
        case '९' : lC='9'; break;
        case 'ॐ' : lC='OmSymbol'; break;
        case 'ः' : lC='H'; break;
        case 'अ' : lC='A'; break;
        case 'आ' : lC='AA'; break;
        case 'ऐ' : lC='AI'; break;
        case 'औ' : lC='AO'; break;
        case 'ऍ' : lC='AE'; break;
        case 'ऑ' : lC='AW'; break;
        case 'इ' : lC='I'; break;
        case 'ई' : lC='EE'; break;
        case 'ए' : lC='E'; break;
        case 'उ' : lC='U'; break;
        case 'ऊ' : lC='OO'; break;
        case 'ओ' : lC='O'; break;
        case 'ऋ' : lC='RI'; break;
        case 'ृ' : lC='Ri'; break;
        case 'र्‍' : lC='R'; break;
        case 'ा' : lC='aa'; break;
        case 'ै' : lC='ai'; break;
        case 'ौ' : lC='ao'; break;
        case 'ॅ' : lC='ae'; break;
        case 'ॉ' : lC='aw'; break;
        case 'ि' : lC='i'; break;
        case 'ी' : lC='ee'; break;
        case 'े' : lC='e'; break;
        case 'ु' : lC='u'; break;
        case 'ू' : lC='oo'; break;
        case 'ो' : lC='o'; break;
        case 'ख' : da=true; if (nC2=='़') { lC='Kh'; i++; break;} lC='kh'; break;
        case 'क' : da=true; if (nC2=='़') { lC='Q'; i++; break;} lC='k'; break;
        case 'घ' : da=true; lC='gh'; break;
        case 'ग' : da=true; if (nC2=='़') { lC='G'; i++; break;} lC='g'; break;
        case 'छ' : da=true; lC='chh'; break;
        case 'च' : da=true; lC='ch'; break;
        case 'झ' : da=true; lC='jh'; break;
        case 'ज' : da=true;
            if (nC2=='़') { lC='Z'; i++; break;}
            if ((nC2=='्') && (nC3=='ञ')) { da=false; lC='gNy'; i+=2; break;}
            lC='j'; break;
        case 'ठ' : da=true; lC='Th'; break;
        case 'ट' : da=true; lC='T'; break;
        case 'ढ' : da=true;
            if (nC2=='़') { lC='Ddh'; i++; break;}
            lC='Dh'; break;
        case 'ड' : da=true;
            if (nC2=='़') { lC='Dd'; i++; break;}
            lC='D'; break;
        case 'थ' : da=true; lC='th'; break;
        case 'त' : da=true; lC='t'; break;
        case 'ध' : da=true; lC='dh'; break;
        case 'द' : da=true; lC='d'; break;
        case 'फ' : da=true;
            if (nC2=='़') { lC='F'; i++; break;}
            lC='ph'; break;
        case 'प' : da=true; lC='p'; break;
        case 'भ' : da=true; lC='bh'; break;
        case 'ब' : da=true; lC='b'; break;
        case 'य' : da=true; lC='y'; break;
        case 'र' : da=true; lC='r'; break;
        case 'ल' : da=true; lC='l'; break;
        case 'व' : da=true; lC='v'; break;
        case 'श' : da=true; lC='sh'; break;
        case 'स' : da=true; lC='s'; break;
        case 'ष' : da=true; lC='Sh'; break;
        case 'ह' : da=true; lC='h'; break;
        case 'म' : da=true; lC='m'; break;
        case 'न' : da=true; lC='n'; break;
        case 'ङ' : da=true; lC='NG'; break;
        case 'ञ' : da=true; lC='NJ'; break;
        case 'ण' : da=true; lC='NN'; break;
        case 'ढ़' : da=true; lC='Ddh'; break;
        case 'ड़' : da=true; lC='Dd'; break;
        case 'ज़' : da=true; lC='J'; break; // it was 'Z'
        case 'फ़' : da=true; lC='F'; break;
        case 'ख़' : da=true; lC='Kh'; break;
        case 'ग़' : da=true; lC='G'; break;
        case 'क़' : da=true; lC='Q'; break;
        case 'ळ' : da=true; lC='L'; break;
        case 'ँ' : lC='Nn'; break;
        case 'ं' : lC='N'; break;
        case '।' : lC=';;'; break;
        case '\r' : lC=nC1;
            if (nC2=='\n') { lC='\r\n'; i++; }
            break;
        default: lC=nC1;
    }
    if (da==true) {
        if (nC2=='़') nC2=nC3;
switch(nC2) {

    case 'ृ' : 
    case 'ा' : 
    case 'ै' : 
    case 'ौ' : 
    case 'ॅ' : 
    case 'ॉ' : 
    case 'ि' : 
case 'ी' :case 'े' : case 'ु' : case 'ू' : case 'ो' : 
    da=false; break;
case '्' :
    da=false; i++; break;
// when word ends
case ' ' : case ',' : case '.' : case '।' : case '\r' : case ')' : case ']' :case '\t' : 
    if ( (nC1=='य') || (nC1=='र') ) break; /* else */ da=false;         // || (nC1=='ञ')  already taken care of
}
}

document.f.lOut.value +=lC;

if (da==true) {

document.f.lOut.value += 'a';
da=false;

}
}
}
