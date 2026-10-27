#!/usr/bin/env python3
"""Prepare supplied user transcriptions. Run manually; builds need no API.

Usage: python scripts/prepare-rashash.py /absolute/upload/directory /absolute/cache
Dicta's rabbinic Nakdan supplies proposed vowels, never text.
Every source letter, original vowel, space and punctuation mark is retained.
"""
import argparse
from datetime import date
from collections import Counter
from difflib import SequenceMatcher
from hashlib import sha256
from html import escape
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET

from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent.parent
ENDPOINT = 'https://nakdan-u2-1a.loadbalancer.dicta.org.il/api'
VERSION = '2026-10-25-rabbinic-v1'
MARK = re.compile('[\u0591-\u05af\u05b0-\u05bd\u05bf\u05c1\u05c2\u05c4\u05c5\u05c7]')
WORD = re.compile('[\u05d0-\u05ea][\u05d0-\u05ea\u0591-\u05c7]*(?:["\'״׳][\u05d0-\u05ea\u0591-\u05c7]*)*')
PAGE = re.compile(r'━+\s+(?:דף )?(.*?)\s+\(PDF (\d+)\)\s+━+')
TABLE_MARKERS = re.compile(r'(?:=== (?:סוף )?טבלה ===)+')
TABLE_TOKEN = re.compile(r'=== (?:סוף )?טבלה ===')
SACRED = {'יהוה','אהיה','אדני','אלהים','אלהינו','אלהיכם','אלוהינו','הויה',
          'יאהדונהי','יאההויהה','איההיוהה','יהו','הוי','ויה','יוה','היו','והי',
          'אבגיתץ','קרע','שטן','נגד','יכש','בטר','צתג','חקב','טנע','יגל','פזק',
          'שקו','צית','אלף','יוד','הי','הא','הה','וו','ואו','ויו','דלת',
          'אל','אלוה','אלהי','שדי','צבאות','צבאו','אכדטם','אילההויהם','מנצפך',
          'יהאהלוההים','יאההוהה','יאהדונהי','דינא','דיאנ','נאדי','נאיד','נדאי',
          'יה','יו','הו','וד','או','מצפץ','מצפ','יאאא','דני','אה','אהי','שד','ץיהא',
          'אלם','בוכו','כוזו','במוכסז','למד','שין','מם','נון','צדי','קוף','ריש','תיו',
          'יאהלוההים','יאהי','אאללההייםם','תצמץ','אכתריאל'}
VOLUMES = [
 ('21521',1,'bis_PDF050','Schabbatmorgen · Birkhot haSchachar, Korbanot und Pesukei deZimra · HB21521',231),
 ('21375',2,'bis_PDF050','Werktagsgebete · Hodu und Pesukei deZimra · bis PDF 50',323),
 ('21519',3,'Erev_Schabbat','Erev Schabbat · Kabbalat Schabbat & Arvit · HB21519',73),
 ('21520',3,'Erev_Schabbat','Erev Schabbat · Kabbalat Schabbat & Arvit',73),
 ('21518',6,'Schawuot','Schawuot · Lernen in der Nacht, Schacharit & Musaf',25),
 ('21721',7,'bis_PDF050','Rosch HaSchana · Schema und Amida-Kavvanot · HB21721',209),
 ('21722',8,'Jom_Kippur','Jom Kippur · Gebete, Kavvanot & Seder haAvoda',139),
 ('21723',9,'Sukkot','Sukkot · Na’anuim, Hallel, Hakafot & Hoschana Rabba',43),
]
STAGED_VOLUMES = {'21375':323,'21521':231,'21721':209}
HB21375_EXTRA_NAMES = frozenset({'בם','פאי','חתך','אט','אכפץ','אכנסם','טדהד',
    'אידהנויה','קרעשטן','נגדיכש','בטרצתג','חקבטנע','יגלפזק','שקוצית',
    'יההווההו','יאי','יהה','משסג','ההה','האהיה','ואהיהו','יאהלהוהים'})
HB21521_EXTRA_NAMES = frozenset({'אאלל','אידהנויה','חתך','סאל','במוכן','ינעם',
    'יההווההו','האהיה','ואהיהו','האה'})

def hb21521_symbol_offsets(line,page):
    """Names above Shema words and explicit bracketed letter diagrams."""
    offsets=set()
    for bracket in re.finditer(r'\[([^\[\]]+)\]',line):
        content=bracket[1].strip().rstrip('.')
        words=content.split()
        diagram=bool(words and words[0] in {'הו','הוה','יהו'} and len(words)>5
                     and re.fullmatch('[א-ת ]+',content))
        shema=bool(101<=page<=118 and not line.startswith('[') and words
                   and all(1<=len(w)<=3 for w in words) and re.fullmatch('[א-ת ]+',content))
        if diagram or shema:
            offsets.update(bracket.start(1)+word.start() for word in WORD.finditer(bracket[1]))
    return offsets

def hb21721_name_line(line,page):
    """Preserve explicit name annotations and diagram rows from this source."""
    if line.startswith(('[שמות ','[מעל התיב','[מעל כל תיבה:','[ציור:')):return True
    if 19<=page<=25 and source_name_line(line):return True
    if 19<=page<=25 and line in {'[יחי]','[מנה]','[חהו]','[נקם]'}:return True
    return hb21375_name_line(line) or line in {'יה ריו','רו'}

