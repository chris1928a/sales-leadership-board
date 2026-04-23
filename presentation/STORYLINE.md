# Transcripts as a Goldmine
## Chris Erler · Bottleneck 03 · 10 Minuten · B2B Sales Exchange 24.04.2026

---

## Event-Kontext (Luma)

- **130 Angemeldete**
- **Format:** 3 × 10 Min + 20 Min Live Slido Q&A
- **Umbrella:** "Your sales calls contain a goldmine of market intelligence — most founders never extract it."
- **Chris' offizieller Slot (Luma-Wortlaut):** "Extracting value from call recordings for **lead management, SDR training, and performance analytics**"
- **Deliverable für alle:** Claude Skill auf GitHub (fork-ready) + Tutorial PDF + B2B Sales Folder

## Mein Platz in der Story

Phil baut die Foundation (ICP, Voice-of-Customer aus Calls). Manu baut die Assets (ROI Calculator, Closing-Tools). Ich zeige, **was operativ kippt, wenn deine SDRs wirklich auf AI laufen** — weil Training, Routing und Analytics dann alle anders aussehen müssen.

Das ist nicht "ein weiteres AI-Tool". Das ist die Antwort auf die Frage, die Phil und Manu offen lassen: *"Okay cool, aber was ändert sich an meinem Alltag, wenn ich das ernst nehme?"*

---

## Die Hauptthese (ein Satz)

> **"Dein CRM weiß längst, was schiefläuft. Du hast nur nie zugehört. Ich zeige dir, wie Claude jede Nacht zuhört — und was das mit Training, Routing und Analytics macht."**

---

## Pacing für 10 Minuten

| # | Slide | Dauer | Funktion |
|---|-------|-------|----------|
| 1 | Title / Hook | 0:45 | Tension aufbauen, Umbrella aufgreifen |
| 2 | The 8-Hour Problem | 1:00 | Schmerz etablieren |
| 3 | Why Your Dashboard Lies | 1:00 | Konkretes Versagen zeigen |
| 4 | The Shift (Architektur) | 1:00 | Aha-Moment, wie einfach es ist |
| 5 | The 6-Dimension Scoring Stack | 1:30 | Kern-System |
| 6 | Gap Matrix · Label → Diagnose | 1:30 | Abgrenzung zu Gong |
| 7 | Closed Loop Coaching (Training) | 1:00 | SDR Training delivered |
| 8 | What Shifts in Lead Mgmt | 1:30 | Lead Management delivered (Kern für Phil) |
| 9 | Performance Analytics | 0:45 | Analytics delivered |
| 10 | Takeaway + Fork it | 0:30 | CTA, Mic drop |

**Puffer: 30 Sekunden.** Das ist knapp, aber machbar wenn ich nicht improvisiere.

---

# Slide 1 — Title / Hook

**BOTTLENECK 03 · CHRIS · 10 MIN**

## Transcripts as a **Goldmine**

*What changes once your SDRs actually run on AI — in training, routing, and analytics.*

### WHY diese Slide
Phils Umbrella-Wort ist "Goldmine". Ich übernehme es wörtlich — signalisiert: wir spielen im gleichen Stück, ich bin nicht der Abweichler. Der Untertitel macht meinen einzigartigen Winkel klar: während Phil und Manu zeigen *wie man das Gold schürft*, zeige ich *wie die Mine danach läuft*.

### Was ich sage (45 Sekunden)
> "Phil hat euch gezeigt, wie ihr Calls zu Foundations macht. Manu hat die Closing-Tools live gebaut. Meine 10 Minuten sind die Brücke dazwischen: Was ändert sich im Sales-Alltag, wenn das alles wirklich läuft? Spoiler: Training, Lead Routing und euer Performance Dashboard sehen in drei Wochen anders aus. Sonst lasst ihr das Gold in der Mine liegen."

---

# Slide 2 — The 8-Hour Problem

## **8 hours per rep per week.**

*That's what it takes to coach a rep by listening to their calls. 3 reps = 24 hours. 5 reps = 40.*

→ **No founder has that time. So nobody does it.**

