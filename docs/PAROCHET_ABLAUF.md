# Parochet und Aron haKodesch

Der Aron erhält einen blickdichten, zweigeteilten Samtvorhang mit Falten, goldener Einfassung und Torakrone. Beide Hälften werden an die äußeren Seiten gerafft. Die Torarollen stehen hinter dem Stoff im Inneren des Schranks. Die vier Glasfenster samt kreuzenden Sprossen und Fensterrahmen wurden vollständig entfernt; dort setzt sich die Steinwand fort. WebGL und die Canvas-Ersatzdarstellung verwenden dieselben Handlungsregeln.

## Ablauf

| Handlung im vorhandenen Gebetsplan | Parochet |
|---|---|
| Gewöhnliche Gebete, Amida, Megilla, Aleinu | geschlossen |
| Öffnung des Hechals | öffnet sich im ersten Drittel des Abschnitts |
| Herausnehmen und Prozession zur Bima | offen |
| Hagbaha, Toralesung, Maftir, Haftara | offen |
| Rückkehr der Tora | zunächst offen; schließt nach Ankunft am Aron im letzten Viertel |
| Kol Nidre | öffnet sich zu Beginn, schließt am Ende |
| Hoschanot mit Umzug und Simchat-Tora-Hakafot | öffnet sich zu Beginn, schließt am Ende |
| Hoschanot am Schabbat ohne Umzug | geschlossen |
| Neïla und abschließendes Schema | offen |
| Abschließender Schofarton nach Neïla | schließt am Ende |

Das Offenhalten des gesamten Toralesungsblocks entspricht der gewünschten szenischen Darstellung. Einzelheiten des Öffnens und Schließens unterscheiden sich nach Gemeindeminhag. Die Tabelle beschreibt das Verhalten dieser Anwendung, keine einheitlich verbindliche Ritualanweisung. Die Festhandlungen werden auf der Granularität der bereits vorhandenen Gebetsabschnitte dargestellt.

Die Tora wird bei der Prozession sichtbar getragen. Der Rückweg verläuft von der Bima zum Aron; erst nach der Ankunft schließt sich der Vorhang. Die offene Schriftrolle auf der Bima erscheint während Toralesung und Maftir; bei der Haftara wird keine offene Tora dargestellt.

## Steuerung und Prüfung

`src/ritual.js` beschreibt die Handlungen unabhängig von der Grafik. Jeder Gebetsabschnitt erhält `arkAction`; zusätzliche Abschnitte können diese Eigenschaft ausdrücklich festlegen. Ein allgemeines `pose: reading` öffnet den Aron nicht. Ein Sprung zu einem anderen Abschnitt setzt dessen eigenen Zustand, ohne einen früheren Öffnungszustand zu übernehmen. Das Raffen wird zeitbasiert weich interpoliert; bei reduzierter Bewegung wird der Zielzustand direkt gesetzt.

`tests/ritual.test.mjs` prüft Werktags- und Schabbatlesungen, Schabbat-Mincha, beide Prozessionsrichtungen, Festhandlungen, den Neïla-Abschluss und die seitliche Stoffraffung. Der Status der Parochet steht zusätzlich neben der Szene.

Primäre Beschreibungen der berücksichtigten Festhandlungen:

- [Kol Nidre: Herausnehmen der Torarollen](https://www.chabad.org/library/article_cdo/aid/995094/jewish/A-Step-by-Step-Yom-Kippur-Guide.htm)
- [Hoschanot: offene Lade beim Umzug](https://www.chabad.org/library/article_cdo/aid/2337565/jewish/All-About-Hoshanot.htm)
- [Neïla: offene Lade](https://www.chabad.org/library/article_cdo/aid/5349/jewish/Neilah-The-Closing-Services.htm)
- [Simchat Tora: Herausnehmen und Zurückbringen der Rollen](https://www.chabad.org/library/article_cdo/aid/1288671/jewish/Simchat-Torah-Hakafot-Procedure.htm)
