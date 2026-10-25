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
    raw=(ROOT/meta['sourcePath']).read_text();lines=raw.splitlines()
    root=ET.parse(ROOT/meta['txtPath']).getroot()
    assert root.find('metadata/source').attrib['sha256']==sha256(raw.encode()).hexdigest()
    pages=root.findall('page');expected=[1,*range(3,meta['pdfPages']+1)]
    assert [int(p.attrib['pdf']) for p in pages]==expected
    assert len(pages)==meta['pages']
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
        if '━━━━━━━━' in line or line in ['=== טבלה ===','=== סוף טבלה ===']:continue
        assert n in seen,f'Missing line HB{meta["id"]} {n}'
    assert added>1000
    volume=json.loads((ROOT/meta['jsonPath']).read_text())
    assert len(volume['pages'])==len(pages)
    for page in volume['pages']:
        for block in page['blocks']:
            for item in block['rows'] if block['kind']=='table' else [block]:
                assert item['text']==seen[item['line']]
                assert '<script' not in item['html'] and 'onclick=' not in item['html']
    report.append({'id':meta['id'],'pages':len(pages),'tables':len(root.findall('.//table')),'addedMarks':added,'protectedTokens':protected,'sourceLines':len(lines)})
print(json.dumps(report))