def hb21721_symbol_offsets(line):
    offsets=set()
    for prefix,token in [('ברוך — ','יא'),('אתה — ','יא'),("זקיפה ב' — ",'אי')]:
        if line.startswith(prefix+token+' '):offsets.add(len(prefix))
    for sequence in re.finditer('וד י ין י',line):
        offsets.update(sequence.start()+word.start() for word in WORD.finditer(sequence[0]))
    return offsets

def hb21721_readings(original):
    """Ordinary prayer words which coincide with protected name combinations."""
    readings={}
    if original.startswith(('והיו הדברים','והיו לטטפת','אתם לאות על ידכם והיו','וביום שמחתכם')):
        readings['והיו']='וְהָיוּ'
    if original.startswith(('והיה אם שמע','והיה לכם לציצת')) or 'ואז הדין נמתק והיה יגיד' in original:
        readings['והיה']='וְהָיָה'
    if original.startswith('והיה אם שמע'):readings['אל']='אֶל'
    return readings

def hb21375_name_line(line):
    """Recognize standalone diagram rows, not short prayer phrases."""
    text=bare(line).strip();words=text.split()
    if text in {'מם כף קץ','דין דין דין דין דין','שן אלף למד הה יוד מם אדני',
                'לל שיד הויה','לל שיד הויה עבד ב׳','שך פר'}:return True
    if not re.fullmatch('[א-ת ]+',text):return False
    if len(words)>=2 and len(words[0])==1 and all(len(w)<=4 for w in words):return True
    if text=='לף י וד י':return True
    return False

def hb21375_symbol_word(original,offset):
    return original=='טובך יד י אן י' and offset>=len('טובך ')

FLAGS = [
 {'volume':'21521','pdfPages':[45,46],'kind':'possible_source_repetition',
  'note':'Die Gottesnamenfolge am Ende von PDF 45 erscheint erneut vor סביב ליראיו auf PDF 46. Beide Vorkommen der Vorlage bleiben erhalten; möglichen Seitenanschluss am Scan prüfen.'},
 {'volume':'21521','pdfPages':[47],'kind':'possible_source_repetition',
  'quote':'כי כלינו באפך ובחמתך נבהלנו: שתה עונתינו לנגדך עלמנו למאור פניך:',
  'note':'Die Vorlage wiederholt diese beiden Sätze aus Psalm 90 unmittelbar. Beide Vorkommen bleiben erhalten; mögliche Dopplung am Scan prüfen.'},
 {'volume':'21520','pdfPages':[1],'kind':'transcription_typo','quote':'בשער פקרי הצלם',
  'note':'Im Scan steht בשער פרקי הצלם. Die hochgeladene Buchstabenfolge bleibt erhalten; zur Korrektur markiert.'},
 {'volume':'21520','pdfPages':[19],'kind':'missing_source_niqqud','quote':'[בניקוד הנדפס תחת האותיות]',
  'note':'Zwei Tabellenzeilen haben einen Platzhalter statt des gedruckten Niqqud. Die Originalpunktierung muss noch aus dem Scan übertragen werden.'},
 {'volume':'21518','pdfPages':[1,3],'kind':'page_anchor_imprecision',
  'note':'Die Fußnote unter PDF 1 setzt sich unter PDF 3 fort. In der gelieferten Transkription steht die gesamte Fußnote bei PDF 1.'},
 {'volume':'21723','pdfPages':[43],'kind':'omitted_footnote',
  'note':'Die untere Schlussfußnote und die Unterschriften fehlen in der gelieferten Transkription. Im Scan nachlesen; nicht aus dem Sprachmodell ergänzt.'},
]

def bare(s):
    return MARK.sub('',s)

def letters(s):
    return ''.join(re.findall('[א-ת]',s))

def protected(token,extra_sacred=()):
    b=bare(token)
    sacred=SACRED.union(extra_sacred) if extra_sacred else SACRED
    if any(c in b for c in '\'"״׳'):
        return 'abbr'
    if b in sacred or any(b.startswith(p) and b[len(p):] in sacred for p in ['ב','ל','כ','מ','ו','ה','ד','וב','ול','של','וה','וד','דה','דב','לה','בה']):
        return 'shem'
    if MARK.search(token):
        return 'source_pointing'
    if len(b)==1:
        return 'letter'
    return None

def graft(original, candidate):
    """Copy only vowel marks; never allow a model to change consonants."""
    units=[]
    for c in candidate.replace('|',''):
        if re.match('[א-ת]',c): units.append([c,''])
        elif MARK.fullmatch(c) and units: units[-1][1]+=c
    base=letters(original); predicted=''.join(x[0] for x in units)
    added={}
    if base==predicted:
        mapping={i:i for i in range(len(base))}
    else:
        # Dicta can omit matres in pointed spelling. Keep every original letter.
        sm=SequenceMatcher(None,base,predicted,autojunk=False)
        mapping={}
        for tag,i,j,k,l in sm.get_opcodes():
            if tag=='equal': mapping.update({a:k+a-i for a in range(i,j)})
            elif tag!='delete' or any(c not in 'וי' for c in base[i:j]):
                return original,False
        for index,char in enumerate(base):
            if char=='ו' and index not in mapping and index-1 in mapping:
                prior=units[mapping[index-1]][1]
                if '\u05b9' in prior:
                    units[mapping[index-1]][1]=prior.replace('\u05b9','');added[index]='\u05b9'
                elif '\u05bb' in prior:
                    units[mapping[index-1]][1]=prior.replace('\u05bb','');added[index]='\u05bc'
    result=[];i=0
    for c in original:
        result.append(c)
        if re.match('[א-ת]',c):
            if i in mapping: result.append(units[mapping[i]][1])
            if i in added: result.append(added[i])
            i+=1
    # Keep plene ו in its usual pointed spelling: חוֹל, not חֹוֽל. This
    # normalization only affects proposed marks; protected source words bypass it.
    result=''.join(result)
    result=re.sub(r'([א-ת])([\u05b0-\u05c7]*)ו([\u05bd]*)(?![\u05b0-\u05bd\u05bf\u05c1\u05c2\u05c7])',
      lambda m:m[1]+m[2].replace('\u05b9','')+'ו\u05b9'+m[3] if '\u05b9' in m[2] else m[0],result)
    return result,True

