# Primer — fdo-architecture

Arbeitsplan für `fdo-architecture`: ein Repo, das die FDOx-Familie selbst
beschreibt — welche Repos es gibt, was sie produzieren, was sie voneinander
konsumieren — als ein von Hand gepflegtes `registry.yaml`, gerendert zu einem
Mermaid-Diagramm und einer statischen Übersichtsseite.

**Ort.** <https://github.com/FDOx-squirrel/fdo-architecture/blob/main/PRIMER.md>
(Repo-Name ist ein Vorschlag, siehe A4.)

**So wird es benutzt.** Es wird in jedem Chat vollständig hochgeladen. Danach
genügt ein Satz: „Wir machen S3." Teil A gilt immer, Teil B ist die Übersicht,
Teil C beschreibt den einzelnen Schritt. Die Statusspalte in Teil B und die
Beschlusslage in A4 werden nach jedem Chat nachgeführt, damit spätere Chats den
aktuellen Stand sehen.

---

# Teil A — Immer gültig

## A1 Ausgangslage

**Die FDOx-Familie wächst schneller, als einzelne PRIMER.md-Dateien die
Beziehungen zwischen den Repos tragen können.** Wer was produziert und wer das
konsumiert, steht bisher verstreut in den A1-Tabellen der einzelnen Repos
(`fdo-squirrel-registry`s „Zwei Repos, eine Kette", `fdo-squirrel-spec`s
Quellenliste) und driftet auseinander, sobald sich eins ändert, ohne dass das
andere nachgezogen wird. `fdo-architecture` bündelt das an einer Stelle.

| Repo | Org | Rolle |
|---|---|---|
| `fdo-squirrel` | Research-Squirrel-Engineers | FDOx-Referenzimplementierung: ZIP → `fdo-metadata.ttl` |
| `fdo-squirrel-md-generator` | FDOx-squirrel | MD.cff/CITATION.cff-Generator |
| `fdo-squirrel-spec` | FDOx-squirrel | Dokumentation: ReSpec-Seite aus Kopien der `fdo-squirrel`-Quellen |
| `fdo-squirrel-registry` | Research-Squirrel-Engineers | Erntet Zenodo-Pakete, DCAT-Katalog + CRM-Anker + SHACL-Gate |
| `SquirrelBase` (Wikibase) | — | externer Meta-Hub, hält die FDO-URL je 3D-Objekt |

**Befunde (geprüft 2026-09-03, aus vorigen Chats zu den einzelnen Repos):**

- `fdo-squirrel` publiziert `fdo-metadata.ttl` unter DOI
  `10.5281/zenodo.18441772` (v0.1, Squirrel Papers 8(1) §4).
- `fdo-squirrel-spec` liest genau vier Quellendateien aus `fdo-squirrel`
  (`MD.cff-schema.yaml`, `crosswalk_md_cff_to_rdf.yaml`,
  `classification_rules.yaml`, `package_source.py`) per
  Kandidatenliste, snapshotet sie in `data/raw/` und publiziert selbst kein
  RDF. S1 gebaut und per Patch-ZIP ausgeliefert.
- `fdo-squirrel-registry` liest ihre Quellenliste aus einem kuratierten
  `registry/sources.json` (DOIs), verankert an CIDOC CRM über das
  N4O-Anwendungsprofil `crm-rdf-ap` (das E55, E52/P82a/b und E41 ausdrücklich
  untersagt), und liefert eine Facettenseite getrennt von der
  SPARQL-Seite, damit niemand auf eine WASM-Runtime warten muss, um nach
  „3D" zu filtern.
- **`fdo-squirrel-md-generator`s Rolle ist nicht am echten Repo verifiziert.**
  Sie steht in `registry.yaml` mit einer entsprechenden Notiz und als
  gestrichelte Kante im Diagramm, nicht als gesicherter Befund — siehe Teil D.
