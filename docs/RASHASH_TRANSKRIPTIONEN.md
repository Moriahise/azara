# Vier Rashash-Textbände · Prüfvermerk vom 25. Oktober 2026

Die vier hochgeladenen Transkriptionen sind in Azara unter **Siddur & Kavvanot → HaRashash · Text mit Niqqud** erschlossen. Die TXT-Downloads enthalten XML-Struktur-Tags und sind UTF-8-Dateien. Die hochgeladenen Originaltranskriptionen werden daneben unverändert erhalten.

| Band | Thema | HebrewBooks | Textseiten | Tabellen |
|---|---|---|---:|---:|
| III | Erev Schabbat, Kabbalat Schabbat und Arvit | 21520 | 72 | 149 |
| VI | Schawuot, Lernen in der Nacht, Schacharit und Musaf | 21518 | 24 | 28 |
| VIII | Jom Kippur, Gebete, Kavvanot und Seder haAvoda | 21722 | 138 | 416 |
| IX | Sukkot, Na’anuim, Hallel, Hakafot und Hoschana Rabba | 21723 | 42 | 97 |

Die Textseitenfolge umfasst in jedem Band PDF 1 und PDF 3 bis zur jeweiligen Schlussseite. PDF 2 ist jeweils der Scannerhinweis. **Seitenfolge vollständig verankert** bedeutet nicht, dass jeder Satz des Scans vollständig transkribiert wurde: siehe die unten genannten Lücken.

## Niqqud

