# Acht Rashash-Textfassungen · Prüfvermerk vom 27. Oktober 2026

Die acht hochgeladenen Transkriptionen sind in Azara unter **Siddur & Kavvanot → HaRashash · Text mit Niqqud** erschlossen. Teil III liegt in zwei getrennten Scanfassungen vor. HB21521 wird als eigene Schabbatmorgen-Ausgabe neben HB21376 geführt. Die TXT-Downloads enthalten XML-Struktur-Tags und sind UTF-8-Dateien. Die hochgeladenen Originaltranskriptionen werden unverändert erhalten. HB21376 wurde bereits mit Tags und Niqqud geliefert; hierfür ist der TXT-Download zugleich die unveränderte Quelldatei.

| Band | Thema | HebrewBooks | Textseiten | Tabellen |
|---|---|---|---:|---:|
| I | Grundlagen, Morgenberachot, Tallit, Tefillin und Ketoret | 21376 | 176 | 308 |
| I laut Dateiname (Teilfassung bis PDF 50) | Schabbatmorgen, Morgenberachot, Korbanot und Beginn Pesukei deZimra | 21521 | 49 | 45 |
| II (bis zum Scanende PDF 323) | Werktagsgebete, Amida, Birkhat Kohanim, Selichot, Mincha und Arvit | 21375 | 322 | 843 |
| III | Erev Schabbat, Kabbalat Schabbat und Arvit | 21519 | 72 | 149 |
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
- Sämtliche 2.035 Tabellen bleiben einschließlich ihrer Punktierung und Abstände unverändert. Es wird kein fehlendes Namen-Niqqud aus einem Sprachmodell ergänzt.
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
| `number recite="false"` | Unveränderte hebräische Nummerierung der dreizehn Middot in HB21521 |
| `review status="open"` | Nicht aufgelöste Prüfstelle mit verständlicher Beschreibung |
| `niqqud="added-draft"` | Zeile mit ergänztem Niqqud als Arbeitsfassung |
| `niqqud="source-preserved"` | Unveränderte Textzeile |
| `lb source-line="…"` | Erhaltene Leerzeile |
| `unclear reason="source-transcription"` | Erhaltene unsichere Lesart `[?]` |

Beispiel einer stabilen ID: `HB21520-L1840`. Sie bezieht sich auf die ursprüngliche Zeilennummer der Nutzerdatei. Diese IDs sind keine Audio-Zeitmarken.

## Einbindung und Audio

Die acht Textfassungen besitzen Seitenwahl, Suche auch ohne Niqqud, Schriftgrößensteuerung, TXT-Download und einen Direktverweis zum Originalscan derselben Seite. Vom Scan lässt sich die entsprechende Textseite öffnen. Im Tagesablauf wird bei einem passenden Band auch dessen Textfassung angeboten.

Die Bände enthalten vielfach einzelne Gebetswörter, Kavvanot und Tabellen statt einer durchgehenden Gebetsrezitation. Sie ersetzen deshalb nicht automatisch den zusammenhängenden Edot-HaMizrach-Mitlesetext einer Aufnahme. Die vorhandene Audio-Mitlesefunktion bleibt erhalten. Kabbalistische Namen und Tabellen werden nicht künstlich vorgelesen.

## Technische Prüfung und Wiederholung

`python3 scripts/validate-rashash.py` prüft offline Seitenfolge, alle Textzeilen, unveränderte Konsonanten und Satzzeichen, ursprüngliche Punktierung, geschützte Wörter, Tabellenidentität, XML und die Übereinstimmung mit den Webdaten. Die Prüfroutine läuft auch in `npm test`.

Eine erneute Niqqud-Vorbereitung erfolgt nur ausdrücklich mit `scripts/prepare-rashash.py`, einem Pfad zu den ursprünglichen Nutzer-TXT-Dateien und einem Cacheverzeichnis. Für einen einzelnen neuen Band dient `--volume 21722`; bereits erschlossene Bände bleiben dabei unverändert. Sie benötigt Python mit `requests` und den externen Nakdan-Dienst. Der normale Seitenaufbau benötigt weder den Dienst noch einen API-Schlüssel.

## Ergänzung: Teil III · Erev Schabbat · HB21519

Die separat gelieferte und zuvor visuell durchgesehene Transkription von HB21519 wird als eigene Fassung eingebunden: 72 Textseiten (PDF 1 und 3–73), 149 Tabellen. Sie ersetzt HB21520 nicht. Beide Fassungsköpfe, Quelltexte und Prüflisten bleiben getrennt. Die neue Fassung ist die anfänglich ausgewählte Textfassung. Der Tagesablauf öffnet bei HB21519 nun dessen eigenen Text und Scan.