### WHY diese Slide
Ich muss Schmerz etablieren, der konkret genug ist, dass 130 Leute nicken. "8 Stunden pro Rep pro Woche" ist ein Zahlen-Anker, den jeder sofort versteht. Der Follow-up macht klar: das ist nicht ein "nice to have" Problem, das ist die Realität jeder Sales-Org.

### Was ich sage (60 Sekunden)
> "Echtes Coaching heißt Calls hören. Nicht Dashboards lesen. Acht Stunden pro Rep pro Woche — das ist der ehrliche Preis. Bei drei Reps ist euer Montag weg. Bei fünf Reps die halbe Woche. Also was tun wir? Wir öffnen Close.com, sehen 'Rep B hat 40 Calls gemacht, 2 Meetings gebucht' und schreiben in Slack: *Du musst besser pitchen*. Das ist kein Coaching. Das ist ein Horoskop."

---

# Slide 3 — Why Your Dashboard Lies

### Your dashboard says:
> *"Low close rate — fix the pitch."*

### The reality, rep by rep:

| Rep A | opens weak — loses them in the first 30 seconds |
| Rep B | never asks discovery — jumps straight to features |
| Rep C | ends without a concrete next step |

**Same symptom. Three different diseases. One generic coaching sentence.**

### WHY diese Slide
Jeder in der audience hat dieses exakte Gespräch letzte Woche mit seinem Sales Lead gehabt. Ich gebe ihnen die Sprache dafür. Und der Dreisprung (A/B/C) zeigt: das Problem ist nicht *zu wenig Daten*, sondern *zu aggregierte Daten*. Das macht den Weg frei für die Scoring-Lösung.

### Was ich sage (60 Sekunden)
> "Euer Dashboard diagnostiziert jeden Rep gleich. Rep A verliert die Leute in den ersten 30 Sekunden, weil der Opener tot ist. Rep B springt direkt zu Features, weil er nie Discovery macht. Rep C redet super, bucht aber nie einen nächsten Schritt. Drei komplett verschiedene Krankheiten. Ein Satz Coaching: 'pitch besser'. Das bewegt keinen der drei."

---

# Slide 4 — The Shift

## Stop listening. Start scoring.

### Nightly pipeline (runs unattended):

**Close.com / HubSpot API** → every call pulled
**Deepgram** → transcribed in seconds
**Claude** → scored across 6 dimensions
**Google Sheets + Telegram** → one message per rep per morning

**Setup:** one evening. **Cost:** <$50 / month for 10 reps.

### WHY diese Slide
Das ist der architektonische Aha-Moment. Ich will, dass die Leute denken: *"Wait, das sind vier APIs, die ich schon habe oder die 50 Bucks kosten?"* Die Einfachheit ist die Message. Keine Enterprise-Plattform, kein Rollout, kein Consulting Fee. Vier Pipes, ein Cron Job.

### Was ich sage (60 Sekunden)
> "Die Lösung ist lächerlich simpel. Close oder HubSpot API zieht die Calls. Deepgram transkribiert. Claude scored. Google Sheet speichert, Telegram schickt dem Manager morgens eine Nachricht. Ein Abend Setup. Unter 50 Dollar im Monat für zehn Reps. Das Ding läuft seit März bei einer Recruiting Agency. Jeden Morgen liegt die Coaching-Empfehlung im Postfach, bevor der Manager Kaffee trinkt."

---

# Slide 5 — The 6-Dimension Scoring Stack

*(Diese Slide existiert bereits in Phils Brand-Deck — ich referenziere sie nur hier)*

## The 6-Dimension **Scoring Stack**

*CRM data + transcripts → nightly scoring → coaching focus of the week.*

| # | Dimension | Framework (the WHY) |
|---|-----------|---------------------|
| 01 | **Opener** | Pattern Interrupt — first 30s decide everything (Chris Voss) |
| 02 | **Pitch** | SPIN — problem framing, not feature dumping (Rackham) |
| 03 | **Objection Handling** | LARC — Listen · Acknowledge · Reframe · Confirm |
| 04 | **Closing** | Concrete next step with a date in the calendar (Oren Klaff) |
| 05 | **Conversation Depth** | 3-layer Why before pitching (Toyota 5-Whys) |
| 06 | **Rapport** | Mirror, pace, 3-second pause discipline |

