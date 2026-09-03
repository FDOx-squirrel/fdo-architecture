# FDOx-Squirrel-Plan — Stand & offene To-Dos

Stand: 03.09.2026, vollständiger Live-Audit aller Repos in [github.com/FDOx-squirrel](https://github.com/FDOx-squirrel) (geklont, `PRIMER.md`/Commit-Historie ausgewertet) plus `n4o-rse/n4o-kg-profile`. Dieses Dokument liegt selbst in [`fdo-architecture/FDOx-Squirrel-Plan.md`](https://github.com/FDOx-squirrel/fdo-architecture/blob/main/FDOx-Squirrel-Plan.md) und soll als lebendes Dokument fortgeschrieben werden — bei jeder größeren Änderung an einem Familienmitglied hier nachziehen.

## Familie im Überblick

Alle sieben Repos liegen unter `FDOx-squirrel`, **alle sieben haben inzwischen Inhalt** (beim letzten Stand waren vier noch leer — die ausstehenden Pushes sind erledigt).

| Repo | Rolle | Status (S-Schritte laut `PRIMER.md`, falls vorhanden) |
|---|---|---|
| [`fdo-squirrel`](https://github.com/FDOx-squirrel/fdo-squirrel) | Referenzimplementierung: liest ein FDO-Paket (ZIP), schreibt `fdo-metadata.ttl` | Kein `PRIMER.md` (älter als die Familienkonvention). v0.1, publiziert (Zenodo DOI 10.5281/zenodo.18441772). Laufend gepflegt — siehe unten. |
| [`fdo-squirrel-registry`](https://github.com/FDOx-squirrel/fdo-squirrel-registry) | Erntet von Zenodo, DCAT-Bundle + CRM-Bridge, SHACL-Gate, N4O-Export, Facetten- + SPARQL-Seite | **S0–S7 fertig.** S8 (Registry als FDO, Release/CI) und S9 (N4O-Andockung) offen. |
| [`fdo-squirrel-md-generator`](https://github.com/FDOx-squirrel/fdo-squirrel-md-generator) | Web-Generator für `MD.cff`+`CITATION.cff` | Nur `PRIMER.md` im Repo. **S0 (Entscheidungen) fertig, S1–S7 (aller Code) offen.** |
| [`fdo-squirrel-spec`](https://github.com/FDOx-squirrel/fdo-squirrel-spec) | ReSpec-HTML-Doku des Metadatenformats | **S1 fertig** (`docs/index.html` rendert offline). S2 (echtes Beispiel statt kaputtem Demo-TTL), S3 (`fetch` auf Tag statt `main` pinnen) offen. |
| [`fdo-architecture`](https://github.com/FDOx-squirrel/fdo-architecture) | Meta-Repo: `registry.yaml` + Mermaid-Übersicht + dieser Plan | **S0–S1 fertig.** `registry.yaml` ist veraltet — siehe To-Do unten. |
| [`fdo-3d-packager`](https://github.com/FDOx-squirrel/fdo-3d-packager) | Sketchfab/lokales 3D-Modell → `fdo:3DDataFDO`-Paket | **S0–S1 fertig** (Skeleton, 7 Schritte). S2–S7 (Implementierung) offen. |
| [`fdo-git-packager`](https://github.com/FDOx-squirrel/fdo-git-packager) | Git-Repo (fester Commit) → `fdo:SoftwareFDO`-Paket | **S0–S1 fertig** (Skeleton, 6 Schritte). S2–S6 (Implementierung) offen. |

**Verwandtes externes Repo (andere Org, kein Teil der Familie, aber Abnehmer/Partner):**

| Repo | Rolle | Status |
|---|---|---|
| [`n4o-rse/n4o-kg-profile`](https://github.com/n4o-rse/n4o-kg-profile) | Projektübergreifendes Werkzeug: `metadata.yaml` → per GitHub Action Metadaten-RDF, CIDOC-CRM-Anbindung, browserbasierte SPARQL-Seite, damit eine Collection in den NFDI4Objects Knowledge Graph aufgenommen werden kann | Hat jetzt echten Inhalt (`profile/`, `build/`, `action.yml`, `example/` mit Beispieldaten). **Aber:** in `fdo-squirrel-registry`s aktuellem `PRIMER.md` (S8/S9) taucht dieses Repo nirgends auf — siehe Abhängigkeit 4 unten. |

---

## Status & To-Dos je Repo

### `fdo-squirrel`
Kein `PRIMER.md`, daher aus der Commit-Historie abgelesen statt aus einer Schritttabelle. Seit dem letzten Bericht sind mehrere weitere Fixes gelandet, zusätzlich zu den beiden bekannten Patches:
- ✅ Patch #1 (CRM-Klassen-IRIs, `xsd:gYear`, GeoSPARQL-BBox, fehlende Labels).
- ✅ Patch #2 (`Bundle generated files into one finished FDO package`) — das fertige Bundle-ZIP-Feature ist im Repo, nicht mehr nur verifiziert und wartend.
- ✅ Weitere, in diesem Projekt bisher nicht dokumentierte Fixes: Mermaid-Diagramm zeigte räumliche/zeitliche Namen nicht an (behoben), Mermaid-Markdown-String-Modus für Diagrammbeschriftungen aktiviert, `MD.cff`-Felder `keywords`/`related_resources` emittierten nicht + ein Datatype-Override-Bug (behoben), `MD.cff`-Identifier erzeugten gar kein RDF (behoben, aktueller HEAD).
- **To-Do:** Diese letzten vier Fixes sind nicht aus den bisher bekannten Chats dieses Projekts nachvollziehbar — falls sie in einem anderen Chat/Projekt entstanden sind, lohnt es sich, deren Kontext (Ursache, Testabdeckung) hier oder im nächsten `fdo-squirrel`-Chat kurz festzuhalten, damit das Wissen nicht nur im Commit-Message steckt.
- **To-Do (weiterhin offen, aus dem Registry-Qualitätsbericht):** abgekürzte Klassen-IRIs außerhalb der bereits gepatchten Stellen, `xsd:integer` an weiteren Zeitgrenzen, doppelte Prozentkodierung der `content/`-IRIs (siehe Registry-Sektion), `<DOI>_geom`/`<DOI>_temporal`-IRIs in fremdem Namensraum — alle in `fdo-squirrel-registry/PRIMER.md` Teil D als „Rückfluss nach fdo-squirrel" gesammelt.
- **Empfehlung:** Da dieses Repo mittlerweile so viele Nachbesserungen bekommt, könnte ein eigenes `PRIMER.md` (nach dem Familienmuster) helfen, den Überblick zu behalten — bisher lebt der Stand nur in Commit-Messages.

### `fdo-squirrel-registry`
- ✅ **S0–S7 vollständig erledigt:** Skeleton, Zenodo-Harvest, CRM-Crosswalk, DCAT-Bundle, SHACL-Gate + Qualitätsbericht, Registry-Index + Facettenseite, S6b (Autoescape-Fix), SPARQL-Seite. Das ist mehr, als der letzte Bericht zeigte — S7 war zum letzten Check noch als „angelaufen" markiert, ist laut `PRIMER.md` jetzt fertig.
- **Offen: S8 — Registry als FDO, Release und CI.** `MD.cff`+`CITATION.cff` fürs Repo selbst, `fdo_type` noch zu entscheiden (`fdo:AnalysisFDO` oder neuer `fdo:RegistryFDO` — betrifft dann `fdo-squirrel`), Bundle+Index+Shapes als ZIP durch `fdo-squirrel` schicken und auf Zenodo publizieren, zwei GitHub Actions (Gate bei jedem Push, Pages-Deploy).
- **Offen: S9 — N4O-Andockung.** Eintrag in `n4o-collections.json` (nfdi4objects/n4o-databases), vorher zu klären: Lieferform, Collection vs. Datenbank-Eintrag, Wikidata-Item, Verhältnis zur N4O Objects Ontology (mit A. Noback/A. Gerber) — **dieser Abschnitt referenziert `n4o-kg-profile` nicht**, siehe Abhängigkeit 4.
- **To-Do:** Doppelte Prozentkodierung der `content/`-IRIs — laut Teil D entschieden, dass der Fix **upstream in `fdo-squirrel`** landet, nicht hier; Zeitpunkt hängt am Qualitätsbericht.
- Weitere in Teil D gesammelte, noch offene Kleinigkeiten: Label-Pflege für fremde IRIs (`registry/labels.json`, aktuell 14 Einträge, von Hand), kein Einreichungsweg für Dritte, nur Zenodo als Quelle, vier von sieben TTL im Bestand mit deklarierten Reparaturen statt sauberen Originalen.

### `fdo-squirrel-spec`
- ✅ S1 fertig (gepusht, `docs/index.html` rendert offline).
- **To-Do S2:** echtes, valides `fdo-metadata.ttl` als Vorzeigebeispiel statt des kaputten Demo-TTL — offene Frage, ob aus `fdo-squirrel-registry` referenziert oder eine eigene kuratierte Minimalinstanz gepflegt wird.
- **To-Do S3:** `fetch` von `main`-Branch auf einen festen Tag umstellen, sobald `fdo-squirrel` Releases taggt.
- Kleinigkeit: ORCID in `CITATION.cff` ist noch Platzhalter.

### `fdo-squirrel-md-generator`
- ✅ S0 (alle Entscheidungen: Tech-Stack, Schema-Quelle, Mapping-Regeln) fertig.
- **To-Do:** Immer noch **kein Code** — S1 (Skeleton) bis S7 (`CITATION.cff`-Ableitung) sind alle offen, das Repo enthält bislang nur `PRIMER.md`. Von allen sieben Repos das mit dem größten Rückstand zwischen Planung und Umsetzung.

### `fdo-architecture`
- ✅ S0–S1 fertig, `FDOx-Squirrel-Plan.md` (dieses Dokument) liegt im Repo.
- **To-Do — `registry.yaml` ist veraltet**, in drei Punkten:
  1. Fehlt: `fdo-3d-packager` und `fdo-git-packager` als Einträge.
  2. `org`-Feld für `fdo-squirrel` und `fdo-squirrel-registry` steht noch auf `Research-Squirrel-Engineers` — beide sind längst zu `FDOx-squirrel` umgezogen.
  3. `status`-Text für `fdo-squirrel-registry` sagt noch „im Bau" — tatsächlich S0–S7 fertig (siehe oben).
  4. Zu klären, ob `n4o-kg-profile` als externes System (wie `squirrelbase`) aufgenommen wird, sobald sein Verhältnis zur Registry geklärt ist (Abhängigkeit 4).
- Vorgeschlagen, aber noch **nicht umgesetzt**: CI-Workflow (`--strict` bei jedem Push), `check-links`-Schritt gegen echte GitHub-URLs, Cross-Repo-Backlog im Architektur-Repo, Rücklinks in den READMEs der anderen Repos.

### `fdo-3d-packager`
- Zweck: Sketchfab-Modell oder lokale Datei → fertiges `fdo:3DDataFDO`-Paket im `fdo-squirrel`-Layout (Viewer inklusive, `distributions[]` bewusst nicht vorbefüllt).
- ✅ S0–S1 fertig und gepusht (Initial Commit).
- **To-Do:** S2–S7 (`fetch`, `convert`, `nexus`, `mdcff`, `bundle`, `build_fdo`) sind alle noch Stubs.
- **Offen:** Einbindungsmechanismus für `fdo-squirrel` in S7 (pip aus GitHub, Git-Submodule oder externer Pfad) — identisch mit der offenen Frage bei `fdo-git-packager`, einmal klären gilt für beide.

### `fdo-git-packager`
- Zweck: Git-Repo + fester Commit-SHA → fertiges `fdo:SoftwareFDO`-Paket, Working Tree flach auf ZIP-Root (sonst greifen `fdo-squirrel`s `path_prefix`-Klassifikationsregeln nicht).
- ✅ S0–S1 fertig und gepusht (Initial Commit).
- **To-Do:** S2–S6 (`fetch`, `inspect`, `mdcff`, `bundle`, `build_fdo`) sind alle noch Stubs.
- **Offen:** gleiche `fdo-squirrel`-Einbindungsfrage wie oben; zusätzlich unbestätigt, ob eine im Ziel-Repo vorhandene `CITATION.cff` wirklich immer Vorrang vor einer synthetisierten haben soll.

### `n4o-kg-profile` (extern, Org `n4o-rse`)
- Muster: *Source-Repo* baut das Bundle → *Collection-Repo* pflegt nur `metadata.yaml` + `rdf/<name>-bundle.ttl`, referenziert `n4o-kg-profile` als versionierten Tag (`@v1`) in einer GitHub Action → `n4o-kg-profile` liefert `profile/` + `build/` (Metadaten-RDF, CIDOC-CRM-Crosswalk, SPARQL-Seite via GitHub Pages).
- ✅ Hat jetzt echten Inhalt: `profile/profile.ttl`, `profile/shapes.ttl`, `profile/context.jsonld`, `profile/CROSSWALK.md`, `build/make_metadata.py`, `build/build_sparql.py`, `action.yml`, ein vollständiges `example/`.
- **To-Do:** siehe Abhängigkeit 4 — klären, ob und wie `fdo-squirrel-registry`s S8/S9 dieses Muster nutzt.

---

## Abhängigkeiten

1. **`fdo-squirrel`s neueste Fixes → `fdo-squirrel-registry`**: Vier weitere Fixes (Mermaid-Diagramm, `MD.cff`-Keywords/Identifiers) sind seit dem letzten Bericht gelandet. Vor dem nächsten Registry-Harvest-Lauf lohnt ein Blick, ob sich dadurch der Qualitätsbericht (`dist/quality_report.md`) verbessert hat.
2. **Doppelte Prozentkodierung** bleibt Aufgabe der Registry (`content_iri()`), nicht von `fdo-squirrel` — Entscheidung steht fest in `fdo-squirrel-registry/PRIMER.md` Teil D.
3. **`fdo-architecture`/`registry.yaml` ist veraltet** (siehe oben, drei konkrete Punkte) — sollte vor der nächsten Diagramm-Generierung aktualisiert werden, sonst zeigt das öffentliche Familienbild einen falschen Stand.
4. **`n4o-kg-profile` ↔ `fdo-squirrel-registry` S8/S9 — Widerspruch zu klären.** Frühere Chats in diesem Projekt hatten einen Hinweis auf `n4o-kg-profile` als projektübergreifendes Muster für S8/S9 vorbereitet; **im aktuell live stehenden `PRIMER.md` der Registry ist davon nichts zu finden** — S9 beschreibt weiterhin ausschließlich den `n4o-collections.json`/`n4o-graph-importer`-Weg. Das ist entweder ein noch nicht angewendeter Patch oder eine bewusste spätere Korrektur — vor S8/S9 zu klären, welcher Weg tatsächlich gilt, bevor daran weitergebaut wird.
5. **`fdo-3d-packager`/`fdo-git-packager` → `fdo-squirrel`-Einbindung**: gemeinsame offene Design-Frage, einmal klären genügt für beide.
6. **RSE-Tauglichkeit der ganzen Familie** (CITATION.cff-ORCIDs, Zenodo-Releases pro Repo, einheitliche CONTRIBUTING.md) weiterhin angekündigt, noch nicht begonnen.

---

*Hinweis: Dieser Stand basiert auf einem vollständigen Klon aller sieben Repos plus `n4o-kg-profile` am 03.09.2026 (Commit-Historien und `PRIMER.md`-Inhalte ausgewertet), nicht mehr nur auf Chatverlauf. Bei Widersprüchen zwischen diesem Dokument und einem `PRIMER.md` gilt das jeweilige `PRIMER.md` des Repos als genauer — dieses Dokument ist die Zusammenfassung, nicht die Quelle der Wahrheit.*