Die acht ursprünglichen `[?]`-Markierungen bleiben sichtbar und tragen zusätzlich `<unclear>`-Tags sowie seitenbezogene Prüfvermerke. Sie betreffen die gedruckte Punktierung des verschränkten Namens `אידהנויה` in jeweils drei Amen-Zeilen:

| Folio | PDF-Seite |
|---|---:|
| י ע"ב | 21 |
| יא ע"ב | 23 |
| כד ע"ב | 49 |
| כה ע"ב | 51 |
| לא ע"ב | 63 |
| לב ע"ב | 65 |
| לד ע"ב | 69 |
| לה ע"ב | 71 |

Die ausdrücklich ausgewiesenen Namenslisten über den Schema-Wörtern bleiben ohne neues Niqqud erhalten und werden mit geschützten Namen-Tags erschlossen. Das gilt auch für Buchstabenkombinationen, die wie gewöhnliche Wörter aussehen, etwa `אני` und `כלי`. Die Tabellen bleiben zeichengetreu einschließlich Wiederholungen und vorhandener Punktierung. Die typografische Sicherheit der Transkription und die sprachliche Prüfung des ergänzten Niqqud sind unterschiedliche Prüfungen: das zusätzliche Niqqud bleibt eine redaktionell zu prüfende Arbeitsfassung.

Die letzte Seite enthält zusätzlich `אתה יצרת` für Mussaf an Schabbat Rosch Chodesch. Der erhaltene Kopfblock der Originaltranskription beschreibt deren ursprünglichen unvokalisierten Gebetstext; die Metadaten der neuen Datei kennzeichnen das nachträglich ergänzte Niqqud.

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


## Ergänzung: Teil I · HB21376 · Erstimport am 26. Oktober 2026

Die gelieferte Datei `Siddur_HaRashash_Teil_1_HB21376_Niqqud_Tags_Kontextgeprueft.txt` wurde **bytegenau unverändert** übernommen (SHA-256 `d63dfd961cf1cad86f5f647ef6c8b5a7e5cbd2b779f52517689671f1108a8e29`). Sie enthält bereits wohlgeformtes XML, Niqqud und geschützte Namen-Tags. Für diesen Import wurde kein Niqqud-Dienst aufgerufen. Der Download ist zugleich die gelieferte Quelldatei; eine unvokalisierte Vorgängerfassung lag für diesen Import nicht vor. Die oben beschriebenen Niqqud-Erzeugungsschritte der früheren fünf Textfassungen wurden auf diesen Band nicht erneut angewandt.

Geprüft wurden die lückenlose Folge der 176 Textseiten (PDF 1 und 3–177), alle 6.118 Absatz-/Überschriften-/Zeilen-IDs, 308 Tabellen mit 4.110 Zeilen, sämtliche geschützten Namen sowie die vollständige Textidentität zwischen XML und Webdaten. Alle 143 `[?]`-Markierungen sind hervorgehoben und mit seitenbezogenen Prüfvermerken erschlossen. Die Metadaten der gelieferten Datei beschreiben eine selektive Kontextprüfung und überwiegend ungeprüftes automatisches Niqqud. Dies wird nicht als vollständige philologische oder sprachliche Freigabe ausgewiesen. Der erhaltene Transkriptionskopf beschreibt teilweise noch den früheren unvokalisierten Stand; maßgebend für den aktuellen Bearbeitungsstand sind die mitgelieferten Metadaten.

Visuelle Stichproben am vorhandenen Originalscan betrafen PDF 19 (Beracha/Namenstabellen), PDF 153 (Ketoret und Fußnote) und PDF 177 (gedrucktes Fehlerverzeichnis). Diese Stichprobe ist keine vollständige neue Kollation aller Seiten. Die gedruckte Korrekturtabelle auf PDF 177 bleibt als eigener Quelltext erhalten; ihre Lesarten wurden nicht stillschweigend auf andere Seiten angewandt.

Der neue Band ist in der Textansicht zunächst ausgewählt. An Werktagen verweisen die Morgenberachot auf PDF 19 und die Ketoret-Schritte auf PDF 153 dieses Bandes. Suche ohne Niqqud, Schriftgröße, Seitenwechsel, TXT-Download und Originalscan-Verweise nutzen die bestehende Leseansicht. Die bisherigen fünf TXT- und Webtextdateien bleiben unverändert.