### WHY diese Slide
Die Dimensionen sind nicht aus der Luft gegriffen. Hinter jeder steht ein Buch, ein Framework, eine testbare Methode. Das ist der Unterschied zu "AI bewertet Calls mit Vibes". Ich kann jedem CEO im Raum sagen: *"Eure Reps scheitern an Dimension 5? Schickt sie ins SPIN Selling Buch, Kapitel 4."*

### Was ich sage (90 Sekunden)
> "Sechs Dimensionen. Jede hat ein Framework dahinter, mit einem Buch. Opener: Chris Voss, die ersten 30 Sekunden entscheiden alles. Pitch: SPIN Selling, also Probleme framen statt Features abfeuern. Einwandbehandlung: LARC. Closing: konkreter nächster Schritt mit Datum im Kalender. Conversation Depth: drei Ebenen 'warum' bevor du pitchst. Rapport: spiegeln, Tempo anpassen, drei Sekunden Pause aushalten. Claude scored jeden Call auf diesen sechs Achsen, eins bis fünf. Rolling 14-Tage-Schnitt pro Rep pro Dimension. Das ist kein Vibe. Das ist messbar."

---

# Slide 6 — From Label to Diagnosis: The Gap Matrix

## One label. **Nine diagnoses.**

### 2-axis matrix: Activity × Outcomes

|  | **Low Activity** | **Mid Activity** | **High Activity** |
|---|---|---|---|
| **High Outcomes** | Throughput problem → prospecting, speed-to-lead | On track | Elite — replicate |
| **Mid Outcomes** | Engagement dip → ramping, motivation | Average — pick one dimension | Quality gap → script, framework |
| **Low Outcomes** | Check-in required | Volume without conversion → pitch/discovery | Burning the funnel — stop and retrain |

→ **9 cells. 9 distinct coaching paths.**

### WHY diese Slide
Das ist meine Differenzierung gegenüber Gong/Chorus. Die sagen: *"wir nehmen Calls auf."* Ich sage: *"wir diagnostizieren."* Ein Rep mit hoher Activity und niedrigen Outcomes braucht was anderes als einer mit niedriger Activity und hohen Outcomes. Matrix macht das sichtbar und nicht diskutierbar.

### Was ich sage (90 Sekunden)
> "Hier kommt der Unterschied zu Gong oder Chorus. Die nehmen Calls auf — das ist das Gold in der Mine, ungeschürft. Ich drehe das Ding eine Ebene weiter: zwei Achsen, Activity gegen Outcomes, neun Felder. Rep mit viel Activity und miesem Outcome? Qualitäts-Gap, Skript-Problem. Rep mit wenig Activity und gutem Outcome? Throughput-Problem, gib ihm mehr Leads. Rep mit wenig Activity und schwachem Outcome? Engagement, schau ob er ramping oder motivation braucht. Neun Felder, neun verschiedene Coaching-Pfade. Nicht ein generisches 'pitch besser'."

---

# Slide 7 — Closed Loop Coaching (SDR Training)

## Coaching that closes its own loop.

1. **Monday 08:00** — weakest dimension (last 14 days) lands in Telegram
2. **Manager** gets a 90-second script + the matching framework chapter
3. **Rep** practices in next 5 calls — system records
4. **Next Monday** — same system measures: did it move?

→ **Coaching becomes a KPI, not a calendar slot.**

### WHY diese Slide
Das ist die direkte Antwort auf Phils "SDR training" Promise im Luma. Der Punkt ist: Coaching war immer ein Kalender-Event, 1:1 am Freitag. Jetzt ist es ein Messwert mit Feedback-Loop. Das ist für jeden operativen Founder im Raum ein sofort einleuchtender Shift.

### Was ich sage (60 Sekunden)
> "Coaching war immer ein Kalendertermin. Freitag Vierzehn Uhr, Rep und Manager, Kaffee, Bauchgefühl. Mein System macht Coaching zu einem Messwert mit Loop. Montag acht Uhr liegt die schwächste Dimension der letzten vierzehn Tage in Telegram. Manager kriegt ein 90-Sekunden-Skript und das passende Framework-Kapitel dazu. Rep übt fünf Calls. Nächsten Montag misst das System ob es sich bewegt hat. Coaching ist jetzt ein KPI, kein Kalender."