- `fdo-squirrel-registry` hat einen eigenen Bug (doppelte Prozentkodierung im
  Bundle-Build) von einem vermuteten `fdo-squirrel`-Fehler unterschieden und
  korrigiert; das betrifft `fdo-architecture` nicht direkt, zeigt aber, warum
  eine repo-übergreifende Übersicht nützlich ist — der Fehler wurde erst beim
  Rückfluss zwischen zwei Repos sichtbar.

## A2 Zielbild

```
registry.yaml (Quelle, von Hand gepflegt)
        │
        ▼
python main.py validate  ──▶  Fehlerbericht (fehlende Felder, tote Referenzen)
        │
        ▼
python main.py render    ──▶  dist/architecture.mmd  (Mermaid-Quelltext, versioniert)
                          ──▶  docs/index.html         (Diagramm + Tabelle, GitHub Pages)
```

Eigenschaften, die das fertige Ding hat:

1. `registry.yaml` ist die einzige Stelle, an der eine Repo-Beziehung
   eingetragen wird — `dist/architecture.mmd` und `docs/index.html` werden nie
   von Hand angefasst.
2. Jeder Knoten im Diagramm verlinkt auf das echte GitHub-Repo (Mermaid
   `click`) — keine Karteileiche ohne URL.
3. `python main.py` zweimal hintereinander → `git status` bleibt leer.
4. Kein Rendering-Build auf der GitHub-Pages-Seite: `docs/index.html` ist eine
   einzelne statische Datei, Mermaid lädt sich per `<script>` aus dem CDN —
   genau das Muster, das `fdo-squirrel-spec` für ReSpec schon nutzt.
5. `validate` meldet jede `consumes[].from`-Referenz, die keine existierende
   `id` trifft, als Fehler — verhindert eine still driftende Kante.

## A3 Querschnittsregeln

- **Kein Fetch-Schritt.** `registry.yaml` wird von Hand gepflegt, nicht
  geerntet — anders als bei `fdo-squirrel-registry` gibt es hier keine
  Netzwerkgrenze zu ziehen, weil es gar kein Netzwerk im Pipeline-Lauf gibt.
- `dist/` und `docs/` sind generiert, aber **versioniert** — sie sind das
  zitierbare Erzeugnis dieses Repos, kein Build-Abfall. `.gitignore`
  ignoriert sie deshalb bewusst nicht (siehe `primer-repo`-Skill).
- Kein `datetime.now()` im Output. `RELEASE` in `py/architecture_utils.py`
  ist die einzige Stelle, an der ein Datum im generierten Output erscheinen
  darf.
- Zweimal laufen lassen, `git status` muss danach leer sein.
- `PRIMER.md` ist Deutsch, alles andere (Code, README, Kommentare) ist
  britisches Englisch.
- Windows ist die Referenzplattform: `cmd`-Befehle einzeilig.
- Kommunikation informell ("du").

## A4 Beschlusslage