Der Import lässt sich offline wiederholen:

```bash
python3 scripts/import-tagged-rashash.py /pfad/zur/gelieferten/HB21376.txt
npm test
npm run build
```


## Aktualisierung: Teil I · HB21376 · Scanabgleich-Fassung

Die nachgereichte Datei `Siddur_HaRashash_Teil_1_HB21376_Niqqud_Tags_Scanabgleich.txt` ersetzt die oben dokumentierte Kontextprüfungs-Fassung als aktuelle Text- und Downloadfassung. Sie wurde bytegenau übernommen: SHA-256 `994f829fd4ddc93220353ae593475a4b9d41a16ea89dff9b40c1fbc303e5d1a6`. Die bisherige TXT-Datei ist aus dem aktuellen Dateibaum entfernt und bleibt in der Git-Historie nachvollziehbar.

Der Dateivergleich ergibt 43 geänderte Textabsätze auf 22 Seiten (PDF 6, 7, 8, 10, 17, 19, 23, 24, 43, 48, 73, 77, 81, 85, 89, 94, 97, 101, 119, 133, 143 und 145). Seitenfolge, stabile IDs, alle 308 Tabellen und geschützten Namen-Texte sowie ihre Tags bleiben gegenüber der vorherigen Fassung gleich. Die aktualisierten Absätze werden vollständig in die Webdaten übernommen.

Der Umfang bleibt bei 176 Textseiten und 4.110 Tabellenzeilen. Die mitgelieferten Metadaten sind unverändert: Sie nennen weiterhin 143 offene Lesestellen und nur selektiv geprüftes automatisches Niqqud. Der Dateiname Scanabgleich wird deshalb nicht als neue vollständige sprachliche Freigabe interpretiert. Bei dieser Ersetzung wurde kein eigener erneuter Scanabgleich durchgeführt. Alle übrigen Bände bleiben unverändert.


## Ergänzung: Teil II · HB21375 · Teilfassung bis PDF 50

Die hochgeladene Datei `Siddur_HaRashash_Teil_2_HB21375_bis_PDF050.txt` enthält ausschließlich PDF 1 und 3–50, insgesamt 49 Textseiten. Der Originalscan hat 323 Seiten. PDF 2 ist laut Vorlage die ausgelassene Stempelseite. Ab PDF 51 liegt in diesem Import kein Text vor. In der Leseansicht und im TXT-Download wird der Umfang ausdrücklich als Teilfassung ausgewiesen. Verweise auf spätere Seiten bleiben beim Originalscan und öffnen keine unzutreffende Ersatzseite.

Der hebräische Fließtext wurde mit dem öffentlich von Nakdan Pro verwendeten Dicta-Dienst im rabbinischen Modus vokalisiert. Der Endpunkt wurde am 26. Oktober 2026 anhand des aktuellen Anwendungsskripts von `https://nakdanpro.dicta.org.il/` verifiziert. Alle acht Textblöcke wurden erfolgreich verarbeitet. Die vorhandene vokalisierte Shaliehsaboo-Ausgabe dient zusätzlich nur bei exakt gleichlautenden Mehrwortpassagen als Punktierungsreferenz. Bei diesem Band werden daraus ausschließlich Niqqud-Zeichen, keine zusätzlichen Kantillationszeichen übernommen.

Die unveränderte Quelle wird unter `texts/rashash/sources/HB21375_Original.txt` erhalten; die neue UTF-8-TXT mit XML-Tags unter `texts/rashash/Siddur_HaRashash_Teil_2_HB21375_bis_PDF050_Niqqud_Tags.txt`. Namen, Abkürzungen, einzelne Buchstaben und bereits punktierte Wörter bleiben geschützt. Die 102 Tabellen mit 1.346 Textzeilen und einer Leerzeile bleiben zeichengetreu erhalten. Geschützte Tabellen erhalten kein aus dem Sprachmodell ergänztes Namen-Niqqud. Es wird keine künstliche Aussprache erzeugt.

Alle sieben Unsicherheitsmarker auf PDF 9, 38, 39, 40, 43, 44 und 47 bleiben erhalten und tragen zusätzlich `unclear`-Tags und seitenbezogene Prüfvermerke. Die unsicheren Namenpunktierungen und Buchstabenkombinationen werden nicht aus dem Zusammenhang erraten. Der Kopftext beschreibt den ursprünglichen unvokalisierten Stand; die Metadaten kennzeichnen das nachträglich ergänzte Niqqud als fachlich zu prüfende Arbeitsfassung. Diese technische Aufbereitung ist keine neue vollständige Kollation am Originalscan.

