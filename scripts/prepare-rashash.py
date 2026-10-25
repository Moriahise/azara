#!/usr/bin/env python3
"""Prepare supplied user transcriptions. Run manually; builds need no API.

Usage: python scripts/prepare-rashash.py /absolute/upload/directory /absolute/cache
Requires requests. Dicta's rabbinic Nakdan supplies proposed vowels, never text.
Every source letter, original vowel, space and punctuation mark is retained.
"""
import argparse
from collections import Counter
from difflib import SequenceMatcher
from hashlib import sha256
from html import escape
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET

import requests

ROOT = Path(__file__).resolve().parent.parent
ENDPOINT = 'https://nakdan-u2-1a.loadbalancer.dicta.org.il/api'
VERSION = '2026-10-25-rabbinic-v1'
MARK = re.compile('[\u0591-\u05af\u05b0-\u05bd\u05bf\u05c1\u05c2\u05c4\u05c5\u05c7]')
WORD = re.compile('[\u05d0-\u05ea][\u05d0-\u05ea\u0591-\u05c7]*(?:["\'״׳][\u05d0-\u05ea\u0591-\u05c7]*)*')
PAGE = re.compile(r'━+\s+דף (.*?)\s+\(PDF (\d+)\)\s+━+')
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
 ('21520',3,'Erev_Schabbat','Erev Schabbat · Kabbalat Schabbat & Arvit',73),
 ('21518',6,'Schawuot','Schawuot · Lernen in der Nacht, Schacharit & Musaf',25),
 ('21722',8,'Jom_Kippur','Jom Kippur · Gebete, Kavvanot & Seder haAvoda',139),
 ('21723',9,'Sukkot','Sukkot · Na’anuim, Hallel, Hakafot & Hoschana Rabba',43),
]
FLAGS = [
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

def protected(token):
    b=bare(token)
    if any(c in b for c in '\'"״׳'):
        return 'abbr'
    if b in SACRED or any(b.startswith(p) and b[len(p):] in SACRED for p in ['ב','ל','כ','מ','ו','ה','ד','וב','ול','של','וה','וד','דה','דב','לה','בה']):
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
    r=requests.post(ENDPOINT,json={'task':'nakdan','genre':'rabbinic','data':text,
      'addmorph':True,'keepmetagim':True,'keepqq':False,'matchpartial':True,
      'nodageshdefmem':True,'patachma':False,'useTokenization':True},timeout=55)
    r.raise_for_status();body=r.json()
    if not isinstance(body,dict) or not isinstance(body.get('data'),list):
        raise ValueError('Unexpected Nakdan response')
    # Retain a small reproducible research cache, outside the Git repository.
    data=[{'str':x.get('str',''),'options':[o['w'] for o in x.get('nakdan',{}).get('options',[])],
           'confident':x.get('nakdan',{}).get('fconfident',False)} for x in body['data']]
    p.write_text(json.dumps(data,ensure_ascii=False));return data

def vocalize_chunk(text,cache,stats):
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
        out.append(text[last:m.start()]);word=m.group();reason=protected(word)
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

def refine_prayer_line(original,pointed,indexes,stats):
    source=list(WORD.finditer(original));result=[m.group() for m in WORD.finditer(pointed)]
    keys=[bare(m.group()) for m in source];replaced=set()
    for n in reversed(indexes):
        for i in range(len(source)-n+1):
            phrase=indexes[n].get(tuple(keys[i:i+n]))
            if not phrase:continue
            for j,word in enumerate(phrase,i):
                if j in replaced or protected(source[j].group()):continue
                value,ok=graft(source[j].group(),word)
                if ok and MARK.search(value):
                    result[j]=value;replaced.add(j)
    # Disambiguations confirmed against the visible liturgical context. No letters
    # are corrected here, including a source's plene/defective spelling.
    corrections={'קדשנו':'קִדְּשָׁנוּ','השבעות':'הַשָּׁבֻעוֹת','האמות':'הָאֻמּוֹת'}
    for i,key in enumerate(keys):
        if key in corrections and not protected(source[i].group()):
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

def inline_xml(text,original):
    """Protected names and original pointing are independently addressable."""
    orig=list(WORD.finditer(original));now=list(WORD.finditer(text))
    assert len(orig)==len(now)
    out=[];last=0
    for a,b in zip(orig,now):
        out.append(escape(text[last:b.start()]));tag=protected(a.group())
        if tag=='shem' and bare(a.group())=='מנגד' and 'מחה והעבר פשענו מנגד עיניך' in original:
            tag=None # Verified ordinary preposition, not the name נג״ד יכ״ש.
        if tag:
            assert a.group()==b.group()
            attrs=' recite="false"' if tag in ['shem','letter'] else ''
            out.append(f'<{tag}{attrs}>{escape(b.group())}</{tag}>')
        else: out.append(escape(b.group()))
        last=b.end()
    out.append(escape(text[last:]));return ''.join(out).replace('[?]','<unclear reason="source-transcription">[?]</unclear>')

def main():
    ap=argparse.ArgumentParser();ap.add_argument('input',type=Path);ap.add_argument('cache',type=Path);ap.add_argument('--volume',choices=[v[0] for v in VOLUMES]);args=ap.parse_args()
    args.cache.mkdir(parents=True,exist_ok=True)
    output=ROOT/'texts/rashash';(output/'sources').mkdir(parents=True,exist_ok=True)
    docs=json.loads((ROOT/'data/rashash.json').read_text())
    summaries={v['id']:v for v in docs.get('transcriptions',{}).get('volumes',[])};phrase_index=prayer_phrases()
    all_flags=[f for v in summaries.values() for f in v.get('flags',[])]
    for ident,part,slug,title,total in VOLUMES:
        if args.volume and ident!=args.volume:continue
        source=next(args.input.glob('*HB'+ident+'*.txt'));raw=source.read_text();lines=raw.splitlines()
        volume_flags=[f for f in FLAGS if f['volume']==ident]
        if ident=='21722':
            uncertain={};current_page=0
            for line_no,line in enumerate(lines,1):
                marker=PAGE.fullmatch(line)
                if marker:current_page=int(marker[2])
                if '[?]' in line:uncertain.setdefault(current_page,[]).append({'line':line_no,'count':line.count('[?]')})
            for number,places in uncertain.items():
                count=sum(p['count'] for p in places)
                volume_flags.append({'volume':ident,'pdfPages':[number],'kind':'source_uncertainty',
                  'sourceLines':[p['line'] for p in places],'occurrences':count,
                  'note':f'Die gelieferte Transkription markiert hier {count} unsichere Lesart(en) mit [?] (Quellzeile(n) '+', '.join(str(p['line']) for p in places)+'). Die Markierungen und die unmittelbar davor stehenden Wörter bleiben erhalten; am Scan prüfen.'})
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
        stats=Counter();newlines=lines.copy();chunks=[];indices=[];size=0;in_table=False;table_lines=set()
        for n in range(first,len(lines)):
            # Names in diagrams are not ordinary words. Keep whole tables, even
            # their labels, exactly as supplied; do not infer missing pointing.
            if lines[n]=='=== טבלה ===': in_table=True;continue
            if lines[n]=='=== סוף טבלה ===': in_table=False;continue
            if in_table:
                stats['table_lines_preserved']+=1;table_lines.add(n)
            # Structural delimiters remain source text; only textual lines sent.
            if PAGE.fullmatch(lines[n]) or lines[n].startswith('===') or not letters(lines[n]):continue
            if size+len(lines[n])>5500 and indices:chunks.append(indices);indices=[];size=0
            indices.append(n);size+=len(lines[n])+1
        if indices:chunks.append(indices)
        for i,indices in enumerate(chunks):
            text='\n'.join(lines[n] for n in indices)
            result=vocalize_chunk(text,args.cache,stats).split('\n')
            assert len(result)==len(indices)
            for n,value in zip(indices,result):
                if n not in table_lines:
                    value=refine_prayer_line(lines[n],value,phrase_index,stats)
                    # Do not settle a word which the transcriber marked uncertain.
                    old_words=list(WORD.finditer(lines[n]));new_words=list(WORD.finditer(value))
                    replacements=[]
                    for a,b in zip(old_words,new_words):
                        if re.match(r'\s*\[\?\]',lines[n][a.end():]):replacements.append((b.start(),b.end(),a.group()))
                    for start,end,original_word in reversed(replacements):value=value[:start]+original_word+value[end:]
                    newlines[n]=value
            print(f'HB{ident}: {i+1}/{len(chunks)} chunks vocalized',flush=True)
        stats['words_with_added_niqqud']=sum(a.group()!=b.group() for old,new in zip(lines,newlines) for a,b in zip(WORD.finditer(old),WORD.finditer(new)))
        pages=[];page=None;table=None;blocks=[]
        xml=['<?xml version="1.0" encoding="UTF-8"?>',f'<siddur id="HB{ident}" part="{part}" xml:lang="he" schema="azara-rashash-1" niqqud-status="machine-assisted-draft">',
             '<metadata>',f'<title>{escape(title)}</title>',f'<source filename="{escape(source.name,quote=True)}" sha256="{sha256(raw.encode()).hexdigest()}" />',
             '<vocalization engine="Dicta Nakdan" genre="rabbinic" status="editorial-review-required" />',
             '<policy>Alle Quellbuchstaben bleiben erhalten. Namen, Abkürzungen, einzelne Buchstaben und vorhandene Punktierung werden nicht automatisch verändert. Ergänztes Niqqud ist kein vollständig am Scan geprüftes Original-Niqqud.</policy>',
             '</metadata>','<transcription_header status="original-before-vocalization">']
        for n,value in enumerate(prefix,1):xml.append(f'<line source-line="{n}">{escape(value)}</line>')
        xml.append('</transcription_header>')
        def close_table():
            nonlocal table
            if table is not None:
                blocks.append(table);table=None;xml.append('</table>')
        def close_page():
            if page is not None:
                close_table();page['blocks']=blocks.copy();pages.append(page.copy());xml.append('</page>')
        for n in range(first,len(lines)):
            orig=lines[n];value=newlines[n];m=PAGE.fullmatch(orig)
            if m:
                close_page();blocks=[];number=int(m[2]);page={'pdfPage':number,'folio':m[1],'flags':[f for f in volume_flags if number in f['pdfPages']]}
                xml.append(f'<page id="HB{ident}-p{number:03}" pdf="{number}" folio="{escape(m[1],quote=True)}" marker="{escape(orig,quote=True)}">')
                for flag in page['flags']:xml.append(f'<review kind="{flag["kind"]}" status="open">{escape(flag["note"])}</review>')
                continue
            identline=f'HB{ident}-L{n+1:04}'
            if orig=='=== טבלה ===':
                assert table is None
                table={'kind':'table','id':identline,'rows':[],'startLine':n+1};xml.append(f'<table id="{identline}" source-line="{n+1}" preserve-layout="true" niqqud="source-only" recite="false">');continue
            if orig=='=== סוף טבלה ===':
                assert table is not None;table['endLine']=n+1;close_table();continue
            tag='row' if table is not None else 'heading' if orig.strip().startswith('■') else 'p'
            if not orig.strip():
                xml.append(f'<lb source-line="{n+1}" />');continue
            content=inline_xml(value,orig)
            status='added-draft' if value!=orig else 'source-preserved'
            xml.append(f'<{tag} id="{identline}" source-line="{n+1}" niqqud="{status}">{content}</{tag}>')
            # Only generated, escaped markup; no source HTML is trusted.
            html=re.sub(r'<(shem|abbr|source_pointing|letter)(?: recite="false")?>',lambda m:f'<span class="rashash-{m[1]}">',content)
            html=re.sub(r'</(?:shem|abbr|source_pointing|letter)>','</span>',html)
            html=html.replace('<unclear reason="source-transcription">','<span class="rashash-unclear" title="Unsichere Lesart der Transkription">').replace('</unclear>','</span>')
            block={'id':identline,'line':n+1,'kind':tag,'text':value,'html':html}
            if table is not None:table['rows'].append(block)
            else:blocks.append(block)
        close_page();xml.append('</siddur>');tagged='\n'.join(xml)+'\n';ET.fromstring(tagged)
        assert [p['pdfPage'] for p in pages]==[1,*range(3,total+1)]
        # Check all original text lines and original protected words byte-for-byte.
        assert all(bare(a)==bare(b) for a,b in zip(lines,newlines))
        name=f'Siddur_HaRashash_Teil_{part}_HB{ident}_{slug}_Niqqud_Tags.txt'
        sourcepath=output/'sources'/f'HB{ident}_Original.txt';sourcepath.write_text(raw)
        (output/name).write_text(tagged)
        entry={'id':ident,'part':part,'title':title,'pages':len(pages),'pdfPages':total,'txtPath':'texts/rashash/'+name,
               'sourcePath':'texts/rashash/sources/'+sourcepath.name,'jsonPath':f'data/rashash-text-{ident}.json',
               'status':'Niqqud-Arbeitsfassung · redaktionell zu prüfen','statistics':dict(stats),'flags':volume_flags}
        (ROOT/entry['jsonPath']).write_text(json.dumps({**entry,'pages':pages},ensure_ascii=False,separators=(',',':'))+'\n')
        summaries[ident]=entry
        doc=next(x for x in docs['documents'] if x['id']==ident);doc['transcription']=entry
        print(json.dumps({'volume':ident,'pages':len(pages),'statistics':dict(stats)},ensure_ascii=False),flush=True)
    ordered=sorted(summaries.values(),key=lambda v:v['part'])
    docs['transcriptions']={'schemaVersion':1,'date':'2026-10-25','volumes':ordered,
      'policy':'Maschinell unterstützte Niqqud-Arbeitsfassungen der hochgeladenen Transkriptionen. Keine vollständige Kollation; Originalscan bleibt maßgebend.'}
    docs['warnings']=[w for w in docs['warnings'] if not w.startswith(('Die gesamte Abfolge','Drei Transkriptionen','4 Transkriptionen'))]
    docs['warnings'].append(f'{len(ordered)} Transkriptionen sind strukturiert und mit zusätzlichem Niqqud erschlossen. Die Gesamtjahresfolge und die ergänzte Punktierung sind nicht vollständig am Scan geprüft; bekannte Lücken tragen Prüfmarkierungen.')
    (ROOT/'data/rashash.json').write_text(json.dumps(docs,ensure_ascii=False,indent=2)+'\n')
    (ROOT/'data/rashash-text-audit.json').write_text(json.dumps({'date':'2026-10-25','flags':all_flags,'volumes':ordered},ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':main()