def call_nakdan(text,cache):
    key=sha256((VERSION+text).encode()).hexdigest();p=cache/(key+'.json')
    if p.exists(): return json.loads(p.read_text())
    payload={'task':'nakdan','genre':'rabbinic','data':text,
      'addmorph':True,'keepmetagim':True,'keepqq':False,'matchpartial':True,
      'nodageshdefmem':True,'patachma':False,'useTokenization':True}
    request=Request(ENDPOINT,data=json.dumps(payload).encode(),headers={'Content-Type':'application/json'})
    with urlopen(request,timeout=55) as response:
        body=json.load(response)
    if not isinstance(body,dict) or not isinstance(body.get('data'),list):
        raise ValueError('Unexpected Nakdan response')
    # Retain a small reproducible research cache, outside the Git repository.
    data=[{'str':x.get('str',''),'options':[o['w'] for o in x.get('nakdan',{}).get('options',[])],
           'confident':x.get('nakdan',{}).get('fconfident',False)} for x in body['data']]
    p.write_text(json.dumps(data,ensure_ascii=False));return data

def vocalize_chunk(text,cache,stats,extra_sacred=()):
    data=call_nakdan(text,cache)
    tokens=[m for m in WORD.finditer(text)]
    # Align through echoed Hebrew letters, not through the generated text.
    expected=letters(text); echoed=''.join(letters(x['str']) for x in data)
    if expected!=echoed:
        raise ValueError('Nakdan echoed a changed consonantal sequence; aborting')
    predictions=[]
    for item in data:
        if not letters(item['str']): continue
        chosen=item['options'][0] if item['options'] else item['str']
        new,ok=graft(item['str'],chosen)
        predictions.extend([(c,marks) for c,marks in char_units(new)])
    if ''.join(c for c,_ in predictions)!=expected:
        raise ValueError('Prediction alignment failed')
    offsets={};pos=0
    for m in tokens:
        count=len(letters(m.group()));offsets[m.start()]=(pos,count);pos+=count
    out=[];last=0
    for m in tokens:
        out.append(text[last:m.start()]);word=m.group();reason=protected(word,extra_sacred)
        if reason:
            stats['protected_'+reason]+=1;out.append(word)
        else:
            start,count=offsets[m.start()]
            candidate=''.join(c+v for c,v in predictions[start:start+count])
            changed,ok=graft(word,candidate)
            if not ok: stats['unaligned_words']+=1
            if changed!=word: stats['words_with_added_niqqud']+=1
            out.append(changed)
        last=m.end()
    out.append(text[last:]);result=''.join(out)
    assert bare(result)==bare(text)
    return result

def char_units(s):
    units=[]
    for c in s:
        if re.match('[א-ת]',c): units.append([c,''])
        elif MARK.fullmatch(c) and units: units[-1][1]+=c
    return units

def prayer_phrases():
    """Exact consonantal phrases from the supplied pointed Siddur, not a new nusach."""
    source=(ROOT/'Shaliehsaboo Edition.txt').read_text()
    source=re.sub(r'<small>.*?</small>',' ',source,flags=re.S)
    source=re.sub(r'<[^>]+>',' ',source).replace('־',' ')
    words=[m.group() for m in WORD.finditer(source)]
    indexes={n:{} for n in range(3,11)}
    for n,index in indexes.items():
        for i in range(len(words)-n+1):
            phrase=tuple(words[i:i+n]);key=tuple(bare(w) for w in phrase)
            if not all(MARK.search(w) or protected(w) for w in phrase):continue
            if key not in index:index[key]=phrase
            elif index[key]!=phrase:index[key]=None
    return indexes