Die Offline-Prüfung vergleicht jede Quellzeile, alle Konsonanten und Satzzeichen, vorhandenes Niqqud, geschützte Wörter und Tabellen sowie die Übereinstimmung zwischen XML und Webdaten. Die übrigen sechs Textfassungen bleiben unverändert.

Wiederholung nur für diese Teilfassung:

```bash
python3 scripts/prepare-rashash.py /pfad/zum/upload /pfad/zum/cache --volume 21375 --through-pdf 50
npm test
npm run build
```


## Aktualisierung: Teil II · HB21375 · Erweiterung bis PDF 100

Die neue Vorlage `Siddur_HaRashash_Teil_2_HB21375_bis_PDF100.txt` ersetzt die vorherige Teilfassung bis PDF 50. Sie enthält PDF 1 und 3–100, insgesamt 99 Textseiten. Die neue vokalisierte und getaggte TXT heißt `Siddur_HaRashash_Teil_2_HB21375_bis_PDF100_Niqqud_Tags.txt`. Die aktuelle Ausgangsdatei bleibt unter `texts/rashash/sources/HB21375_Original.txt` erhalten. Die vorherige Downloadfassung wird aus dem aktuellen Dateibaum entfernt und bleibt in der Git-Historie nachvollziehbar.

Die bereits veröffentlichten 49 Textseiten bis PDF 50 sind inhaltlich unverändert. Das vorhandene Niqqud wird aus der bisherigen XML-Datei übernommen, wenn die betreffende Quellseite bis auf abschließende Leerzeilen identisch ist. Text-IDs, Absatz- und Tabelleninhalte bleiben dadurch erhalten. Nur neue bzw. geänderte Quellseiten werden erneut durch Dicta Nakdan im rabbinischen Modus verarbeitet. Ein automatischer Vergleich der bisherigen Webtextseiten ist als Prüfsumme in den Tests hinterlegt.

Der erweiterte Bestand enthält 232 Tabellen. Alle sieben ursprünglichen Unsicherheitsmarker bleiben erhalten; auf den hinzugekommenen Seiten enthält die Vorlage keine neuen `[?]`-Markierungen. Namen, vorhandene Punktierung und alle Tabellen werden unverändert aus der Vorlage übernommen. Ergänztes Niqqud bleibt eine fachlich zu prüfende Arbeitsfassung; bei diesem Update wurde kein neuer vollständiger Scanabgleich durchgeführt.

Seitenwahl, Suche, TXT-Download und Verweise aus dem Tagesablauf nutzen jetzt den Bereich bis PDF 100. Ab PDF 101 ist weiterhin ausschließlich der Originalscan verfügbar. Die anderen sechs Textfassungen bleiben unverändert.

```bash
python3 scripts/prepare-rashash.py /pfad/zum/upload /pfad/zum/cache --volume 21375 --through-pdf 100
npm test
npm run build
```


## Aktualisierung: Teil II · HB21375 · Erweiterung bis PDF 200

Die neue Vorlage `Siddur_HaRashash_Teil_2_HB21375_bis_PDF200.txt` ersetzt die vorherige Teilfassung bis PDF 100. Der aktuelle Textbestand umfasst PDF 1 und 3–200, insgesamt 199 Textseiten und 488 Tabellen. Die neue UTF-8-Datei mit Niqqud und XML-Tags heißt `Siddur_HaRashash_Teil_2_HB21375_bis_PDF200_Niqqud_Tags.txt`. Der Originalscan umfasst weiterhin 323 Seiten; ab PDF 201 liegt in dieser Teilfassung noch kein Text vor.

Die 99 bisherigen Textseiten bis PDF 100 stimmen in der Vorlage unverändert überein. Niqqud, Absatz- und Tabelleninhalte sowie IDs werden aus der bestehenden Fassung übernommen und durch einen separaten Prüfsummenvergleich abgesichert. Nur die neu hinzugekommenen Fließtexte werden mit Dicta Nakdan im rabbinischen Modus vokalisiert. Die neue Ausgangsdatei wird unverändert unter `texts/rashash/sources/HB21375_Original.txt` erhalten. Die bisherige TXT bis PDF 100 wird im aktuellen Dateibaum durch die erweiterte Fassung ersetzt; frühere Fassungen bleiben in der Git-Historie erhalten.

