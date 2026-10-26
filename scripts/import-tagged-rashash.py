#!/usr/bin/env python3
"""Import the supplied HB21376 tagged edition offline, without changing its TXT."""
import argparse
from collections import Counter
from hashlib import sha256
from html import escape
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
TXT = 'texts/rashash/Siddur_HaRashash_Teil_1_HB21376_Niqqud_Tags_Scanabgleich.txt'


def inline(node):
    def plain(value):
        return escape(value or '').replace('[?]', '<span class="rashash-unclear" title="Ungeklärte Lesart der gelieferten Transkription">[?]</span>')
    html = plain(node.text)
    for child in node:
        assert child.tag == 'shem' and child.attrib == {'recite': 'false'}
        html += '<span class="rashash-shem">' + inline(child) + '</span>' + plain(child.tail)
    return html


def prepare(raw):
    root = ET.fromstring(raw)
    assert root.tag == 'siddur' and root.get('schema') == 'azara-rashash-1'
    allowed = {'siddur', 'metadata', 'title', 'source', 'original-transcription-sha256',
               'revision', 'automatic-niqqud', 'context-review', 'transcription_header',
               'line', 'page', 'heading', 'p', 'table', 'row', 'lb', 'shem'}
    assert all(n.tag in allowed for n in root.iter())
    ids = [n.get('id') for n in root.iter() if n.get('id')]
    assert len(ids) == len(set(ids))
    elements = root.findall('page')
    assert [int(p.get('pdf')) for p in elements] == [1, *range(3, 178)]
    flags, pages = [], []
    for page in elements:
        number = int(page.get('pdf'))
        assert page.get('id') == f'HB21376-p{number:03}'
        uncertain = [n for n in page.iter() if n.tag in {'p', 'heading', 'row'} and '[?]' in ''.join(n.itertext())]
        count = sum(''.join(n.itertext()).count('[?]') for n in uncertain)
        page_flags = []
        if count:
            page_flags.append({'volume': '21376', 'pdfPages': [number], 'kind': 'source_uncertainty',
                'sourceIds': [n.get('id') for n in uncertain], 'occurrences': count,
                'note': f'{count} ungeklärte Lesart(en) mit [?] in der gelieferten, selektiv kontextgeprüften Fassung. Am Originalscan prüfen; automatisches Niqqud ist nicht vollständig fachlich geprüft.'})
        flags.extend(page_flags)

        def item(node):
            ident = node.get('id')
            assert re.fullmatch(fr'HB21376-P{number:03}-T\d{{3}}', ident or '')
            return {'id': ident, 'kind': node.tag, 'text': ''.join(node.itertext()), 'html': inline(node)}

        blocks = []
        for node in page:
            if node.tag == 'lb':
                continue
            if node.tag == 'table':
                assert all(n.tag in {'row', 'lb'} for n in node)
                # Tables lack IDs in the upload. Row and paragraph IDs are preserved.
                blocks.append({'kind': 'table', 'rows': [item(row) for row in node if row.tag=='row']})
            else:
                assert node.tag in {'p', 'heading'}
                blocks.append(item(node))
        pages.append({'pdfPage': number, 'folio': page.get('folio'), 'flags': page_flags, 'blocks': blocks})
    statistics = dict(Counter(n.tag for n in root.iter()))
    statistics['unresolved_markers'] = sum(f['occurrences'] for f in flags)
    assert statistics['unresolved_markers'] == int(root.find('metadata/context-review').get('remaining-markers')) == 143
    entry = {'id': '21376', 'part': 1, 'title': 'Grundlagen und Morgengebet · HB21376',
        'pages': len(pages), 'pdfPages': 177, 'txtPath': TXT, 'sourcePath': TXT,
        'sourceFormat': 'tagged-xml', 'sourceSha256': sha256(raw).hexdigest(),
        'jsonPath': 'data/rashash-text-21376.json',
        'status': 'Automatisches Niqqud · selektiv kontextgeprüft · 143 Lesestellen offen',
        'statistics': statistics, 'flags': flags,
        'editionNote': 'Unverändert übernommene Scanabgleich-Fassung mit Niqqud und Tags. 143 Lesestellen bleiben laut mitgelieferten Metadaten offen. Das automatische Niqqud ist weiterhin nur selektiv kontextgeprüft.',
        'sourceLabel': 'Gelieferte Scanabgleich-TXT mit Niqqud und Tags ↓'}
    volume = {**entry, 'pages': pages, 'provenance': {
        'niqqudStatus': root.get('niqqud-status'),
        'revision': root.findtext('metadata/revision'),
        'automaticNiqqud': dict(root.find('metadata/automatic-niqqud').attrib),
        'contextReview': dict(root.find('metadata/context-review').attrib),
        'originalTranscriptionSha256': root.findtext('metadata/original-transcription-sha256'),
        'header': [n.text for n in root.findall('transcription_header/line')]}}
    return entry, volume


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    args = parser.parse_args()
    raw = args.input.read_bytes()
    entry, volume = prepare(raw)
    (ROOT / TXT).write_bytes(raw)
    (ROOT / entry['jsonPath']).write_text(json.dumps(volume, ensure_ascii=False, separators=(',', ':')) + '\n')
    catalog = json.loads((ROOT / 'data/rashash.json').read_text())
    document = next(d for d in catalog['documents'] if d['id'] == entry['id'])
    previous_txt = document.get('transcription', {}).get('txtPath')
    document['transcription'] = entry
    transcriptions = catalog['transcriptions']
    transcriptions['volumes'] = sorted([v for v in transcriptions['volumes'] if v['id'] != entry['id']] + [entry], key=lambda v: (v['part'], v['id']))
    transcriptions['date'] = '2026-10-26'
    catalog['warnings'] = [re.sub(r'^5 Transkriptionen', '6 Transkriptionen', w) for w in catalog['warnings']]
    (ROOT / 'data/rashash.json').write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + '\n')
    audit = json.loads((ROOT / 'data/rashash-text-audit.json').read_text())
    audit.update(date='2026-10-26', volumes=transcriptions['volumes'],
                 flags=[f for f in audit['flags'] if f['volume'] != entry['id']] + entry['flags'])
    (ROOT / 'data/rashash-text-audit.json').write_text(json.dumps(audit, ensure_ascii=False, indent=2) + '\n')
    # A replacement keeps one current downloadable edition; git retains history.
    if previous_txt and previous_txt != TXT:
        previous = ROOT / previous_txt
        assert previous.parent == ROOT / 'texts/rashash'
        previous.unlink(missing_ok=True)
    print(json.dumps({'id': entry['id'], 'pages': entry['pages'], 'statistics': entry['statistics'], 'sha256': entry['sourceSha256']}))


if __name__ == '__main__':
    main()
