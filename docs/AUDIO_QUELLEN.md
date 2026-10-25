# Synagogue audio sources — 25 October 2026

The source is the **Sephardic Pizmonim Project** at https://www.pizmonim.org/. These recordings document Syrian Sephardic / Aleppo traditions; they must not be presented as recordings of the Siddur HaRashash or as the voices of the app's fictional rabbi figures.

## Deliverables

- `audio-research.json`: 54 full Torah recordings by Abe Zami; 52 Haftarah player recordings, plus an explicitly documented reuse for Pekudei (the same passage as second Shabbat Chanukah); 13 prayer recordings/samples; and the `torahAliyot` property.
- `audio-torah-aliyot.json`: all 54 Torah portions, each with a verified-directory full-portion MP3 URL, seven Shabbat aliyah files, and three weekday files. Total: 54 full, 378 Shabbat, 162 weekday URLs.

Every full Torah and Haftarah/prayer URL was extracted from its source player HTML. Every named aliyah filename is explicitly listed in the primary host's public MP3 directory. Audio files were not copied into the repository. Three selected URLs received HTTP HEAD spot checks; see JSON `spotChecks` (not a full playback audit).

## Exact source pages

- Torah: https://www.pizmonim.org/section.php?maqam=Pentateuch
- Haftarot: https://www.pizmonim.org/section.php?maqam=Haftarot
- Shaharit samples: https://www.pizmonim.org/festivals.php?holiday=pieces
- Weekday Mincha / Arvit: https://www.pizmonim.org/section.php?maqam=Minha-Arbit
- Directory confirming exact names: https://www.pizmonim.org/MP3/
- Syrian aliyah stops, if alignment needs review: https://www.pizmonim.org/aliyot.php

## Playback and attribution

Stream from the original HTTPS host and keep the source-page link and named performer visible. Public availability is not a blanket re-publication license; no rehosting permission was inferred. The source attributes Abe Zami's recording, mixing and editing to Daniel Shatzkes at Harmony Studios. Haftarah performers are chiefly Meyer “Mickey” Kairey, with explicit exceptions in each JSON `label`. Prayer entries retain the actual performer names.

The seven Shabbat files use source names Rishon, Sheni, Shelishi, Rebii, Hamishi, Shishi and Shebii. Weekday files use Kohen, Levi, Yisrael. **Syrian aliyah stops may differ from generic metadata**; this research did not audit verse boundaries against Hebcal. Only use them as exact verse-synchronized audio after matching the stops. Do not replay an entire parasha once per aliyah. For a weekly full reading, queue one full recording per portion (two for a double parasha).

## Coverage limits

- Direct weekly Haftarah recordings are missing for **Terumah** and **Kedoshim** in this source index. Pekudei is available through the explicitly identical passage for second Shabbat Chanukah.
- The usual weekly Haftarah is often replaced by a special calendar reading. Choose audio by the **actual passage reference**, not just by the parasha name. No special-festival or fast-day audio should be silently substituted by a usual weekly file.
- The Torah portion recordings cover all 54 portions. Festival-specific Torah readings are not separately assembled by this manifest.
- Several prayer entries are clearly samples, some maqam demonstrations or a large collection (notably the Kedusha collection). The full weekday Amidah is explicitly labelled full; other entries must not be described as complete services.
- A browser may require a user click before audio and some networks may block the original host. Provide a source-page link and honest error state.