---

# Slide 8 — What Shifts in Lead Management

*(Das ist die Slide, die Phil am meisten will. Hier liefere ich seinen Luma-Pitch.)*

## Once your SDRs run on AI, **three things shift** in lead mgmt.

### 1. Routing
Low-intent transcripts → **nurture track**, not SDR time.
*We save 4 hrs per SDR per week.*

### 2. Qualification
High-intent language in transcript → **auto-escalates to AE** same day.
*Speed-to-quote dropped from 3.2 days to 11 hours.*

### 3. Handoff to Marketing
Lost-reason patterns feed **ICP + ad copy** weekly — Phil's foundation stays fresh.
*Example: 256 calls analyzed. 52% die at gatekeeper, only 7% real engagement → ICP re-cut, outbound rewritten.*

### WHY diese Slide
Das ist *der* Moment des Decks. Phils Event verspricht "extracting value from call recordings for lead management" — wenn ich das hier nicht konkret liefere, ist der ganze Slot schwach. Drei harte Shifts, jeder mit einer Zahl oder einem Beispiel. Der dritte Punkt baut explizit die Brücke zurück zu Phils Segment ("Phil's foundation stays fresh") — das macht das Deck als Ganzes zu einem Kreislauf, nicht zu drei isolierten Pitches.

### Was ich sage (90 Sekunden)
> "Drei harte Shifts im Lead Management, wenn das System läuft. Erstens Routing: Low-Intent Transcripts gehen direkt in den Nurture-Track, nicht auf den SDR-Kalender. Wir haben damit vier Stunden pro SDR pro Woche gespart. Zweitens Qualification: wenn im Transcript klare Buying-Signale auftauchen — Budget, Timeline, Pain — eskaliert der Deal automatisch am selben Tag an den AE. Speed-to-Quote ist von 3,2 Tagen auf 11 Stunden gefallen. Drittens Handoff zu Marketing: die Lost-Reason-Patterns fließen wöchentlich zurück in ICP und Ad Copy. Das ist genau das, was Phil vorhin gezeigt hat — nur dass seine Foundation nicht einmalig gebaut wird, sondern jede Woche neu gefüttert. Beispiel aus März: 256 Calls. 52 Prozent sterben am Gatekeeper, nur 7 Prozent echtes Engagement. ICP wurde neu geschnitten, Outbound komplett umgeschrieben."

---

# Slide 9 — Performance Analytics

## The founder's dashboard: **one screen, three signals.**

### 1. Dimension trend per rep
Are my reps actually improving on their weakest area?

### 2. Framework adoption rate
Is coaching sticking — or are reps falling back into habits?

### 3. ICP drift indicator
Is the market shifting underneath me?

### The founder's single metric:
> **% of reps improving on their weakest dimension this month.**

### WHY diese Slide
Schließt die Luma-Trias "training, performance, analytics" ab. Der Kniff ist die "eine Metrik für den Founder" am Ende — weil jeder Gründer im Raum genau diese Frage hat: *"Welche eine Zahl soll ich mir jede Woche anschauen?"* Ich gebe sie ihnen auf dem Silbertablett.

### Was ich sage (45 Sekunden)
> "Performance Analytics auf einem Screen. Drei Signale: Dimension-Trend pro Rep — verbessern sie sich überhaupt auf ihrer schwächsten Achse? Framework-Adoption — bleibt das Coaching kleben oder fallen sie zurück? ICP-Drift — verschiebt sich der Markt unter meinen Füßen? Und eine einzige Zahl für euch als Founder: Prozent der Reps, die sich diesen Monat auf ihrer schwächsten Dimension verbessert haben. Das ist euer North Star."

---

# Slide 10 — Takeaway + Fork It

## Three sentences. Then Q&A.

> **1.** Reporting tells you what *happened.*
> This system tells each rep what to *practice this week.*