| Frage | Beschluss | seit |
|---|---|---|
| Scope der Familie | nur FDOx (`fdo-squirrel`, `-spec`, `-registry`, `-md-generator`, SquirrelBase); die `wdt-*`-Familie bewusst aussen vor | 2026-09-03 |
| Ziel-Org | `FDOx-squirrel` | 2026-09-03 |
| Repo-Name | `fdo-architecture` | Vorschlag |
| Diagramm-Tool | Mermaid, clientseitig per CDN-Script in `docs/index.html` (wie ReSpec bei `fdo-squirrel-spec`); Quelltext zusätzlich in `dist/architecture.mmd` versioniert | Vorschlag |
| `registry.yaml`-Schema | Liste unter `repos:` mit `id`/`kind`/`org`/`url`/`role`/`status`/`produces[]`/`consumes[]`; `consumes[].from` verweist auf eine andere `id` oder ist `null` für externe Eingaben | Vorschlag |
| Datenquelle | von Hand gepflegtes `registry.yaml`, kein Harvesting, kein Fetch-Schritt | Vorschlag |
| Unsichere Kanten | Einträge mit „nicht verifiziert"/„vermutet" in der Notiz werden im Diagramm gestrichelt gezeichnet, nicht stillschweigend als gesichert dargestellt | Vorschlag |
| Statusanzeige nach aussen | `status_level` (`done`/`in-progress`/`error`) als eigenes Pflichtfeld neben `status`; die Seite zeigt eine farbige Badge (grün/gelb/rot) plus einen kurzen Ein-Satz-Status, nicht mehr den vollen Fließtext. Lange Historie (Befund-Nummern, Patch-Verläufe) gehört ins jeweilige `PRIMER.md`/`FDOx-Squirrel-Plan.md`, nicht auf die öffentliche Seite | 2026-09-04 |
| Sprache von `registry.yaml`/Seite | A3s Regel („alles ausser `PRIMER.md` ist Englisch") war nie umgesetzt — `registry.yaml`s `role`/`status`-Werte und `docs/index.html` waren deutsch. Am 2026-09-04 nachgezogen, keine neue Regel, nur die bestehende endlich angewendet | 2026-09-04 |

## A5 Was in welchem Chat hochgeladen wird

Bundle: `PRIMER.md` + `registry.yaml` + `main.py` + `py/` + `requirements.txt`
+ `.gitignore`. **Nicht hochladen:** `dist/`, `docs/`, `__pycache__/`, `.git/`
— alles davon wird von `python main.py` neu erzeugt.

```cmd
robocopy . fdo-architecture-bundle PRIMER.md registry.yaml main.py requirements.txt .gitignore /S
robocopy py fdo-architecture-bundle\py /S
powershell Compress-Archive -Path fdo-architecture-bundle\* -DestinationPath fdo-architecture-bundle.zip -Force
```

A6 entfällt für dieses Repo — es publiziert kein eigenes RDF, nur eine
Übersicht über andere Repos.

---

# Teil B — Schrittübersicht

| ID | Schritt | Repo | hängt ab von | Status |
|---|---|---|---|---|
| S0 | Festlegungen: Repo-Name, Diagramm-Tool, `registry.yaml`-Schema | `fdo-architecture` | — | erledigt 2026-09-03 |
| S1 | Skelett: `main.py`, `registry.yaml` (Erstbefüllung), `validate`- und `render`-Schritt | `fdo-architecture` | S0 | erledigt 2026-09-03 |
| S2 | Weitere Familienmitglieder pflegen | `fdo-architecture` | S1 | laufend — kein Abnahmeschritt, siehe Teil C |
| S3 | Englisch + Status-Ampel | `fdo-architecture` | S1 | erledigt 2026-09-04 |

S0 und S1 sind in diesem Chat zusammen entstanden, weil die Entscheidungen aus
S0 unmittelbar in die `registry.yaml`-Struktur von S1 eingeflossen sind.
Künftige Schritte (z. B. Rückfluss-Prüfung für `fdo-squirrel-md-generator`,
siehe Teil D) sind unabhängig voneinander und können in beliebiger Reihenfolge
laufen.

---

# Teil C — Die Schritte

## S0 — Festlegungen

**Ziel:** Repo-Name, Diagramm-Tool und `registry.yaml`-Schema stehen fest,
bevor Code entsteht — spätere Änderungen daran würden generierten Output
umschreiben.

**Uploads:** keine, reine Entscheidungsrunde.

Entschieden im Chat vom 2026-09-03: Scope (nur FDOx) und Ziel-Org
(`FDOx-squirrel`) direkt bestätigt; Repo-Name, Diagramm-Tool und
`registry.yaml`-Schema als Vorschlag gesetzt (Details in A4), weil sie sich
unmittelbar aus dem bestehenden Familienmuster ergeben (Mermaid via
`fdo-mermaid-viz`, statische Einzeldatei-Seite via `fdo-squirrel-spec`) und
keine eigene Diskussion brauchten.

**Abnahme:** A4 enthält Repo-Name, Diagramm-Tool und Schema mit Datum.

### Erledigt 2026-09-03

Alle sechs Fragen aus A4 beantwortet oder als Vorschlag gesetzt. Keine
Überraschung — die Entscheidungen folgen durchgehend dem, was in der Familie
schon existiert (kein neues Muster erfunden).

## S1 — Skelett

**Ziel:** `python main.py` läuft, `registry.yaml` enthält die fünf bekannten
Einträge der FDOx-Familie, `validate` und `render` sind lauffähig und
deterministisch.

**Uploads:** keine — S1 ist der Erstaufbau dieses Repos, es gibt noch nichts
Bestehendes zum Hochladen.

Layout:

```
fdo-architecture/
├── PRIMER.md
├── README.md
├── LICENSE
├── CITATION.cff
├── requirements.txt
├── .gitignore
├── main.py
├── py/
│   ├── architecture_utils.py   RELEASE, Pfade, ensure_dirs(), write_text()
│   ├── step_validate.py        Schema- und Referenzprüfung
│   └── step_render.py          Mermaid + docs/index.html
├── registry.yaml                Quelle: fünf Einträge (vier Repos + SquirrelBase)
├── dist/
│   └── architecture.mmd         generiert, versioniert
└── docs/
    └── index.html                generiert, GitHub Pages
```

`registry.yaml` enthält die fünf Einträge aus A1, inklusive der als unsicher
markierten Kante `fdo-squirrel-md-generator → fdo-squirrel`. `step_render.py`
zeichnet diese Kante gestrichelt (`-. label .->`), damit die Unsicherheit im
Diagramm sichtbar bleibt und nicht wie eine geprüfte Beziehung aussieht.

**Abnahme:** `python main.py` läuft zweimal hintereinander durch, `git
status` bleibt nach dem zweiten Lauf leer (Test unten), `docs/index.html`
enthält alle fünf `id`s aus `registry.yaml`, `dist/architecture.mmd` beginnt
mit `flowchart LR` und enthält für jeden Eintrag genau einen Knoten.

### Erledigt 2026-09-03

Im Sandkasten geprüft: `python main.py`, `--list`, `--dry-run`, `--only
render`, `--strict` liefen alle wie im Vertrag beschrieben. Zwei Läufe von
`python main.py render` hintereinander erzeugten byte-identische
`dist/architecture.mmd` und `docs/index.html` (`diff` leer). Frisches,
unversioniertes Verzeichnis mit `git init` + zwei vollständigen
`main.py`-Läufen bestätigt: `git status` ist nach dem zweiten Lauf leer bis
auf die einmalig neu angelegten Pfade aus dem ersten Lauf.

### Nachtrag 2026-09-04, `registry.yaml` auf den aktuellen Familienstand gebracht

Anlass war `FDOx-Squirrel-Plan.md`s eigener Hinweis, dass das öffentliche
Familienbild sonst einen falschen Stand zeigt. Vier Änderungen: `org:` für
`fdo-squirrel`/`fdo-squirrel-registry` von `Research-Squirrel-Engineers` auf
`FDOx-squirrel` korrigiert (beide sind längst umgezogen, GitHub hält zwar
einen Redirect, aber `registry.yaml` soll das nicht brauchen); `status:` der
Registry von „im Bau" auf S0–S9 aktualisiert; `fdo-3d-packager` und
`fdo-git-packager` als fehlende Einträge ergänzt; `n4o-kg-profile` (als
`external-system`, Org `n4o-rse`) und das neue `fdox-squirrel-n4o-collection`
aufgenommen, inklusive der Kante zwischen beiden. `python main.py --strict`
danach: 9 Einträge, 0 Fehler, 0 Warnungen; `dist/architecture.mmd` und
`docs/index.html` neu gebaut, nicht von Hand nachgezogen.

## S2 — Weitere Familienmitglieder pflegen

**Ziel:** Kein eigener Abnahmeschritt wie S0/S1, sondern die laufende
Verpflichtung aus A2 („Registry synchron"): sobald ein Repo der Familie
substanziell weiterkommt oder neu hinzukommt, wird `registry.yaml` — und
damit `FDOx-Squirrel-Plan.md` — im selben Zug nachgezogen, nicht erst, wenn
das Diagramm sichtbar falsch liegt.

### Erledigt 2026-09-04

Siehe Nachtrag unter S1: `registry.yaml` von sieben auf neun Einträge
gebracht (die drei alten Fehler behoben, zwei Repos ergänzt, `n4o-kg-profile`
neu als externes System), `FDOx-Squirrel-Plan.md` komplett neu geschrieben
mit dem Stand aller acht Familienrepos plus `n4o-kg-profile`.

### Erledigt 2026-09-07, `fdo-squirrel-md-generator` v0.1 + `fdo-3d-packager` S0–S9

Zwei Familienmitglieder seit dem letzten Stand substanziell weitergekommen,
`registry.yaml`/`FDOx-Squirrel-Plan.md` entsprechend nachgezogen:

- **`fdo-squirrel-md-generator`**: von `status_level: in-progress`
  ("Decisions done, no code yet") auf `done` — v0.1 live, über fünf
  Feedback-Runden im echten Browser verifiziert (siehe dessen eigenes
  `PRIMER.md` A6–A10). `consumes` war vorher leer; jetzt die tatsächliche
  Kante zu `fdo-squirrel` (Live-Fetch von `MD.cff-schema.yaml`) ergänzt.
- **`fdo-3d-packager`**: von `status_level: in-progress` ("Skeleton done
  (seven steps), implementation not started") auf `done` — komplette
  Pipeline (`fetch`→`build_fdo`, S0–S9), inklusive eines erfolgreichen
  echten Rundlaufs durch `fdo-squirrel` (S7). Die vorher offene
  Einbindungsfrage (`consumes.note`) ist jetzt konkret beantwortet:
  gepinnte `pip`-Abhängigkeit von GitHub, Commit `504b7af`.
- **`fdo-squirrel`**s `consumes`-Notiz zu `fdo-squirrel-md-generator` von
  "Assumed link, not verified" auf einen genaueren, weiterhin ehrlichen
  Stand aktualisiert (Schema-Kompatibilität ist durch den Live-Fetch
  gegeben, ein tatsächlicher Ingest-Rundlauf für ein dort erzeugtes
  `MD.cff` steht — anders als bei `fdo-3d-packager` — noch aus).

Quelle: frischer Klon beider Repos, `fdo-3d-packager` zusätzlich per
`requirements.txt`/`step_build_fdo.py`-Lektüre auf die tatsächliche
`fdo-squirrel`-Einbindung hin geprüft, nicht nur aus der `PRIMER.md`
übernommen. `python main.py --strict` danach: weiterhin 9 Einträge, 0
Fehler, 0 Warnungen; `dist/architecture.mmd`/`docs/index.html` neu gebaut.

## S3 — Englisch + Status-Ampel

**Ziel:** die Seite und `registry.yaml`s `role`/`status`-Werte tatsächlich
englisch, wie A3 es seit S0 verlangt, aber nie umgesetzt war. Dazu eine grob
granulare Statusanzeige (`status_level`: `done`/`in-progress`/`error`) statt
Fließtext, damit ein Aussenstehender die Seite auf einen Blick liest, ohne
Patch-Historie mitlesen zu müssen.

**Uploads:** keine, Änderung an bestehendem Repo.

**Was gemacht wurde:**

- `registry.yaml`: alle `role`/`status`-Werte ins Englische übersetzt, `note`-Felder ebenso (inkl. `UNVERIFIED_MARKERS` in `step_render.py`, die
  auf den `note`-Text matchen — sonst hätte die gestrichelte Kante lautlos
  aufgehört zu funktionieren). Neues Pflichtfeld `status_level` je Eintrag.
- `py/step_validate.py`: `status_level` zu `REQUIRED_FIELDS`, geprüft gegen
  `VALID_STATUS_LEVELS = ("done", "in-progress", "error")`.
- `py/step_render.py`: `_status_badge()` rendert eine farbige Pille
  (grün/gelb/rot) aus `status_level`, mit einem Fallback auf ein neutrales
  Grau plus dem Rohwert, falls doch mal ein unbekannter Wert durchrutscht —
  die Seite soll nie leer bleiben, nur weil ein Feld fehlt. Der bisherige
  Fließtext steht klein darunter (`status`, jetzt bewusst kurz gehalten,
  Detail gehört ins jeweilige `PRIMER.md`). Seite komplett auf Englisch
  (`<html lang="en">`, Titel, Spaltenköpfe, Legende).
- `py/architecture_utils.py`: `RELEASE` von `2026-09-03` auf `2026-09-04`
  nachgezogen — war beim `registry.yaml`-Update aus S2 übersehen worden
  (A3, „Kein `datetime.now()`" — dafür muss die Konstante aber auch
  tatsächlich mitgezogen werden, das ist an mir vorbeigelaufen).

**Abnahme:** `python main.py --strict` läuft fehlerfrei; zwei Läufe von
`--only render` hintereinander erzeugen byte-identische `docs/index.html`;
kein `status_level` fehlt oder liegt ausserhalb der drei erlaubten Werte.

### Erledigt 2026-09-04

Geprüft: `9 entries, 0 errors, 0 warnings`, Reproduzierbarkeit bestätigt
(`diff` zwischen zwei Läufen leer). Aktuell nutzt kein Eintrag
`status_level: error` — passt zum echten Stand, niemand in der Familie ist
gerade blockiert, nur unterschiedlich weit. **Nicht geprüft:** wie die Badges
tatsächlich in einem Browser aussehen — das ist erst bewiesen, wenn jemand
`docs/index.html` öffnet (dieselbe Lehre wie in `fdo-squirrel-registry`,
Befund 28: eine Seite ist erst geprüft, wenn ein Browser sie gezeichnet hat).

---

# Teil D — Offene Punkte

- **`fdo-squirrel-md-generator`s tatsächliche Rolle.** Bisher nur aus dem
  Repo-Namen erschlossen, nicht am echten Code geprüft (kein Zugriff ohne
  Auth aus diesem Chat heraus). Sobald das Repo in einem Chat hochgeladen
  oder geklont werden kann, gehört das als eigener kurzer Schritt hierher:
  `produces`/`consumes` in `registry.yaml` korrigieren, die Kante im
  Diagramm von gestrichelt auf durchgezogen setzen.
- ~~**Migration der `Research-Squirrel-Engineers`-Repos.**~~ Erledigt
  2026-09-04: `fdo-squirrel` und `fdo-squirrel-registry` sind längst nach
  `FDOx-squirrel` umgezogen, `org:`/`url:` in `registry.yaml` sind
  nachgezogen. Bei diesem Durchgang gleich mit erledigt: `status:` der
  Registry auf S0–S9 aktualisiert, `fdo-3d-packager`/`fdo-git-packager` als
  Einträge ergänzt, `n4o-kg-profile` (extern) und `fdox-squirrel-n4o-collection`
  neu aufgenommen. `python main.py --strict`: 9 Einträge, 0 Fehler.
- **`wdt-*`-Familie bewusst aussen vor** (Scope-Entscheidung 2026-09-03).
  Falls das später gewünscht ist: eigenes `registry.yaml` für die
  `wdt-*`-Familie, oder ein `family:`-Feld zum Filtern in einer gemeinsamen
  Datei — noch keine Präferenz, weil noch kein Bedarf.
- **Farbschema/Legende im Diagramm.** Aktuell zwei `classDef`s (Repo,
  externes System) ohne sichtbare Legende auf der Seite. Klein genug, um bei
  Bedarf in `render` nachzuziehen, sobald es tatsächlich stört.