Die Vorlage enthält nun 19 Unsicherheitsmarker auf 17 Seiten: PDF 9, 38, 39, 40, 43, 44, 47, 117, 130, 139, 167, 168, 185, 187, 190, 195 und 198. Alle bleiben erhalten und werden zusätzlich mit `unclear`-Tags und seitenbezogenen Prüfvermerken erschlossen. Originalpunktierung, Namen und Tabellen werden nicht durch automatisch vorgeschlagene Namenpunktierung ersetzt.

In den neuen Abschnitten stehen Namenreihen auch außerhalb expliziter Tabellen. Eindeutige Buchstabenreihen und Fortschreibungen wie `צ צב צבא` sowie ausdrücklich erkannte Namen wie `פאי`, `חתך`, `בם` und die zusammengesetzten Namen aus Ana beKoach werden zusätzlich geschützt. Bei der gemischten Zeile `טובך יד י אן י` wird nur das Gebetswort vokalisiert; die nachfolgende Buchstabenkombination bleibt unverändert. Diese Regel gilt nur für die neu hinzugekommenen Texte; die bisherigen Seiten werden dadurch nicht nachträglich verändert.

Die technische Prüfung vergleicht Konsonanten und Satzzeichen aller Quellzeilen, vorhandenes Niqqud, Tabellen, geschützte Wörter, stabile IDs und XML-/Webtextidentität. Die ergänzte Vokalisierung ist eine fachlich zu prüfende Arbeitsfassung. Dieses Update umfasst keinen neuen vollständigen Scanabgleich. Die übrigen sechs Textfassungen bleiben unverändert.

```bash
python3 scripts/prepare-rashash.py /pfad/zum/upload /pfad/zum/cache --volume 21375 --through-pdf 200
npm test
npm run build
```


## Aktualisierung: Teil II · HB21375 · bis zum Scanende PDF 323

Die neue Vorlage `Siddur_HaRashash_Teil_2_HB21375_bis_PDF323.txt` ersetzt die Teilfassung bis PDF 200. Sie umfasst PDF 1 und 3–323, insgesamt 322 Textseiten. PDF 2 ist laut Vorlage die ausgelassene Stempelseite. Die neue UTF-8-TXT mit Niqqud und XML-Tags heißt `Siddur_HaRashash_Teil_2_HB21375_bis_PDF323_Niqqud_Tags.txt`. Der Katalog kennzeichnet die Abdeckung als bis zum Scanende reichend; der bisherige Hinweis auf fehlende Seiten ab PDF 201 entfällt. Dies beschreibt den Seitenumfang der gelieferten Transkription und ist keine Bestätigung einer vollständigen philologischen Edition.

Alle 199 bisherigen Textseiten bis PDF 200 stimmen in der neuen Quelle unverändert überein. Vokalisierung, Inline-Tags, IDs und gerenderte Inhalte werden exakt übernommen und durch Prüfsummen für die bisherigen Stände bis PDF 50, 100 und 200 abgesichert. Nur die neuen Fließtexte werden mit Dicta Nakdan im rabbinischen Modus bearbeitet. Die neue Quelle bleibt unverändert unter `texts/rashash/sources/HB21375_Original.txt` erhalten. Die vorige TXT wird im aktuellen Dateibaum ersetzt; frühere Stände bleiben in der Git-Historie erhalten.

Die Vorlage enthält 843 Tabellen, darunter 66 innere Tabellen in 777 äußeren Tabellen. Der Import erhält die Verschachtelung in XML. Für die bestehende lineare Leseansicht werden alle 11.631 nichtleeren Tabellenzeilen einmal in ihrer Quellreihenfolge dargestellt; die Grenzen der inneren Tabellen bleiben zusätzlich in den JSON-Metadaten nachvollziehbar. Auch unmittelbar zusammengezogene End-/Anfangsmarker werden als zwei Strukturereignisse derselben Quellzeile verarbeitet. Der unveränderte Quelltext wird dafür nicht umgeschrieben. Alle Tabellen einschließlich der 14 Leerzeilen bleiben von der automatischen Vokalisierung ausgenommen.

