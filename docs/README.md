# Azara · Die lebendige Synagoge

Azara verbindet eine perspektivische Synagoge, die 71 vorhandenen Projektfiguren, einen fortlaufenden jüdischen Jahreskalender, Tagesgebete, Tora-Aufrufe, einen Siddur-Leser und Originalaufnahmen.

## Start

1. Die veröffentlichte Seite öffnen.
2. **Schabbat erleben** zeigt den nächsten Schabbat mit sieben Alijot und zusätzlichem Maftir.
3. **Ton einschalten** aktiviert die Originalaufnahmen. Browser erlauben hörbares Autoplay erst nach einer Benutzeraktion.
4. **Tora & Alijot** zeigt jede Bibelstelle, den szenischen Aufgerufenen und den Text-/Audiozugang.
5. **Jahreskalender** wählt jeden Tag und jedes Jahr; **Jahreslauf starten** führt Gebete und Tage automatisch fort.
6. Unter **Quellen & Einstellungen** sind Ort, Israel/Diaspora, Lautstärke, künstliche hebräische Einzelstimmen und abweichende Fasttags-Haftara wählbar.

## Darstellung

Die bevorzugte Darstellung verwendet Three.js, WebGL 2, Schatten, perspektivische Kamera, modellierten Aron HaKodesch, Bima, Tora, Steinboden, Säulen, Leuchter und 71 animierte Figuren mit den vorhandenen Porträts. Ist WebGL nicht verfügbar, übernimmt ein interaktiver Software-Perspektivrenderer denselben Ablauf. Ziehen dreht, das Mausrad zoomt, Kameratasten wählen Ansichten; ein Klick auf einen Beter öffnet sein Porträt.

## Text und Minhag

Die Originaldateien bleiben unverändert. Die neun Rashash-Scans sind mit überprüften Themen und physischen PDF-Seiten erschlossen. Der lesbare ergänzende Siddur enthält 145 Abschnitte der Shaliehsaboo Edition (Edot HaMizrach, Sefaria CC0). Er enthält auch alternative Texte und Anweisungen; diese werden nicht automatisch bereinigt.

Die vollständige Rashash-Kavvanot-Abfolge ist nicht maschinenlesbar transkribiert oder als vollständiger Jahresnusach geprüft. Fehlende Festtexte werden nicht erfunden. Die genaue liturgische Feingliederung, Gemeindeminhag und Kavvanot erfordern fachliche redaktionelle Prüfung. Die dargestellten Gebetszeiten und Dauern sind Modellwerte, keine verbindliche Gottesdienstzeit.

Kohen- und Levi-Status der Projektfiguren ist nicht dokumentiert. Die Anwendung stellt dies ausdrücklich offen dar und leitet keine Abstammung aus Dateinamen ab. Die 71 Figuren sind eine szenische Gemeinde und keine physisch versammelten Personen.

## Audio

- 55 unveränderte MP3-Dateien im Nutzerbestand (einschließlich Namensvarianten/Dubletten).
- 54 vollständige externe Tora-Lesungen.
- 378 einzelne Schabbat-Alijot und 162 Werktags-Alijot.
- 53 Haftara-Einträge und 13 Gebetsaufnahmen.
- Externe Aufnahmen bleiben auf den Servern des Sephardic Pizmonim Project; Quellen und Vortragende erscheinen am Player.
- Automatische Haftara-Zuordnung erfolgt nach der tatsächlichen Bibelstelle, nicht nur dem Paraschenamen. Für einige Sonderfälle und Teruma/Kedoschim fehlen passende Aufnahmen.
- Syrisch-sefardische Alija-Grenzen wurden nicht versgenau gegen Hebcal geprüft. Die Software kennzeichnet dies. Maftir bleibt ein eigenständiger szenischer/Textabschnitt, wenn keine passende Aufnahme vorliegt.
- Künstliche hebräische Lesestimmen sind optional und hängen von installierten hebräischen Browser-/Systemstimmen ab. Sie imitieren keine Stimmen der Porträtfiguren und keine Kantillation.
- Stille Amida bleibt ohne automatische Audio-Wiedergabe.

## Kalender

Lokale Berechnung mit festgeschriebenen Versionen von @hebcal/core und @hebcal/leyning. Israel und Diaspora, Schaltjahre, Sonder-Schabbatot, Feiertagsüberschneidungen, sefardische Haftara, Fasttage, Rosch Chodesch und Omer. Der hebräische Tag wechselt am berechneten Sonnenuntergang des gewählten Ortes. Sonnenzeiten ohne Höhenkorrektur; Sommer-/Winterzeit folgt der IANA-Zeitzone.

## Entwicklung und Veröffentlichung

```sh
npm ci
npm test
npm run build
npm run dev
```

Die GitHub-Actions-Datei `.github/workflows/pages.yml` baut und veröffentlicht `dist/` über GitHub Pages. Alle bereits vorhandenen Quelldateien werden unverändert mitgenommen. Zum Aktivieren der ersten Veröffentlichung muss GitHub Pages gegebenenfalls einmal auf **GitHub Actions** eingestellt werden, falls die Installation die Einrichtung nicht selbst zulässt.

Ein Neubau aktualisiert den Textkatalog aus `Shaliehsaboo Edition.txt`. Neue MP3-/PDF-Dateien brauchen zusätzlich einen Eintrag in `data/repository-assets.json`; neue Aufnahmen und ihre liturgische Zuordnung werden bewusst nicht ungeprüft erraten.

## Prüfung

Automatisierte Prüfungen decken Grundzahlen der Alijot, Maftir, Schabbat-Mincha, Festkollisionen, Fasttagsvarianten, Rosch-Chodesch/Chanukka, Abendwechsel, Sommerzeit und die Jahre 5787–5789 in Israel und Diaspora ab. Browserprüfung prüft Navigation, Darstellung, Kalender, Porträts, Textleser und Player. Die WebGL-Darstellung kann in einer Umgebung mit deaktiviertem Grafiktreiber nicht bildlich geprüft werden; dort wird der Software-Renderer geprüft.