def refine_prayer_line(original,pointed,indexes,stats,niqqud_only=False,extra_sacred=()):
    source=list(WORD.finditer(original));result=[m.group() for m in WORD.finditer(pointed)]
    keys=[bare(m.group()) for m in source];replaced=set()
    for n in reversed(indexes):
        for i in range(len(source)-n+1):
            phrase=indexes[n].get(tuple(keys[i:i+n]))
            if not phrase:continue
            for j,word in enumerate(phrase,i):
                if j in replaced or protected(source[j].group(),extra_sacred):continue
                if niqqud_only:word=re.sub('[\u0591-\u05af]','',word)
                value,ok=graft(source[j].group(),word)
                if ok and MARK.search(value):
                    result[j]=value;replaced.add(j)
    # Disambiguations confirmed against the visible liturgical context. No letters
    # are corrected here, including a source's plene/defective spelling.
    corrections={'קדשנו':'קִדְּשָׁנוּ','השבעות':'הַשָּׁבֻעוֹת','האמות':'הָאֻמּוֹת'}
    for i,key in enumerate(keys):
        if key in corrections and not protected(source[i].group(),extra_sacred):
            result[i],ok=graft(source[i].group(),corrections[key]);replaced.add(i)
    # HB21722 PDF99: visually checked imperative. The later מֹחֶה quotation
    # has a different grammatical form and must not be globally overwritten.
    if 'מחה והעבר פשענו מנגד עיניך' in original:
        if 'מחול' in keys:
            i=keys.index('מחול');result[i],ok=graft(source[i].group(),'מְחוֹל')
        for i in range(len(keys)-4):
            if keys[i:i+5]==['מחה','והעבר','פשענו','מנגד','עיניך']:
                for j,candidate in enumerate(['מְחֵה','וְהַעֲבֵר','פְשָׁעֵנוּ','מִנֶּגֶד','עֵינֶיךָ'],i):
                    if not MARK.search(source[j].group()):result[j],ok=graft(source[j].group(),candidate)
    chunks=[];last=0
    for m,value in zip(WORD.finditer(pointed),result):
        chunks.extend([pointed[last:m.start()],value]);last=m.end()
    chunks.append(pointed[last:]);stats['words_with_siddur_phrase_reference']+=len(replaced)
    return ''.join(chunks)

def hb21519_readings(original):
    """Contextual readings checked during review of this new working edition."""
    readings={}
    if original.startswith('בואו ונצא'):
        readings['בואו']='בּוֹאוּ'
    if 'שם יה או"א בוה זו"ן' in original:
        readings['בוה']='בוה' # Symbolic combination, not an ordinary word.
    if 'וישים לנגד עיניו' in original:
        readings['לנגד']='לְנֶגֶד'
    if 'והיו הדברים' in original or 'והיו [א]' in original:
        readings['והיו']='וְהָיוּ'
    if 'והיה לכם' in original:
        readings['והיה']='וְהָיָה'
    if original.startswith('לשם יחוד קודשא'):
        readings.update({'שורשה':'שׁוֹרְשָׁהּ','קבל':'קַבֵּל'})
    if 'וגלה יקרנו' in original:
        readings.update({'וגלה':'וְגָלָה','יקרנו':'יְקָרֵנוּ','ונטל':'וְנִטַּל'})
    if original.startswith('אתם [א]') or 'ולמדתם [א] אתם [ה]' in original or original.startswith('אתם ולא תתורו'):
        readings['אתם']='אֹתָם'
    return readings

def refine_hb21519_line(original,pointed):
    readings=hb21519_readings(original)
    old=list(WORD.finditer(original));new=list(WORD.finditer(pointed));changes=[]
    for a,b in zip(old,new):
        if a.group() in readings and not MARK.search(a.group()):
            value,ok=graft(a.group(),readings[a.group()]);assert ok
            changes.append((b.start(),b.end(),value))
    for start,end,value in reversed(changes):
        pointed=pointed[:start]+value+pointed[end:]
    return pointed

def refine_hb21521_line(original,pointed):
    """The annotated Shema passage refers to commandments, not matzot."""
    if 'מצות [יין]' not in original:return pointed
    changes=[]
    for a,b in zip(WORD.finditer(original),WORD.finditer(pointed)):
        if a.group()=='מצות':
            value,ok=graft(a.group(),'מִצְוֹת');assert ok
            changes.append((b.start(),b.end(),value))
    for start,end,value in reversed(changes):pointed=pointed[:start]+value+pointed[end:]
    return pointed

def refine_hb21721_line(original,pointed):
    readings=hb21721_readings(original);changes=[]
    for a,b in zip(WORD.finditer(original),WORD.finditer(pointed)):
        if a.group() in readings:
            value,ok=graft(a.group(),readings[a.group()]);assert ok
            changes.append((b.start(),b.end(),value))
    for start,end,value in reversed(changes):pointed=pointed[:start]+value+pointed[end:]
    return pointed

def inline_xml(text,original,names_line=False,volume=None,extra_sacred=(),symbol_offsets=()):
    """Protected names and original pointing are independently addressable."""
    orig=list(WORD.finditer(original));now=list(WORD.finditer(text))
    assert len(orig)==len(now)
    out=[];last=0
    for a,b in zip(orig,now):
        out.append(escape(text[last:b.start()]));tag=protected(a.group(),extra_sacred)
        if a.start() in symbol_offsets:tag='shem'
        if volume=='21721' and a.group() in hb21721_readings(original):tag=None
        if volume=='21375' and extra_sacred and hb21375_symbol_word(original,a.start()):tag='shem'
        if volume=='21519' and a.group() in hb21519_readings(original):
            tag='shem' if a.group()=='בוה' else None
        # HB21519 explicitly labels the names placed above the Shema words.
        # Even ordinary-looking combinations such as אני remain source names.
        if names_line and a.start() > original.find(':'):
            tag='shem'
        if tag=='shem' and bare(a.group())=='מנגד' and 'מחה והעבר פשענו מנגד עיניך' in original:
            tag=None # Verified ordinary preposition, not the name נג״ד יכ״ש.
        if tag:
            assert a.group()==b.group()
            attrs=' recite="false"' if tag in ['shem','letter'] else ''
            out.append(f'<{tag}{attrs}>{escape(b.group())}</{tag}>')
        else: out.append(escape(b.group()))
        last=b.end()
    out.append(escape(text[last:]));return ''.join(out).replace('[?]','<unclear reason="source-transcription">[?]</unclear>')