> **2.** Your CRM already knows what's broken.
> You just never listened.

> **3.** **Fork the blueprint.** Plug in your Close or HubSpot key. It runs tonight.

### github.com/chris1928a/sales-leadership-board
### Questions → live on Slido

### WHY diese Slide
Drei Sätze, die jeder nachhause trägt. Satz 1 ist der System-Punkt. Satz 2 ist der emotionale Gut-Punch. Satz 3 ist der CTA, der zu Phils Event-Promise passt (GitHub, fork-ready). Das Luma-Deliverable wird explizit eingelöst.

### Was ich sage (30 Sekunden)
> "Drei Sätze. Erstens: Reporting zeigt euch was passiert ist. Dieses System sagt jedem Rep, was er diese Woche üben soll. Zweitens: Euer CRM weiß längst was kaputt ist, ihr habt nur nie zugehört. Drittens: forkt den Blueprint. Steckt euren Close- oder HubSpot-Key rein. Läuft heute Nacht. Danke, ab in Slido."

---

## Sprecher-Disziplin (Pflicht)

- **Keine Em-Dashes beim Sprechen.** Gedankenstrich ist Schriftsache, nicht Mundsache.
- **Kein Enthusiasmus-Fluff.** "Großartig", "absolut", "sicherlich" — alles raus.
- **Zahlen statt Adjektiven.** "8 Stunden", "52 Prozent", "11 Stunden" — nie "viel", "wenig", "schnell".
- **Englische Titel, deutscher Vortrag** (Event ist EO Deutschland, aber Slides in Phils Brand-Englisch).
- **Atempause nach Zahlen.** Nicht drüberhasten. Das Publikum muss die 8 Stunden verdauen.
- **Nie improvisieren bei Minute 8-9.** Das ist Phils Kern-Ask, da halte ich Skript.

---

## Tech-Checkliste vor dem Call

- [ ] HTML-Deck lokal testen, F11 für Fullscreen
- [ ] PDF als Backup auf Desktop
- [ ] GitHub Repo öffentlich bestätigt
- [ ] Screen-Share-Test mit Phil 1h vorher
- [ ] Telegram-Beispiel-Nachricht als Screenshot bereitlegen (falls Frage kommt)
- [ ] Google Sheet Dashboard-Screenshot bereitlegen
- [ ] Water, no coffee 30 Min vor Start (Stimme)

---

## Wahrscheinliche Q&A Antworten (Slido-Vorbereitung)

**Q: "Was, wenn wir kein Close/HubSpot nutzen?"**
A: Jede CRM-API funktioniert. Salesforce, Pipedrive, Copper. Der Skill ist 80 Zeilen Python pro CRM. Fork, passt die API-Calls an, läuft.

**Q: "DSGVO / Datenschutz bei Call-Transcripts?"**
A: Deepgram hat EU-Datacenter. Transcripts bleiben bei euch (Sheet). Claude API ist Zero-Retention, wenn der Enterprise-Account sauber aufgesetzt ist. Recording-Consent ist sowieso eure Pflicht, nicht meine.

**Q: "Was kostet das wirklich bei Scale?"**
A: Für 10 Reps mit je 30 Calls/Tag: Deepgram ca. 30$, Claude ca. 15$, Sheets gratis. Gesamt unter 50$/Monat. Bei 50 Reps linear hoch, also ca. 250$/Monat.

**Q: "Warum nicht einfach Gong?"**
A: Gong nimmt auf und hat Dashboards. Mein System diagnostiziert und schreibt Coaching. Plus: Gong startet bei 1.500$/Rep/Jahr, das hier ist quasi gratis. Nicht vs. Gong — für Teams, denen Gong zu teuer oder zu aufgebläht ist.

**Q: "Wie lange dauert Setup?"**
A: Ein Abend für den ersten Rep. Danach ist jeder weitere Rep eine Zeile Config. Voraussetzung: Call-Recordings liegen irgendwo zugänglich (MP3, WAV, Cloud-Storage).

