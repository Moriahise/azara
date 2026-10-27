#!/usr/bin/env python3
"""Offline integrity checks for the distributed Rashash TXT working editions."""
from pathlib import Path
from hashlib import sha256
import json
import re
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parent.parent
marks=re.compile('[\u0591-\u05af\u05b0-\u05bd\u05bf\u05c1\u05c2\u05c4\u05c5\u05c7]')
word=re.compile('[\u05d0-\u05ea][\u05d0-\u05ea\u0591-\u05c7]*(?:["\'״׳][\u05d0-\u05ea\u0591-\u05c7]*)*')
bare=lambda s:marks.sub('',s)
data=json.loads((ROOT/'data/rashash.json').read_text())
report=[]
for meta in data['transcriptions']['volumes']:
    if meta.get('sourceFormat')=='tagged-xml':
        raw=(ROOT/meta['txtPath']).read_bytes()
        assert sha256(raw).hexdigest()==meta['sourceSha256']
        root=ET.fromstring(raw);pages=root.findall('page')
        assert [int(p.attrib['pdf']) for p in pages]==[1,*range(3,meta['pdfPages']+1)]
        assert len(pages)==meta['pages']
        ids=[n.get('id') for n in root.iter() if n.get('id')]
        assert len(ids)==len(set(ids))
        volume=json.loads((ROOT/meta['jsonPath']).read_text())
        assert volume['sourceSha256']==meta['sourceSha256'] and volume['id']==meta['id']
        assert len(volume['pages'])==len(pages)
        for source,page in zip(pages,volume['pages']):
            assert page['pdfPage']==int(source.get('pdf')) and page['folio']==source.get('folio')
            expected=[n for n in source if n.tag!='lb']
            assert len(expected)==len(page['blocks'])
            for node,block in zip(expected,page['blocks']):
                assert block['kind']==node.tag
                nodes=[n for n in node if n.tag=='row'] if node.tag=='table' else [node]
                items=block['rows'] if node.tag=='table' else [block]
                assert len(nodes)==len(items)
                for n,item in zip(nodes,items):
                    assert item['id']==n.get('id') and item['text']==''.join(n.itertext())
                    assert '<script' not in item['html'] and 'onclick=' not in item['html']
            count=''.join(source.itertext()).count('[?]')
            assert sum(f.get('occurrences',0) for f in page['flags'])==count
        assert sum(''.join(p.itertext()).count('[?]') for p in pages)==meta['statistics']['unresolved_markers']
        report.append({'id':meta['id'],'pages':len(pages),'tables':len(root.findall('.//table')),
                       'protectedTokens':len(root.findall('.//shem')),'importedUnchanged':True})
        continue
    raw=(ROOT/meta['sourcePath']).read_text();lines=raw.splitlines()
    root=ET.parse(ROOT/meta['txtPath']).getroot()
    assert root.find('metadata/source').attrib['sha256']==sha256(raw.encode()).hexdigest()
    pages=root.findall('page');expected=[1,*range(3,meta['pdfPages']+1)]
    assert [int(p.attrib['pdf']) for p in pages]==expected
    assert len(pages)==meta['pages']
    ids=[node.get('id') for node in root.iter() if node.get('id')]
    assert len(ids)==len(set(ids)),f'Duplicate ID HB{meta["id"]}'
    first=next(i for i,line in enumerate(lines) if '━━━━━━━━' in line)
    table_markers=re.compile(r'(?:=== (?:סוף )?טבלה ===)+')
    assert len(root.findall('.//table'))==sum(line.count('=== טבלה ===') for line in lines[first:] if table_markers.fullmatch(line))
    seen={};added=0;protected=0
    for node in root.iter():
        if node.tag not in ['line','p','heading','row','lb']:continue
        n=int(node.attrib['source-line']);assert n not in seen
        value=''.join(node.itertext());seen[n]=value
        assert bare(value)==bare(lines[n-1]),f'Changed consonants/punctuation HB{meta["id"]} line {n}'
        old=list(word.finditer(lines[n-1]));new=list(word.finditer(value));assert len(old)==len(new)
        for a,b in zip(old,new):
            if marks.search(a.group()):assert a.group()==b.group(),f'Changed source pointing HB{meta["id"]} line {n}'
        for part in node:
            if part.tag in ['shem','abbr','source_pointing','letter']:
                assert part.text in lines[n-1];protected+=1
        if node.tag=='row':assert value==lines[n-1],f'Changed table HB{meta["id"]} line {n}'
        added+=len(marks.findall(value))-len(marks.findall(lines[n-1]))
    for n,line in enumerate(lines,1):
        if '━━━━━━━━' in line or (n>first and table_markers.fullmatch(line)):continue
        assert n in seen,f'Missing line HB{meta["id"]} {n}'
    assert added>1000
    volume=json.loads((ROOT/meta['jsonPath']).read_text())
    assert len(volume['pages'])==len(pages)
    for source,page in zip(pages,volume['pages']):
        source_tables=source.findall('table');web_tables=[b for b in page['blocks'] if b['kind']=='table']
        assert len(source_tables)==len(web_tables)
        for node,block in zip(source_tables,web_tables):
            assert [r.get('id') for r in node.findall('.//row')]==[r['id'] for r in block['rows']]
            assert {t.get('id') for t in node.findall('.//table')}=={t['id'] for t in block.get('nestedTables',[])}
        for block in page['blocks']:
            for item in block['rows'] if block['kind']=='table' else [block]:
                assert item['text']==seen[item['line']]
                assert '<script' not in item['html'] and 'onclick=' not in item['html']
    report.append({'id':meta['id'],'pages':len(pages),'tables':len(root.findall('.//table')),'addedMarks':added,'protectedTokens':protected,'sourceLines':len(lines)})
print(json.dumps(report))