def source_name_line(line):
    """Recognize explicit Shema name lists, without classifying prayer prose."""
    if line.startswith('[שמות '):
        return True
    if not (line.startswith('[') and line.endswith(']')):
        return False
    content=line[1:-1].replace('—',' ').strip()
    return bool(re.fullmatch(r'[א-ת ]+',content)) and len(content.split())>=2 and all(2<=len(w)<=3 for w in content.split())

def reusable_pointing(lines,previous):
    """Reuse existing pointed lines only on unchanged source pages."""
    if not previous:return {},0,{}
    oldlines=(ROOT/previous['sourcePath']).read_text().splitlines()
    def spans(source):
        starts=[(i,int(m[2])) for i,line in enumerate(source) if (m:=PAGE.fullmatch(line))]
        return {number:(start,starts[j+1][0] if j+1<len(starts) else len(source)) for j,(start,number) in enumerate(starts)}
    oldspans,newspans=spans(oldlines),spans(lines)
    reused={};markup={};count=0
    oldmarkup={int(m[2])-1:m[3] for m in re.finditer(
        r'<(p|heading|row) [^>]*source-line="(\d+)"[^>]*>(.*?)</\1>',
        (ROOT/previous['txtPath']).read_text())}
    for page in ET.parse(ROOT/previous['txtPath']).getroot().findall('page'):
        number=int(page.get('pdf'))
        if number not in newspans:continue
        a,b=oldspans[number];c,d=newspans[number]
        if '\n'.join(oldlines[a:b]).rstrip()!= '\n'.join(lines[c:d]).rstrip():continue
        count+=1
        for node in page.iter():
            if node.tag not in {'p','heading','row','lb'}:continue
            oldindex=int(node.attrib['source-line'])-1;newindex=c+oldindex-a
            assert oldlines[oldindex]==lines[newindex]
            reused[newindex]=''.join(node.itertext())
            if oldindex in oldmarkup:markup[newindex]=oldmarkup[oldindex]
    return reused,count,markup