86 unsichere Lesestellen auf 44 Textseiten bleiben unverändert erhalten und werden mit `unclear`-Tags sowie seitenbezogenen Prüfvermerken erschlossen. Die zwei zusätzlichen Vorkommen von `[?]` im Vorspann gehören zur Zählangabe und zur Zeichenerklärung, nicht zum Seiteninhalt. Bereits gesetztes Niqqud, Namen, Abkürzungen und Buchstabenreihen bleiben geschützt. Eindeutige neue symbolische Reihen wie `לל שיד הויה` werden ebenfalls nicht automatisch vokalisiert.

Die technischen Prüfungen vergleichen alle Quellzeilen einschließlich Konsonanten, Satzzeichen und bestehender Punktierung, sämtliche Tabellenzeilen, innere Tabellengrenzen, IDs und die XML-/Webtextidentität. Die ergänzte Vokalisierung bleibt eine fachlich zu prüfende Arbeitsfassung. Dieses Update umfasst keinen neuen vollständigen Scanabgleich. Im Ausgangstext vermerkte seitenübergreifende Fortsetzungen bleiben bei den vom Transkribenten zugewiesenen Seiten; es wird keine neue Scanposition behauptet. Die übrigen sechs Textfassungen bleiben unverändert.

```bash
python3 scripts/prepare-rashash.py /pfad/zum/upload /pfad/zum/cache --volume 21375 --through-pdf 323
npm test
npm run build
```

## Ergänzung: HB21521 · Schabbatmorgen · Teilfassung bis PDF 50

Die Datei `Siddur_HaRashash_Teil_1_HB21521_bis_PDF050.txt` wird als eigene Ausgabe neben HB21376 eingebunden. Der Dateiname nennt Teil I; die gedruckte Teilnummer ist im Quellenindex nicht verifiziert. Die inhaltliche Zuordnung bleibt Schabbat-Schacharit, später Musaf und Mincha. Der aktuelle Import enthält ausschließlich PDF 1 und 3–50, also 49 Textseiten von 231 Scan-Seiten. Der Katalog und die Leseansicht kennzeichnen die Ausgabe als Teilfassung; PDF 51–231, insbesondere Musaf PDF 217 und Mincha PDF 221, bleiben ausschließlich über den Originalscan erreichbar.

Der neue UTF-8-Download heißt `Siddur_HaRashash_Teil_1_HB21521_bis_PDF050_Niqqud_Tags.txt`. Die unveränderte Ausgangsdatei liegt unter `texts/rashash/sources/HB21521_Original.txt`. Neue Fließtexte werden mit Dicta Nakdan im rabbinischen Modus vokalisiert; eindeutige Mehrwortpassagen werden zusätzlich mit dem bereits vorhandenen vokalisierten Siddur abgeglichen. Dabei werden nur Vokalzeichen übernommen. Ursprüngliche Konsonanten, Leerzeichen, Satzzeichen und vorhandenes Niqqud bleiben erhalten.

Alle 45 Tabellen mit 546 nichtleeren Zeilen und 16 Leerzeilen bleiben zeichengetreu erhalten und werden nicht automatisch vokalisiert. Namen, Abkürzungen und symbolische Namensfolgen wie `אאלל אידהנויה` bleiben geschützt. Die Nummerierung der dreizehn Middot auf PDF 30–31 (`א` bis `יג`) wird als Nummerierung markiert und erhält keine Wortvokalisierung.

Alle sieben Unsicherheitsmarker auf PDF 6, 26, 34, 36, 37, 39 und 42 bleiben erhalten und werden mit `unclear`-Tags und Prüfvermerken sichtbar gemacht. Zusätzlich sind zwei mögliche Wiederholungen der Vorlage als offene Prüfstellen gekennzeichnet: die Gottesnamenfolge am Übergang PDF 45–46 sowie die unmittelbar wiederholten beiden Sätze aus Psalm 90 auf PDF 47. Die Vorlage wird dafür nicht stillschweigend gekürzt oder korrigiert. Die vom Transkribenten bei ihrem Beginn zusammengeführten seitenübergreifenden Anmerkungen behalten ihre gelieferte Zuordnung.

Die technische Prüfung kontrolliert sämtliche Quellzeilen, vorhandene Vokalzeichen, Tabellen, stabile IDs und die Identität von TXT- und Webtext. Das ergänzte Niqqud bleibt eine fachlich zu prüfende Arbeitsfassung; dieser Import umfasst keinen neuen vollständigen Abgleich mit den Scanseiten. Die sieben bereits eingebundenen Ausgaben bleiben unverändert.

```bash
python3 scripts/prepare-rashash.py /pfad/zum/upload /pfad/zum/cache --volume 21521 --through-pdf 50
npm test
npm run build
```