Zusätzliches Niqqud wurde mit **Dicta Nakdan im rabbinischen Modus** vorgeschlagen. Verwendeter primärer Nachweis zur Technik: [Nakdan: Professional Hebrew Diacritizer](https://aclanthology.org/2020.acl-demos.23/); aktuelle Anwendung [Nakdan Pro](https://nakdanpro.dicta.org.il/). Eindeutig gleichlautende Mehrwortpassagen wurden zusätzlich mit dem bereits gelieferten vokalisierten Siddur Edot HaMizrach, Shaliehsaboo Edition, abgeglichen. Dabei wird ausschließlich Niqqud übernommen, kein anderer Wortlaut. Die Quelldatei enthält teils volle Schreibweisen; deren Buchstaben bleiben erhalten.

**Dies sind redaktionelle Arbeitsfassungen, keine vollständig am Originalscan kollationierten Niqqud-Ausgaben.** Die visuelle Kontrolle betraf ausgewählte Einleitungs-, Gebets-, Tabellen- und Schlussseiten. Seltene Fachausdrücke und aramäische Passagen erfordern weitere sprachliche Kontrolle.

Schutzregeln:

- Alle ursprünglichen Buchstaben, Leerzeichen und Satzzeichen bleiben im Text erhalten.
- Jedes bereits vokalisierte Quellwort bleibt unverändert.
- Gottesnamen, erkannte Buchstabenkombinationen, Abkürzungen und Einzelbuchstaben erhalten kein automatisch vorgeschlagenes neues Niqqud.
- Sämtliche 690 Tabellen bleiben einschließlich ihrer Punktierung und Abstände unverändert. Es wird kein fehlendes Namen-Niqqud aus einem Sprachmodell ergänzt.
- In den Tabellen enthaltene Gebetswörter bleiben deshalb ebenfalls im ursprünglichen Transkriptionsstand.
- Die lineare Transkription rekonstruiert keine verlorene räumliche Anordnung der handschriftlichen Diagramme. Dafür dient der Originalscan.

## Offene Prüfstellen

1. **III / HB21520, PDF 1:** Die Transkription liest `בשער פקרי הצלם`; im Scan steht `בשער פרקי הצלם`. Zur Korrektur gekennzeichnet, Quellbuchstaben nicht stillschweigend geändert.
2. **III / HB21520, PDF 19:** Zwei Namenzeilen enthalten `[בניקוד הנדפס תחת האותיות]` statt der gedruckten Vokalzeichen. Der Platzhalter bleibt sichtbar und trägt einen Prüfvermerk.
3. **VI / HB21518, PDF 1 und 3:** Die auf PDF 3 fortgesetzte Fußnote wurde in der gelieferten Transkription vollständig unter PDF 1 versammelt. Die Seitenzuordnung ist deshalb dort ungenau.
4. **IX / HB21723, PDF 43:** Die untere Schlussfußnote und die Unterschriften fehlen in der gelieferten Textfassung. Sie wurden nicht ungeprüft ergänzt. Der Scan ist auf dieser Seite direkt erreichbar.

## Tags und stabile Verweise

Die TXT-Dateien sind wohlgeformtes XML mit der Wurzel `<siddur>`. Die Dateiendung bleibt auf Wunsch `.txt`.

| Tag / Attribut | Bedeutung |
|---|---|
| `metadata` | Band, Originaldatei, SHA-256, Verfahren und Bearbeitungsstatus |
| `transcription_header` | Unveränderte Einleitung der ursprünglich unvokalisierten Transkription |
| `page pdf="…" folio="…"` | Physische PDF-Seite und gedruckte Blattbezeichnung |
| `heading`, `p` | Überschrift oder Textabsatz mit stabiler ID und ursprünglicher Zeilennummer |
| `table`, `row` | Tabellenanfang und unveränderte Tabellenzeilen; `niqqud="source-only"` |
| `shem`, `abbr`, `source_pointing`, `letter` | Geschützte Namen, Abkürzungen, Originalpunktierung und Einzelbuchstaben |
| `review status="open"` | Nicht aufgelöste Prüfstelle mit verständlicher Beschreibung |
| `niqqud="added-draft"` | Zeile mit ergänztem Niqqud als Arbeitsfassung |
| `niqqud="source-preserved"` | Unveränderte Textzeile |
| `lb source-line="…"` | Erhaltene Leerzeile |
| `unclear reason="source-transcription"` | Erhaltene unsichere Lesart `[?]` |

Beispiel einer stabilen ID: `HB21520-L1840`. Sie bezieht sich auf die ursprüngliche Zeilennummer der Nutzerdatei. Diese IDs sind keine Audio-Zeitmarken.

## Einbindung und Audio

Die vier Bände besitzen Seitenwahl, Suche auch ohne Niqqud, Schriftgrößensteuerung, TXT-Download und einen Direktverweis zum Originalscan derselben Seite. Vom Scan lässt sich die entsprechende Textseite öffnen. Im Tagesablauf wird bei einem passenden Band auch dessen Textfassung angeboten.

Die Bände enthalten vielfach einzelne Gebetswörter, Kavvanot und Tabellen statt einer durchgehenden Gebetsrezitation. Sie ersetzen deshalb nicht automatisch den zusammenhängenden Edot-HaMizrach-Mitlesetext einer Aufnahme. Die vorhandene Audio-Mitlesefunktion bleibt erhalten. Kabbalistische Namen und Tabellen werden nicht künstlich vorgelesen.

## Technische Prüfung und Wiederholung

`python3 scripts/validate-rashash.py` prüft offline Seitenfolge, alle Textzeilen, unveränderte Konsonanten und Satzzeichen, ursprüngliche Punktierung, geschützte Wörter, Tabellenidentität, XML und die Übereinstimmung mit den Webdaten. Die Prüfroutine läuft auch in `npm test`.

Eine erneute Niqqud-Vorbereitung erfolgt nur ausdrücklich mit `scripts/prepare-rashash.py`, einem Pfad zu den ursprünglichen Nutzer-TXT-Dateien und einem Cacheverzeichnis. Für einen einzelnen neuen Band dient `--volume 21722`; bereits erschlossene Bände bleiben dabei unverändert. Sie benötigt Python mit `requests` und den externen Nakdan-Dienst. Der normale Seitenaufbau benötigt weder den Dienst noch einen API-Schlüssel.

## Ergänzung: Teil VIII · Jom Kippur · HB21722

Die neue Transkription umfasst 138 Textseiten (PDF 1 und 3–139) mit 416 ausgeglichenen Tabellenpaaren. Alle 27 ursprünglichen `[?]`-Marker auf 19 Seiten bleiben erhalten und sind zusätzlich mit `<unclear reason="source-transcription">` markiert. Auch das unmittelbar vor einem Marker stehende Wort wird nicht automatisch neu vokalisiert. Seitenbezogene Prüfvermerke führen Quellzeilen und Anzahl der Unsicherheiten auf.

Gezielt visuell verglichen wurden PDF 1, 3, 4, 98, 99, 126, 128, 130, 132, 138 und 139. Dies ist eine Stichprobe, keine vollständige philologische Kollation.

- **PDF 3–4:** Die Fußnote läuft im Scan über beide Seiten, wurde in der gelieferten Textfassung jedoch einschließlich Unterschriften unter PDF 3 zusammengefasst.
- **PDF 128–130:** Die Vorlage markiert teils unsichere Punktierungen von Gottesnamen. Sie bleiben unverändert, statt aus gewöhnlicher Aussprache rekonstruiert zu werden.
- **PDF 132:** Die unsichere Buchstabenkombination `אאללההייםם [?]` bleibt erhalten. Die dortigen Mincha-/Neila-Anweisungen sind Querverweise auf die Arvit-Kavvanot, kein eigenständiger vollständiger Neila-Text.
- **PDF 126:** Übergang zu Schacharit mit Verweisen auf gemeinsame Kriat-Schema-, Amida- und Musaf-Kavvanot.
- Die ungewöhnliche Überschrift `קדיש דקודם דיוצר` auf PDF 3 steht tatsächlich im Scan und bleibt erhalten.

Die zuvor veröffentlichten Textfassungen der Teile III, VI und IX werden durch diese Ergänzung nicht neu erzeugt oder verändert.

Auf PDF 99 wurden außerdem die Wörter `מְחוֹל`, der Imperativ `מְחֵה` und `פְשָׁעֵנוּ` sowie die Passage `מִנֶּגֶד עֵינֶיךָ` direkt am Scan geprüft. Das spätere `מֹחֶה` in der Schriftstelle bleibt als Partizip unterschieden. Die ergänzte Punktierung voller Schreibweisen mit Waw wird entsprechend lesbar gesetzt.