def main():
    ap=argparse.ArgumentParser();ap.add_argument('input',type=Path);ap.add_argument('cache',type=Path);ap.add_argument('--volume',choices=[v[0] for v in VOLUMES]);ap.add_argument('--through-pdf',type=int);args=ap.parse_args()
    if args.volume in STAGED_VOLUMES and (args.through_pdf is None or not 3<=args.through_pdf<=STAGED_VOLUMES[args.volume]):
        ap.error(f'HB{args.volume} requires --through-pdf between 3 and {STAGED_VOLUMES[args.volume]} matching the supplied transcription.')
    if args.through_pdf is not None and args.volume not in STAGED_VOLUMES:
        ap.error('--through-pdf requires a supported staged volume.')
    args.cache.mkdir(parents=True,exist_ok=True)
    output=ROOT/'texts/rashash';(output/'sources').mkdir(parents=True,exist_ok=True)
    docs=json.loads((ROOT/'data/rashash.json').read_text())
    summaries={v['id']:v for v in docs.get('transcriptions',{}).get('volumes',[])};phrase_index=prayer_phrases()
    all_flags=json.loads((ROOT/'data/rashash-text-audit.json').read_text())['flags'];superseded=[]
    for ident,part,slug,title,total in VOLUMES:
        if args.volume and ident!=args.volume:continue
        if ident in STAGED_VOLUMES and args.through_pdf is None:continue
        imported_total=args.through_pdf if ident in STAGED_VOLUMES else total
        if ident in STAGED_VOLUMES:
            slug=f'bis_PDF{imported_total:03}'
            title=(f'Werktagsgebete · Hodu und Pesukei deZimra · bis PDF {imported_total}' if ident=='21375' else title+f' · bis PDF {imported_total}')
            if ident=='21521' and imported_total==total:title=f'Schabbat · Schacharit, Musaf und Mincha · HB21521 · bis PDF {total}'
        if ident in STAGED_VOLUMES:
            candidates=[p for p in args.input.glob(f'*HB{ident}_bis_PDF*.txt')
                        if (match:=re.search(r'_bis_PDF(\d+)\.txt$',p.name)) and int(match[1])==imported_total]
            assert len(candidates)==1, f'Expected exactly one HB{ident} source through PDF {imported_total}'
            source=candidates[0]
        else:source=next(args.input.glob('*HB'+ident+'*.txt'))
        raw=source.read_text();lines=raw.splitlines()
        previous=summaries.get(ident)
        reused,reused_pages,reused_markup=reusable_pointing(lines,previous) if ident in STAGED_VOLUMES else ({},0,{})
        extra_names=HB21375_EXTRA_NAMES if ident=='21375' and imported_total>=200 else HB21521_EXTRA_NAMES if ident=='21521' else frozenset({'רו','ריו'}) if ident=='21721' else ()
        volume_flags=[f for f in FLAGS if f['volume']==ident]
        if ident in ('21375','21521','21721','21519','21722'):
            uncertain={};current_page=0
            for line_no,line in enumerate(lines,1):
                marker=PAGE.fullmatch(line)
                if marker:current_page=int(marker[2])
                if current_page and '[?]' in line:uncertain.setdefault(current_page,[]).append({'line':line_no,'count':line.count('[?]')})
            for number,places in uncertain.items():
                count=sum(p['count'] for p in places)
                volume_flags.append({'volume':ident,'pdfPages':[number],'kind':'source_uncertainty',
                  'sourceLines':[p['line'] for p in places],'occurrences':count,
                  'note':f'Die gelieferte Transkription markiert hier {count} unsichere Lesart(en) mit [?] (Quellzeile(n) '+', '.join(str(p['line']) for p in places)+'). Die Markierungen und die unmittelbar davor stehenden Wörter bleiben erhalten; am Scan prüfen.'})
        if ident=='21521' and imported_total==231 and 'Noch nicht enthalten: PDF 201–231.' in raw[:2000]:
            volume_flags.append({'volume':ident,'pdfPages':[1],'kind':'source_header_coverage_mismatch',
                'note':'Der unverändert erhaltene Quellvorspann nennt noch PDF 1–200 und fehlende PDF 201–231. Tatsächlich enthält die Datei PDF 1 und 3–231, insgesamt 230 Textseiten. Die Abdeckungsmetadaten richten sich nach den vorhandenen Seitenmarkierungen.'})
        if ident=='21722':
            volume_flags.append({'volume':ident,'pdfPages':[132],'kind':'service_cross_reference',
              'note':'Der Hinweis zu Mincha und Neila verweist auf bereits erklärte gemeinsame Kavvanot. Diese Seite ist kein eigenständiger vollständiger Neila-Gebetstext.'})
            volume_flags.append({'volume':ident,'pdfPages':[3,4],'kind':'page_anchor_imprecision',
              'note':'Die Fußnote beginnt unter PDF 3 und setzt sich unter PDF 4 fort. In der gelieferten Transkription steht die gesamte Fußnote einschließlich Unterschriften unter PDF 3.'})
            volume_flags.append({'volume':ident,'pdfPages':[128,129,130],'kind':'uncertain_source_pointing',
              'note':'Mehrere Gottesnamen und ihre besondere Punktierung sind mit [?] markiert. Die Originalzeichen bleiben erhalten; keine Namenpunktierung aus dem Sprachmodell rekonstruiert.'})
            volume_flags.append({'volume':ident,'pdfPages':[132],'kind':'uncertain_name_combination',
              'note':'Die mit [?] markierte Buchstabenkombination אאללההייםם bleibt unverändert. Die Lesart ist am Originalscan zu prüfen.'})
        all_flags=[f for f in all_flags if f['volume']!=ident]+volume_flags
        first=next(i for i,x in enumerate(lines) if PAGE.fullmatch(x));prefix=lines[:first]
        if ident in STAGED_VOLUMES and imported_total<total:
            volume_flags.append({'volume':ident,'pdfPages':[1],'kind':'partial_transcription',
                'note':f'Teilfassung: PDF 1 und 3–{imported_total} von {total} Scan-Seiten. PDF 2 ist ausgelassen. Ab PDF {imported_total+1} ist noch kein transkribierter Text enthalten.'})
            all_flags=[f for f in all_flags if f['volume']!=ident]+volume_flags
        stats=Counter();newlines=lines.copy();chunks=[];indices=[];size=0;table_depth=0;table_lines=set();name_lines=set();number_lines=set();symbol_offsets={};source_page=0
        if reused:
            stats['reused_pages']=reused_pages;stats['reused_source_lines']=len(reused)
            for n,value in reused.items():newlines[n]=value
        for n in range(first,len(lines)):
            if marker:=PAGE.fullmatch(lines[n]):source_page=int(marker[2])
            # Names in diagrams are not ordinary words. Keep whole tables, even
            # their labels, exactly as supplied; do not infer missing pointing.
            if TABLE_MARKERS.fullmatch(lines[n]):
                for token in TABLE_TOKEN.findall(lines[n]):
                    table_depth+=1 if token=='=== טבלה ===' else -1
                    assert table_depth>=0, f'Orphan table close at line {n+1}'
                continue
            if PAGE.fullmatch(lines[n]):assert table_depth==0, f'Table crosses page at line {n+1}'
            if table_depth:
                stats['table_lines_preserved']+=1;table_lines.add(n)
            if ident=='21519' and not table_depth and source_name_line(lines[n]):
                name_lines.add(n);stats['source_name_lines_preserved']+=1
            if ident=='21375' and extra_names and n not in reused and not table_depth and hb21375_name_line(lines[n]):
                name_lines.add(n);stats['source_name_lines_preserved']+=1
            if ident=='21521' and n not in reused and not table_depth:
                offsets=hb21521_symbol_offsets(lines[n],source_page)
                if offsets:symbol_offsets[n]=offsets
                whole_name_line=hb21375_name_line(lines[n]) or lines[n] in {'א אל אלה אלהי אלהים','יהו ינעם'}
                if whole_name_line or (offsets and offsets=={w.start() for w in WORD.finditer(lines[n])}):
                    name_lines.add(n);stats['source_name_lines_preserved']+=1
            if ident=='21721' and n not in reused and not table_depth:
                offsets=hb21721_symbol_offsets(lines[n])
                if offsets:symbol_offsets[n]=offsets
                if hb21721_name_line(lines[n],source_page):
                    name_lines.add(n);stats['source_name_lines_preserved']+=1
            if ident=='21521' and not table_depth and lines[n] in ('א','ב','ג','ד','ה','ו','ז','ח','ט','י','יא','יב','יג'):
                number_lines.add(n);stats['source_number_lines_preserved']+=1
            # Structural delimiters remain source text; only textual lines sent.
            if n in reused or (ident in STAGED_VOLUMES and (n in table_lines or n in name_lines or n in number_lines)) or PAGE.fullmatch(lines[n]) or lines[n].startswith('===') or not letters(lines[n]):continue
            if size+len(lines[n])>5500 and indices:chunks.append(indices);indices=[];size=0
            indices.append(n);size+=len(lines[n])+1
        assert table_depth==0, 'Unclosed source table'
        if indices:chunks.append(indices)
        for i,indices in enumerate(chunks):
            text='\n'.join(lines[n] for n in indices)
            result=vocalize_chunk(text,args.cache,stats,extra_sacred=extra_names).split('\n')
            assert len(result)==len(indices)
            for n,value in zip(indices,result):
                if n not in table_lines and n not in name_lines:
                    value=refine_prayer_line(lines[n],value,phrase_index,stats,niqqud_only=ident in STAGED_VOLUMES,extra_sacred=extra_names)
                    if ident=='21519':value=refine_hb21519_line(lines[n],value)
                    if ident=='21521':value=refine_hb21521_line(lines[n],value)
                    if ident=='21721':value=refine_hb21721_line(lines[n],value)
                    # Do not settle a word which the transcriber marked uncertain.
                    old_words=list(WORD.finditer(lines[n]));new_words=list(WORD.finditer(value))
                    replacements=[]
                    for a,b in zip(old_words,new_words):
                        if re.match(r'\s*\[\?\]',lines[n][a.end():]) or a.start() in symbol_offsets.get(n,()) or (extra_names and hb21375_symbol_word(lines[n],a.start())):replacements.append((b.start(),b.end(),a.group()))
                    for start,end,original_word in reversed(replacements):value=value[:start]+original_word+value[end:]
                    newlines[n]=value
            print(f'HB{ident}: {i+1}/{len(chunks)} chunks vocalized',flush=True)
        stats['words_with_added_niqqud']=sum(a.group()!=b.group() for old,new in zip(lines,newlines) for a,b in zip(WORD.finditer(old),WORD.finditer(new)))
        pages=[];page=None;table=None;table_stack=[];blocks=[]
        xml=['<?xml version="1.0" encoding="UTF-8"?>',f'<siddur id="HB{ident}" part="{part}" xml:lang="he" schema="azara-rashash-1" niqqud-status="machine-assisted-draft">',
             '<metadata>',f'<title>{escape(title)}</title>',f'<source filename="{escape(source.name,quote=True)}" sha256="{sha256(raw.encode()).hexdigest()}" />',
             '<vocalization engine="Dicta Nakdan" genre="rabbinic" status="editorial-review-required" />',
             *([f'<coverage status="{"partial" if imported_total<total else "complete"}" through-pdf="{imported_total}" scan-pages="{total}" omitted-pdf="2" />'] if ident in STAGED_VOLUMES or imported_total<total else []),
             '<policy>Alle Quellbuchstaben bleiben erhalten. Namen, Abkürzungen, einzelne Buchstaben und vorhandene Punktierung werden nicht automatisch verändert. Ergänztes Niqqud ist kein vollständig am Scan geprüftes Original-Niqqud.</policy>',
             '</metadata>','<transcription_header status="original-before-vocalization">']
        for n,value in enumerate(prefix,1):xml.append(f'<line source-line="{n}">{escape(value)}</line>')
        xml.append('</transcription_header>')
        def close_table():
            nonlocal table
            if table is not None:
                xml.append('</table>')
                if table_stack:
                    child=table;table=table_stack.pop()
                    table['rows'].extend(child['rows'])
                    table.setdefault('nestedTables',[]).extend([
                        {k:child[k] for k in ('id','startLine','endLine')},
                        *child.get('nestedTables',[])])
                else:blocks.append(table);table=None
        def close_page():
            if page is not None:
                assert table is None and not table_stack
                page['blocks']=blocks.copy();pages.append(page.copy());xml.append('</page>')
        for n in range(first,len(lines)):
            orig=lines[n];value=newlines[n];m=PAGE.fullmatch(orig)
            if m:
                close_page();blocks=[];number=int(m[2]);page={'pdfPage':number,'folio':m[1],'flags':[f for f in volume_flags if number in f['pdfPages']]}
                xml.append(f'<page id="HB{ident}-p{number:03}" pdf="{number}" folio="{escape(m[1],quote=True)}" marker="{escape(orig,quote=True)}">')
                for flag in page['flags']:xml.append(f'<review kind="{flag["kind"]}" status="open">{escape(flag["note"])}</review>')
                continue
            identline=f'HB{ident}-L{n+1:04}'
            if TABLE_MARKERS.fullmatch(orig):
                for token in TABLE_TOKEN.findall(orig):
                    if token=='=== טבלה ===':
                        if table is not None:table_stack.append(table)
                        table={'kind':'table','id':identline,'rows':[],'startLine':n+1}
                        xml.append(f'<table id="{identline}" source-line="{n+1}" preserve-layout="true" niqqud="source-only" recite="false">')
                    else:
                        assert table is not None
                        table['endLine']=n+1;close_table()
                continue
            tag='row' if table is not None else 'heading' if orig.strip().startswith('■') else 'p'
            if not orig.strip():
                xml.append(f'<lb source-line="{n+1}" />');continue
            content=reused_markup[n] if n in reused_markup else inline_xml(value,orig,names_line=n in name_lines,volume=ident,extra_sacred=extra_names if n not in reused else (),symbol_offsets=symbol_offsets.get(n,()))
            if n in number_lines:content=f'<number recite="false">{escape(orig)}</number>'
            status='added-draft' if value!=orig else 'source-preserved'
            xml.append(f'<{tag} id="{identline}" source-line="{n+1}" niqqud="{status}">{content}</{tag}>')
            # Only generated, escaped markup; no source HTML is trusted.
            html=re.sub(r'<(shem|abbr|source_pointing|letter|number)(?: recite="false")?>',lambda m:f'<span class="rashash-{m[1]}">',content)
            html=re.sub(r'</(?:shem|abbr|source_pointing|letter|number)>','</span>',html)
            html=html.replace('<unclear reason="source-transcription">','<span class="rashash-unclear" title="Unsichere Lesart der Transkription">').replace('</unclear>','</span>')
            block={'id':identline,'line':n+1,'kind':tag,'text':value,'html':html}
            if table is not None:table['rows'].append(block)
            else:blocks.append(block)
        close_page();xml.append('</siddur>');tagged='\n'.join(xml)+'\n';ET.fromstring(tagged)
        assert [p['pdfPage'] for p in pages]==[1,*range(3,imported_total+1)]
        # Check all original text lines and original protected words byte-for-byte.
        assert all(bare(a)==bare(b) for a,b in zip(lines,newlines))
        name=f'Siddur_HaRashash_Teil_{part}_HB{ident}_{slug}_Niqqud_Tags.txt'
        sourcepath=output/'sources'/f'HB{ident}_Original.txt';sourcepath.write_text(raw)
        (output/name).write_text(tagged)
        entry={'id':ident,'part':part,'title':title,'pages':len(pages),'pdfPages':imported_total,'txtPath':'texts/rashash/'+name,
               'sourcePath':'texts/rashash/sources/'+sourcepath.name,'jsonPath':f'data/rashash-text-{ident}.json',
               'status':'Niqqud-Arbeitsfassung · redaktionell zu prüfen','statistics':dict(stats),'flags':volume_flags}
        if imported_total<total:
            entry.update(coverage={'status':'partial','throughPdf':imported_total,'scanPages':total,'omittedPdfPages':[2]},
                editionNote=f'Teilfassung bis PDF {imported_total} von {total}. Die Fortsetzung ab PDF {imported_total+1} ist nicht enthalten. Niqqud mit Dicta Nakdan im rabbinischen Modus ergänzt; fachliche Prüfung bleibt erforderlich.')
        elif ident in STAGED_VOLUMES:
            entry.update(coverage={'status':'complete','throughPdf':total,'scanPages':total,'omittedPdfPages':[2]},
                editionNote=f'Transkription bis zum Scanende PDF {total}; PDF 2 ist die ausgelassene Stempelseite. Niqqud mit Dicta Nakdan im rabbinischen Modus ergänzt; fachliche Prüfung bleibt erforderlich.')
        if ident=='21521':
            entry['editionNote']+=' Der Dateiname nennt Teil I; der Scan ist im Katalog inhaltlich als Schabbatmorgen, Musaf und Mincha geführt. Eine gedruckte Teilnummer ist nicht verifiziert.'
        (ROOT/entry['jsonPath']).write_text(json.dumps({**entry,'pages':pages},ensure_ascii=False,separators=(',',':'))+'\n')
        if previous and previous['txtPath']!=entry['txtPath']:superseded.append(ROOT/previous['txtPath'])
        summaries[ident]=entry
        doc=next(x for x in docs['documents'] if x['id']==ident);doc['transcription']=entry
        print(json.dumps({'volume':ident,'pages':len(pages),'statistics':dict(stats)},ensure_ascii=False),flush=True)
    ordered=sorted(summaries.values(),key=lambda v:(v['part'],v['id']))
    docs['transcriptions']={'schemaVersion':1,'date':date.today().isoformat(),'volumes':ordered,
      'policy':'Maschinell unterstützte Niqqud-Arbeitsfassungen der hochgeladenen Transkriptionen. Keine vollständige Kollation; Originalscan bleibt maßgebend.'}
    docs['warnings']=[w for w in docs['warnings'] if not w.startswith(('Die gesamte Abfolge','Drei Transkriptionen')) and not re.match(r'\d+ Transkriptionen',w)]
    docs['warnings'].append(f'{len(ordered)} Transkriptionen sind strukturiert und mit zusätzlichem Niqqud erschlossen. Die Gesamtjahresfolge und die ergänzte Punktierung sind nicht vollständig am Scan geprüft; bekannte Lücken tragen Prüfmarkierungen.')
    (ROOT/'data/rashash.json').write_text(json.dumps(docs,ensure_ascii=False,indent=2)+'\n')
    (ROOT/'data/rashash-text-audit.json').write_text(json.dumps({'date':date.today().isoformat(),'flags':all_flags,'volumes':ordered},ensure_ascii=False,indent=2)+'\n')
    for path in superseded:
        assert path.parent==ROOT/'texts/rashash'
        path.unlink(missing_ok=True)

if __name__=='__main__':main()