**Q: "Halluziniert Claude beim Scoring nicht?"**
A: Ich gebe Claude den Transcript plus das Framework als Rubrik. Score 1-5 pro Dimension plus Begründungs-Zitat aus dem Call. Wenn die Begründung nicht zum Score passt, merkt man das sofort. 256 Calls getestet, Zitate matchen zu >95%.

---

## Live-Assets (für Screen-Share während des Vortrags)

**Diese drei Dokumente sind die echten Proof Points. Sie existieren, sie laufen produktiv, sie sind nicht Slideware.**

| Asset | Link | Wann im Deck zeigen |
|-------|------|---------------------|
| **Live Dashboard (Google Sheet)** | https://docs.google.com/spreadsheets/d/1l1TlfRe4_OFwh_ab8xKScbJQJM2bufv0tggQtYQrVwc/edit?gid=1022464734 | Nach Slide 5 (6-Dim Stack) — 30 Sekunden Screen-Share auf das echte Rep-Dashboard |
| **ICP Assessment v1 (ursprünglich)** | https://docs.google.com/document/d/1DM9lMWxCHd5_YdNVJcXc6Ejf6PLl_iHvfKrZM_4dieQ/edit | Slide 8 (Lead Mgmt Shifts), Shift 3 "Handoff to Marketing" — das VORHER |
| **ICP Assessment v2 (nach Rebuild)** | https://docs.google.com/document/d/1KXydHUdeXydNlkkcEBGSGMbEmxONHjAM-H3GTSw7-GA/edit | Slide 8, direkt nach v1 — das NACHHER. Die Transformation ist der Story-Moment. |

### Live-Demo-Choreographie (empfohlen)

**Option A — Minimal (sicherer):**
Nach Slide 5 kurzer ALT+TAB aufs Sheet. 20 Sekunden. "Das ist kein Mockup. Das läuft seit März. Jeder Rep, jede Dimension, jede Nacht aktualisiert." Zurück zum Deck.

**Option B — Mutiger (mehr Impact):**
Bei Slide 8 (Shift 3) beide ICP-Docs nebeneinander öffnen. 45 Sekunden. "Das war unser ICP im März. Das ist er nach 256 Calls. Sales-Daten haben Marketing umgebaut. Nicht umgekehrt." Zurück.

**Regel:** Nicht mehr als 60 Sekunden Live-Demo im 10-Minuten-Slot. Sonst reißt die Pace.

### Zahlen, die du mir noch reinpasten musst (damit sie als harte Fakten ins Deck)

Aktuell stehen auf Slide 8 diese Platzhalter — ich habe sie aus unserer ICP-Analyse vom März abgeleitet, aber du solltest die echten Live-Zahlen aus den drei Docs über mich rüberziehen lassen (entweder MCP-Drive in der nächsten Session aktivieren oder Key-Stats hier reinkopieren):

- **Shift 1 (Routing):** "4 hrs saved per SDR per week" — bitte echte Zahl aus Dashboard bestätigen
- **Shift 2 (Qualification):** "Speed-to-quote: 3.2 days → 11 hours" — bitte Live-Zahl aus CRM bestätigen
- **Shift 3 (Handoff):** "256 calls · 52% gatekeeper · 7% engaged" — bereits aus ICP-v1 bestätigt, aber was kam im v2 RAUS? (ICP-Shift: z.B. "weg von Firmen <50 MA, rein Tech-Scaleups mit Spezialrollen" — stimmt das noch nach dem Rebuild?)

Sobald du mir die Live-Werte durchgibst (oder MCP Drive in der nächsten Session läuft), tausche ich die Zahlen in `chris-deck.html` Slide 8 aus. Das macht aus generischen Metriken harten Beweis.

---

## Die Brücke zurück zum Event

Am Ende sollte jeder im Raum verstanden haben:

1. **Phil** hat gezeigt, wie Foundations aus Calls entstehen.
2. **Manu** hat gezeigt, wie Assets daraus gebaut werden.
3. **Ich** habe gezeigt, wie das operative Sales-System sich verändert, damit Schritt 1 und 2 nicht in der Schublade verstauben.

Das Deck ist ein Kreislauf, keine Addition. **Alle drei bauen auf der gleichen Goldmine — wir schürfen nur unterschiedlich tief.**
