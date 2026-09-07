# FDOx-Squirrel-Plan — Stand & offene To-Dos

Stand: 07.09.2026. Aktualisiert nach Abschluss von `fdo-squirrel-md-generator` v0.1 (Formular, Live-Validierung, Round-Trip-Laden, ZIP-Validator, Karte, Wikidata/OSM-Lookup — alles im echten Browser verifiziert) und `fdo-3d-packager` S0–S9 (kompletter Pipeline-Durchlauf `fetch`→`build_fdo`, inkl. eines echten Rundlaufs durch `fdo-squirrel`). `registry.yaml` in diesem Repo ist mit diesem Stand synchron (`python main.py --strict` läuft fehlerfrei, `dist/architecture.mmd`/`docs/index.html` neu gebaut). Dieses Dokument liegt selbst in [`fdo-architecture/FDOx-Squirrel-Plan.md`](https://github.com/FDOx-squirrel/fdo-architecture/blob/main/FDOx-Squirrel-Plan.md) und soll bei jeder größeren Änderung an einem Familienmitglied nachgezogen werden.

## Familie im Überblick

Acht Repos unter `FDOx-squirrel` (sieben plus ein neu hinzugekommenes), dazu ein externes Werkzeug in einer anderen Org, das zwei der Familienmitglieder tatsächlich benutzen.

| Repo | Rolle | Status (S-Schritte laut `PRIMER.md`, falls vorhanden) |
|---|---|---|
| [`fdo-squirrel`](https://github.com/FDOx-squirrel/fdo-squirrel) | Referenzimplementierung: liest ein FDO-Paket (ZIP), schreibt `fdo-metadata.ttl` | Kein `PRIMER.md`. v0.1, publiziert (Zenodo DOI 10.5281/zenodo.18441772). Laufend gepflegt — siehe unten. |
| [`fdo-squirrel-registry`](https://github.com/FDOx-squirrel/fdo-squirrel-registry) | Erntet von Zenodo, DCAT-Bundle + CRM-Bridge, SHACL-Gate, N4O-Export, Facetten- + SPARQL-Seite | **S0–S9 fertig.** S10 (Restarbeiten) läuft — kein Abnahmeschritt, sondern eine Aufgabenliste. |
| [`fdox-squirrel-n4o-collection`](https://github.com/FDOx-squirrel/fdox-squirrel-n4o-collection) | **Neu.** Collection-Repo für den NFDI4Objects Knowledge Graph: eine `metadata.yaml`, der Rest kommt von `n4o-kg-profile` | Live seit 2026-09-04, Build + Pages-Deploy grün. Kein `PRIMER.md`/`main.py` — folgt bewusst nicht dem Familienmuster, siehe unten. |
| [`fdo-squirrel-md-generator`](https://github.com/FDOx-squirrel/fdo-squirrel-md-generator) | Web-Generator für `MD.cff`+`CITATION.cff` | **v0.1 live**, GitHub Pages, im echten Browser verifiziert (Formular, Validierung, Round-Trip, ZIP-Validator, Karte, Wikidata/OSM-Lookup). Details unten. |
| [`fdo-squirrel-spec`](https://github.com/FDOx-squirrel/fdo-squirrel-spec) | ReSpec-HTML-Doku des Metadatenformats | **S1–S3 fertig.** Zwei echte Beispielinstanzen aus `fdo-squirrel-registry` statt kaputtem Demo-TTL, `fetch` für `fdo-squirrel` auf Tag `v0.3.1` gepinnt. Live: <https://fdox-squirrel.github.io/fdo-squirrel-spec/>. |
| [`fdo-architecture`](https://github.com/FDOx-squirrel/fdo-architecture) | Meta-Repo: `registry.yaml` + Mermaid-Übersicht + dieser Plan | **S0–S1 fertig.** `registry.yaml` mit diesem Patch aktualisiert (siehe unten). |
| [`fdo-3d-packager`](https://github.com/FDOx-squirrel/fdo-3d-packager) | Sketchfab/lokales 3D-Modell → `fdo:3DDataFDO`-Paket | **S0–S9 fertig.** Komplette Pipeline live, echter Rundlauf durch `fdo-squirrel` erfolgreich (S7). Kein Zenodo-DOI bisher. |
| [`fdo-git-packager`](https://github.com/FDOx-squirrel/fdo-git-packager) | Git-Repo (fester Commit) → `fdo:SoftwareFDO`-Paket | **S0–S1 fertig** (Skeleton, 6 Schritte, committet). S2–S6 offen — unverändert seit letztem Stand. |

**Verwandtes externes Werkzeug (andere Org, kein Teil der Familie, aber inzwischen produktiv im Einsatz):**

| Repo | Rolle | Status |
|---|---|---|
| [`n4o-rse/n4o-kg-profile`](https://github.com/n4o-rse/n4o-kg-profile) | Projektübergreifendes Werkzeug: `metadata.yaml` → per GitHub Action Metadaten-RDF, CIDOC-CRM-Alignment, browserbasierte SPARQL-Seite, damit eine Collection in den NFDI4Objects Knowledge Graph aufgenommen werden kann | **In Benutzung, nicht mehr nur ein Widerspruch im Plan.** Trägt `fdox-squirrel-n4o-collection`. Drei Bugs am 2026-09-04 gefunden und direkt gepatcht (Flo gehört auch diese Org), alle in echtem CI verifiziert. Selbst noch „Draft" (Crosswalk/Shapes nicht final gegen NCMDP/OCMDP abgeglichen). |

---

## Status & To-Dos je Repo

### `fdo-squirrel`
Kein `PRIMER.md`, daher aus der Commit-Historie abgelesen. Unverändert seit dem letzten Bericht — keine neuen Commits in diesem Zeitraum geprüft.
- **To-Do (weiterhin offen, aus dem Registry-Qualitätsbericht):** abgekürzte Klassen-IRIs außerhalb der bereits gepatchten Stellen, `xsd:integer` an weiteren Zeitgrenzen, `<DOI>_geom`/`<DOI>_temporal`-IRIs in fremdem Namensraum, ORCID statt Personen-URN, `dcat:bbox` statt `geo:hasBoundingBox` — Liste steht jetzt gebündelt in `fdo-squirrel-registry/PRIMER.md`, Schritt **S10**, Punkt 8.
- ✅ **Erledigt seit letztem Stand:** doppelte Prozentkodierung der `content/`-IRIs behoben (`fdo_rdf.py`, Commit „Stop double-percent-encoding content/ distribution IRIs", verifiziert in `fdo-squirrel-registry`).
- **Neuer Fund (2026-09-04, beim S8-Vorlauf der Registry):** `example_fdo/MD.cff` validiert nicht mehr gegen das aktuell geladene Schema (alte Feldnamen `abstract`/`publisher` statt `description`/`publishers`); dazu ein totes `MD.cff.schema.yaml` am Repo-Root, das `main.py` gar nicht mehr lädt. Reine Aufräumarbeit, blockiert nichts.
- **Empfehlung weiterhin offen:** ein eigenes `PRIMER.md` nach Familienmuster, sobald das nächste Mal substanziell daran gearbeitet wird.

### `fdo-squirrel-registry`
- ✅ **S0–S9 vollständig erledigt.** Zusätzlich zum letzten Bericht (S0–S7): S8 (Registry als eigenes FDO, `fdo:RegistryFDO`, GitHub Actions für Gate + Pages) und S9 (N4O-Andockung, siehe `fdox-squirrel-n4o-collection` unten) sind durch.
- **S9, korrigierter Umfang:** kein Eintrag in `n4o-collections.json` durch die Registry selbst — das übernimmt VZG von Hand. Die Registry endet bei einem SHACL-validierten, CRM-verankerten Bundle in einem eigenen Collection-Repo.
- **Läuft: S10 — Restarbeiten**, kein Abnahmeschritt, sondern eine Liste (Details dort): Zenodo-Publish des eigenen Release-Bundles + Eintrag in `sources.json` + Neu-Ernte (schließt den Selbsteintrag-Kreis), VZG-Kontakt sobald das steht, Labels-Pflege auf Dauer, Einreichungsweg für Dritte, Reparatur der vier fehlerhaften TTL im Bestand, `<DOI>_geom`/`<DOI>_temporal`-Entscheidung, der oben genannte Rückfluss nach `fdo-squirrel`.

### `fdox-squirrel-n4o-collection` (neu)
- Zweck: die eine Datei (`metadata.yaml`), die eine NFDI4Objects-KG-Collection aus `fdo-squirrel-registry`s Bundle macht. Folgt bewusst **nicht** dem `primer-repo`-Familienmuster — `n4o-kg-profile` kopiert `profile/`/`build/` bei jedem Lauf frisch rein und verlangt genau eine von Hand gepflegte Datei; ein eigenes `main.py`/`PRIMER.md` wäre hier Overhead, keine Vorsicht.
- ✅ Live: <https://fdox-squirrel.github.io/fdox-squirrel-n4o-collection/> und `/sparql.html` (SPARQL im Browser, gegen 6673 Tripel, 24 Klassen, 20 an CRM ausgerichtet).
- **To-Do:** `metadata.yaml`s `id`/`homepage` zeigen noch auf die GitHub-URL der Registry statt einer echten DOI — hängt am Zenodo-Publish in `fdo-squirrel-registry` S10.
- Zieht `dist/fdo-registry-n4o.ttl` bei jedem Build frisch von `raw.githubusercontent.com` — sobald die Registry sich selbst katalogisiert (S10), landet das ohne Änderung an diesem Repo automatisch im nächsten Build.

### `fdo-squirrel-spec`
- ✅ S1–S3 fertig (2026-09-04).
- Zwei echte, geharvestete Beispielinstanzen aus `fdo-squirrel-registry`
  (eine `SoftwareFDO`, eine `3DDataFDO`) ersetzen das gemischte, kaputte
  Demo-TTL aus `fdo-squirrel` selbst. Eine der beiden ist als harvestet
  ungültiges Turtle (fehlende `crm:`/`crmdig:`-Prefixe) — Reparaturlayer
  (`py/example_repair.py`) dafür aus `fdo-squirrel-registry/py/repair.py`
  kopiert, repariert nur im Speicher, nie auf der Platte.
- `fetch` für `fdo-squirrel` jetzt auf Tag `v0.3.1` gepinnt statt `main`
  (`fdo-squirrel` taggt inzwischen Releases).
- **Neuer Fund dabei:** `main` bei `fdo-squirrel` läuft `v0.3.1` bereits
  voraus (Crosswalk-`identifiers`-Handler, `geosparql:hasBoundingBox` statt
  `dcat:bbox`) — bewusst noch nicht übernommen, nächster Tag-Bump holt das
  nach. Außerdem ein Namespace-Mismatch: `crosswalk_md_cff_to_rdf.yaml`
  deklariert `fdo: https://w3id.org/fdo#`, real erzeugte Instanzen nutzen
  `https://w3id.org/fdo-squirrel/` — siehe `fdo-squirrel-spec`s `PRIMER.md`,
  noch nicht bei `fdo-squirrel` gemeldet.
- Live: <https://fdox-squirrel.github.io/fdo-squirrel-spec/>.
- **To-Do S4:** `owl-time`-artige Diagramme zur Package-Struktur (aus dem
  ursprünglichen S2 ausgelagert).

### `fdo-squirrel-md-generator`
- ✅ **v0.1 fertig und live**: <https://fdox-squirrel.github.io/fdo-squirrel-md-generator/> — von Flo bestätigt, zusätzlich per `web_fetch` gegengeprüft (Inhalt entspricht dem aktuellen Build).
- Formular für alle `MD.cff`-Felder mit Live-Validierung gegen `fdo-squirrel`s Schema (live gefetcht, Branch `master`, bei jedem Seitenaufruf); Round-Trip-Laden (Drag&Drop `MD.cff` oder ein ganzes Bundle-`.zip`); client-seitiger ZIP-Struktur-Validator (Layout, Schema, Datei-Rollen, Checksummen — explizit **kein** Ersatz für `fdo-squirrel`s RDF/SHACL-Prüfung); Karte fürs Spatial Extent inkl. Wikidata-(P625, P1332–P1335)/OpenStreetMap-(Nominatim)-Koordinaten-Lookup; CITATION.cff-Ableitung für `fdo:3DDataFDO`.
- Fünf Feedback-Runden nach dem ersten Deploy (Marker-Icon-Pfad, Start-Zoom, Rectangle-Drag statt Zwei-Klick, Anzeige/Export-Trennung bei Wikidata-/OSM-Kurzformen, Punkt/Bbox-exklusives Setzen) — alle im echten Browser gegengeprüft, siehe `PRIMER.md` A6–A10.
- **To-Do:** Chronontology-API für Temporal-Perioden (Ideensammlung, siehe `PRIMER.md` Teil D) — bewusst noch nicht umgesetzt, schwieriger als der Spatial-Fall (Namensmehrdeutigkeit). Tiefes Feld-Highlighting für Array-Elemente fehlt noch (v0.1-Vereinfachung).

### `fdo-architecture`
- ✅ S0–S1 fertig.
- ✅ **`registry.yaml` heute (2026-09-07) nachgezogen:** `fdo-squirrel-md-generator` von "Decisions done, no code yet" auf `done` (v0.1 live, Produces/Consumes korrigiert — jetzt inkl. der Kante zu `fdo-squirrel`s Schema-Fetch, vorher `consumes: []`); `fdo-3d-packager` von "Skeleton, sieben Schritte" auf `done` (komplette Pipeline, `pip`-Einbindung von `fdo-squirrel` als geklärt vermerkt); `fdo-squirrel`s Consumes-Notiz zu `fdo-squirrel-md-generator` von "Assumed link, not verified" auf den jetzt konkreteren (aber weiterhin ehrlichen) Stand aktualisiert. `python main.py --strict`: 9 Einträge, 0 Fehler, 0 Warnungen; `dist/architecture.mmd`/`docs/index.html` neu gebaut.
- ✅ Vorheriger Stand (04.09.2026): `org`-Feld-Korrektur, `fdo-3d-packager`/`fdo-git-packager` als Einträge ergänzt, `n4o-kg-profile`/`fdox-squirrel-n4o-collection` neu aufgenommen.
- Weiterhin vorgeschlagen, aber **nicht umgesetzt**: CI-Workflow (`--strict` bei jedem Push), `check-links`-Schritt gegen echte GitHub-URLs, Rücklinks in den READMEs der anderen Repos.

### `fdo-3d-packager`
- ✅ **S0–S9 vollständig erledigt** (Stand 2026-09-07). Komplette Pipeline live: `fetch` (Sketchfab/lokal) → `convert` (Blender) → `nexus` (`nxsbuild`/`nxscompress`) → `mdcff` (`MD.cff`+`CITATION.cff`, gegen Schema validiert) → `bundle` (`dist/<slug>.zip` in `fdo-squirrel`-Layout) → `build_fdo` (echter Rundlauf durch `fdo-squirrel`, `fdo-metadata.ttl` als Beleg — S7). Dazu S8 (Batch-Fetch, Multi-Slug) und S9 (CI-Smoke-Test gegen Fakes für Blender/`nxsbuild`/`nxscompress`).
- **Einbindung von `fdo-squirrel` geklärt** (PRIMER.md Teil D, resolved 2026-09-07): gepinnte `pip`-Abhängigkeit direkt von GitHub (`requirements.txt`, Commit `504b7af`) — dieselbe Lösung wie `fdo-squirrel-registry`s S8. Löst Abhängigkeit 4 unten für dieses Repo; `fdo-git-packager` hat die Frage noch offen.
- Kein Zenodo-DOI bisher (`CITATION.cff` trägt noch den `TODO`-Platzhalter-Kommentar).
- `distributions[]` bleibt bewusst leer im erzeugten `MD.cff` — `fdo-squirrel` berechnet das selbst aus dem tatsächlichen ZIP-Inhalt (Familienkonvention, auch in `fdo-squirrel-md-generator` so gehandhabt).

### `fdo-git-packager`
Unverändert seit letztem Stand.
- ✅ S0–S1 fertig (Skeleton, 6 Schritte, committet). S2–S6 offen.
- **Offen:** Einbindungsmechanismus für `fdo-squirrel` — `fdo-3d-packager` hat das jetzt gelöst (gepinnte `pip`-Abhängigkeit von GitHub, siehe oben), dieselbe Lösung dürfte hier passen, ist aber noch nicht übernommen.

### `n4o-kg-profile` (extern, Org `n4o-rse`)
- Muster: *Source-Repo* baut das Bundle → *Collection-Repo* pflegt nur `metadata.yaml`, referenziert `n4o-kg-profile` als versionierten Tag (`@v1`) in einer GitHub Action → `n4o-kg-profile` liefert `profile/` + `build/` (Metadaten-RDF, CIDOC-CRM-Alignment, SPARQL-Seite via GitHub Pages).
- ✅ **Nicht mehr nur ein ungeklärter Widerspruch — in Benutzung und live verifiziert.** `fdox-squirrel-n4o-collection` nutzt genau dieses Muster, echtes CI grün.
- **Drei Bugs am 2026-09-04 gefunden, alle direkt gepatcht** (Flo gehört auch `n4o-rse`, also gepatcht statt gemeldet): kein `v1`-Tag; `action.yml` checkte einen Org-Pfad aus, der 404 gibt; ein Selbst-Checkout via `github.action_ref` löste in der Praxis auf den *falschen* Tag auf (den der verschachtelten `actions/checkout`-Action, nicht die eigene Version) — behoben durch `github.action_path` statt eines zweiten Checkouts.
- **Weiterhin offen:** eigener Status „Draft" — Crosswalk/Shapes noch nicht mit dem verbindlichen NCMDP/OCMDP-Element-Katalog abgeglichen (`profile/CROSSWALK.md`, Abschnitt 6).

---

## Abhängigkeiten

1. **`n4o-kg-profile` ↔ `fdo-squirrel-registry` S9 — erledigt, nicht mehr offen.** Der frühere Widerspruch (ein Chat bereitete das Muster vor, das live stehende `PRIMER.md` kannte es nicht) ist aufgelöst: S9 nutzt jetzt genau dieses Muster, dokumentiert und verifiziert.
2. **`fdo-squirrel-registry` S10 → `fdox-squirrel-n4o-collection`**: der Zenodo-Publish des Registry-eigenen Release-Bundles ist der letzte Schritt, der beiden Repos noch fehlt — danach schließt sich der Selbsteintrag-Kreis automatisch (kein weiterer Code nötig, siehe S10 in der Registry).
3. **`fdo-architecture`/`registry.yaml`**: mit diesem Stand synchron, siehe oben. Nächste Aktualisierung fällig, sobald der Zenodo-Publish (Punkt 2) durch ist oder eines der Skeleton-Repos (`fdo-3d-packager`/`fdo-git-packager`) den nächsten Schritt macht.
4. **`fdo-3d-packager`/`fdo-git-packager` → `fdo-squirrel`-Einbindung**: für `fdo-3d-packager` **erledigt** (gepinnte `pip`-Abhängigkeit von GitHub, Commit `504b7af`, siehe oben) — `fdo-git-packager` hat dieselbe, jetzt erprobte Lösung noch vor sich, reine Übernahme, keine neue Design-Entscheidung nötig.
5. **`fdo-squirrel`s Rückfluss-Liste** (siehe `fdo-squirrel-registry/PRIMER.md` S10, Punkt 8) wartet weiterhin auf einen `fdo-squirrel`-Chat.
6. **RSE-Tauglichkeit der ganzen Familie** (CITATION.cff-ORCIDs, Zenodo-Releases pro Repo, einheitliche CONTRIBUTING.md) weiterhin angekündigt, noch nicht begonnen.

---

*Hinweis: Dieser Stand basiert auf `fdo-squirrel-md-generator`s und `fdo-3d-packager`s live stehenden `PRIMER.md`/Repo-Inhalten am 07.09.2026 (beide frisch geklont und geprüft, `fdo-3d-packager` zusätzlich per `requirements.txt`/`step_build_fdo.py` auf die tatsächliche `fdo-squirrel`-Einbindung hin gelesen), sowie auf dem vorherigen Stand vom 04.09.2026 für `fdo-squirrel-registry`, `fdox-squirrel-n4o-collection`, `fdo-squirrel-spec` und `n4o-kg-profile` (nicht in diesem Durchgang erneut geprüft). `fdo-squirrel` und `fdo-git-packager` wurden ebenfalls nicht erneut geprüft — deren Abschnitte sind unverändert übernommen und entsprechend markiert. Bei Widersprüchen zwischen diesem Dokument und einem `PRIMER.md` gilt das jeweilige `PRIMER.md` des Repos als genauer — dieses Dokument ist die Zusammenfassung, nicht die Quelle der Wahrheit.*
