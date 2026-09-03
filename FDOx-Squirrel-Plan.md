# Kurzbericht: FDOx-Squirrel-Familie — Stand & offene To-Dos

Stand: 03.09.2026, basierend auf den heutigen Chats in diesem Projekt sowie einem Live-Check der GitHub-Org `FDOx-squirrel` und des Repos `n4o-rse/n4o-kg-profile`.

## Familie im Überblick

Alle sieben Repos liegen jetzt unter **[github.com/FDOx-squirrel](https://github.com/FDOx-squirrel)** — die Migration von `Research-Squirrel-Engineers` ist abgeschlossen (alte URLs leiten per 301 auf die neue Org um). Live geprüft: welche Repos schon Inhalt haben und welche noch leer sind (angelegt, aber kein Commit).

| Repo | Rolle | Live-Status |
|---|---|---|
| [`fdo-squirrel`](https://github.com/FDOx-squirrel/fdo-squirrel) | Generator: baut `fdo-metadata.ttl` aus einem FDO-Paket | ✅ hat Inhalt (umgezogen) |
| [`fdo-squirrel-registry`](https://github.com/FDOx-squirrel/fdo-squirrel-registry) | Erntet von Zenodo, baut DCAT-Bundle + CRM-Bridge, SHACL-Gate, N4O-Export, SPARQL/Facetten-Seite | ✅ hat Inhalt (umgezogen) |
| [`fdo-squirrel-md-generator`](https://github.com/FDOx-squirrel/fdo-squirrel-md-generator) | Web-Generator für `MD.cff` (Analogie zu CFF-Initializer) | ✅ hat Inhalt |
| [`fdo-squirrel-spec`](https://github.com/FDOx-squirrel/fdo-squirrel-spec) | ReSpec-HTML-Doku des Metadatenformats | ⬜ leer — ZIP liegt bereit, noch nicht gepusht |
| [`fdo-architecture`](https://github.com/FDOx-squirrel/fdo-architecture) | Meta-Repo: `registry.yaml` + Mermaid-Übersicht der ganzen Familie | ⬜ leer — Patch liegt bereit, noch nicht angewendet |
| [`fdo-3d-packager`](https://github.com/FDOx-squirrel/fdo-3d-packager) | Sketchfab/lokales 3D-Modell → fertiges `fdo:3DDataFDO`-Paket | ⬜ leer — S1-ZIP liegt bereit, noch nicht gepusht |
| [`fdo-git-packager`](https://github.com/FDOx-squirrel/fdo-git-packager) | Git-Repo (fester Commit) → fertiges `fdo:SoftwareFDO`-Paket | ⬜ leer — S1-ZIP liegt bereit, noch nicht gepusht |

**Verwandtes externes Repo (andere Org, kein Teil der FDOx-squirrel-Familie, aber Abnehmer/Partner):**

| Repo | Rolle | Live-Status |
|---|---|---|
| [`n4o-rse/n4o-kg-profile`](https://github.com/n4o-rse/n4o-kg-profile) | Projektübergreifendes Werkzeug: aus `metadata.yaml` per GitHub Action Metadaten-RDF, CIDOC-CRM-Anbindung und eine browserbasierte SPARQL-Seite erzeugen, damit eine Collection in den **NFDI4Objects Knowledge Graph** aufgenommen werden kann | ✅ hat jetzt echten Inhalt (`profile/`, `build/`, `example/` mit Beispieldaten, `action.yml`) — war beim letzten Check noch leer |

---

## Status & To-Dos je Repo

### `fdo-squirrel`
- ✅ Patch #1 (S1–S4) angewendet: CRM-Klassen-IRIs korrigiert, `xsd:gYear` statt Integer, GeoSPARQL-BBox als typisiertes Envelope-Literal, fehlende `rdfs:label` ergänzt.
- ✅ S5 geklärt: **kein Bug** — die drei älteren Pakete (Jan.) tragen die ORCID korrekt, die vier neueren (Feb.) haben ein leeres `orcid:`-Feld in `CITATION.cff` (Datenlücke, nicht Code).
- 🔶 **Feature "fertiges Bundle-ZIP"** (Original-ZIP + generierte Dateien inkl. Distribution-Modellierung + hochauflösendem Mermaid-JPG) ist implementiert und verifiziert, Auslieferung als Patch #2 stand kurz bevor.
  - **To-Do:** Patch #2 abholen/anwenden, sobald geliefert.
- **To-Do (optional, S6):** In den Original-`CITATION.cff` der vier neueren Zenodo-Pakete nachsehen, ob ORCID wirklich fehlt oder nur nicht befüllt wurde.

### `fdo-squirrel-registry`
- ✅ S1–S6 erledigt: Skeleton, Zenodo-Harvest, CRM-Bridge, DCAT-Bundle+Katalog, SHACL-Gate+Qualitätsbericht+N4O-Export, `.gitattributes`/Encoding-Fix.
- 🔶 S7 (SPARQL-/Facetten-Seite im Browser, `queries.yaml` als einzige Quelle, Pyodide/rdflib) ist konzipiert und angelaufen — genauer Fertigstellungsgrad war in dieser Recherche nicht abschließend zu klären.
- **To-Do:** Doppelte Prozentkodierung der `content/`-IRIs im eigenen Bundle-Build fixen — Ursache liegt in `content_iri()` der Registry selbst (nicht im Generator, siehe unten).
- **S9 (N4O-Andockung) hängt jetzt an [`n4o-kg-profile`](https://github.com/n4o-rse/n4o-kg-profile):** Das Repo ist nicht mehr leer — `profile/`, `build/`, `action.yml` und ein `example/` mit echten Beispieldaten (`metadata.yaml`, `queries.yaml`, `rdf/`) liegen vor. Laut dessen README ist das Muster: Collection-Repo pflegt nur `metadata.yaml`, eine GitHub Action (referenziert `n4o-kg-profile` als `@v1`-Tag) erzeugt daraus RDF, CIDOC-CRM-Anbindung und eine SPARQL-Seite; die VZG bindet das Ergebnis danach manuell in den N4O-KG ein. **To-Do:** prüfen, ob `fdo-squirrel-registry`s eigener S8/S9-Weg (`dist/fdo-registry-n4o.ttl`, `n4o-collections.json`) jetzt durch dieses Muster ersetzt oder nur ergänzt wird — in PRIMER.md Teil D als offen vermerkt, jetzt mit echtem Repo-Inhalt neu zu bewerten.
- ⚠️ Ein Chat zum Erstellen einer Arbeitsanweisung für "S6b" brach unerklärt ab — falls das nochmal passiert, eher in kleineren Einzelschritten arbeiten.

### `fdo-squirrel-spec`
- ✅ Fertig gebaut und als komplettes Repo-ZIP geliefert (kein Patch, da Zielrepo leer).
- **To-Do:** Repo ist live bestätigt leer (angelegt, kein Commit) — ZIP entpacken, committen, pushen.

### `fdo-squirrel-md-generator`
- ✅ Planung (PRIMER.md) fertig, Mapping-Entscheidungen bestätigt (automatische FDO-Ableitung nur für `fdo:3DDataFDO`, Autoren immer als CFF-Entity, unbekannte Identifier-Schemata → `type: other`).
- **To-Do:** S1 — eigentliches Repo-Skelett/erster Code steht noch aus, bisher nur Dokumentation.

### `fdo-architecture`
- ✅ S1 geliefert: `registry.yaml` (5 Familienmitglieder) + `main.py` (`validate`/`render`) + generiertes Mermaid-Diagramm/`docs/index.html`.
- **To-Do:** Repo ist live bestätigt leer — Patch anwenden und pushen (stand bei Gesprächsende noch aus).
- Zwei Stellen bewusst als unsicher markiert: Kante `md-generator → fdo-squirrel` (nur aus dem Repo-Namen erschlossen) sowie `org`/`url`-Felder für `fdo-squirrel`/`-registry` (zeigten zum Zeitpunkt der Erstellung noch auf die alte Org — jetzt mit der abgeschlossenen Migration von Hand nachzuziehen).
- Vorgeschlagen, aber noch **nicht umgesetzt**: CI-Workflow (`--strict` bei jedem Push), `check-links`-Schritt gegen echte GitHub-URLs, Cross-Repo-Backlog im Architektur-Repo, Rücklinks in den READMEs der anderen Repos. Sobald es gepusht ist, wäre `n4o-kg-profile` als achter Eintrag (bzw. als verwandtes externes Repo) ein Kandidat für `registry.yaml`.

### `fdo-3d-packager`
- Zweck: Sketchfab-Modell (`--sketchfab URL`) oder lokale Datei (`--local PATH`) → fertiges FDO-Paket im von `fdo-squirrel` erwarteten Layout (`MD.cff`+`CITATION.cff`, `fdo_type: fdo:3DDataFDO`). Baut auf einem Sketchfab-Prototyp auf (Blender-Konvertierung, Nexus-Multiresolution, 3DHOP-Miniviewer).
- ✅ S0 (Name/Org/Format-Entscheidungen) und S1 (lauffähiges Skeleton, 7 Schritte `fetch→convert→nexus→mdcff→bundle→build_fdo`) fertig geliefert als konsolidiertes Initial-Commit-ZIP.
- ✅ Entschieden: Viewer wandert mit ins FDO-ZIP; `distributions[]` wird **nicht** vom Packager vorbefüllt, sondern von `fdo-squirrel` selbst klassifiziert.
- **To-Do:** Repo ist live bestätigt leer — ZIP als Initial Commit pushen; S2–S7 (eigentliche Implementierung) stehen noch aus.
- **Offen:** Wie wird `fdo-squirrel` in S7 technisch eingebunden (pip aus GitHub, Git-Submodule, oder externer Pfad)? Diese Frage ist identisch mit der von `fdo-git-packager` — wird nur einmal entschieden, für beide Repos übernommen.

### `fdo-git-packager`
- Zweck: Git-Repo + fester Commit-SHA → fertiges FDO-Paket (`fdo_type: fdo:SoftwareFDO`). Schwester-Repo zu `fdo-3d-packager`, bewusst separat gehalten (unterschiedliche `fetch`/`convert`-Logik, Familienregel „Kopieren statt Referenzieren").
- ✅ S0-Entscheidungen: kompletter Working Tree (mit Exclude-Liste `.git/`, `node_modules/`, `build/` etc.), fester Commit-SHA als Pflichtangabe (kein Branch-HEAD-Fallback), Titel/Autor/Lizenz aus GitHub-API-Vorschlag + CLI-Override.
- ⚠️ Wichtiger Befund dabei: Der Working Tree muss **flach auf ZIP-Root** liegen, nicht unter einem Unterordner wie `repo/` — sonst greifen die `path_prefix`-Klassifikationsregeln von `fdo-squirrel` (z. B. `tests/`) nicht mehr.
- ✅ S1 (Skeleton, 6 Schritte `fetch→inspect→mdcff→bundle→build_fdo`) fertig geliefert als Initial-Commit-ZIP.
- **To-Do:** Repo ist live bestätigt leer — ZIP pushen; S2–S6 stehen noch aus.
- **Offen:** Gleiche `fdo-squirrel`-Einbindungsfrage wie oben; außerdem unbestätigt, ob eine im Ziel-Repo vorhandene `CITATION.cff` wirklich immer Vorrang vor einer synthetisierten haben soll (bisher nur Vorschlag, kein Beschluss per Rückfrage).

### `n4o-kg-profile` (extern, Org `n4o-rse`)
- Kein Teil der FDOx-squirrel-Familie im engeren Sinn, aber direkter Abnehmer/Partner: Standardwerkzeug, um eine beliebige Collection (nicht nur FDOx) in den NFDI4Objects Knowledge Graph aufzunehmen.
- Muster laut README: *Source-Repo* (baut das Bundle) → *Collection-Repo* (pflegt nur `metadata.yaml` + `rdf/<name>-bundle.ttl`, referenziert `n4o-kg-profile` als versionierten Tag `@v1` in einer GitHub Action) → `n4o-kg-profile` selbst (liefert `profile/` + `build/`: Metadaten-RDF, CIDOC-CRM-Crosswalk, SPARQL-Seite via GitHub Pages).
- ✅ Jetzt mit echtem Inhalt: `profile/profile.ttl`, `profile/shapes.ttl`, `profile/context.jsonld`, `profile/CROSSWALK.md`, `build/make_metadata.py`, `build/build_sparql.py`, `action.yml`, plus ein vollständiges `example/` (`metadata.yaml`, `queries.yaml`, generierte `dist/`/`docs/`).
- **Relevanz für diese Familie:** `fdo-squirrel-registry`s S8/S9 (siehe oben) soll darüber laufen; die generelle Bundle→Zenodo→SHACL→N4O-Kette könnte künftig auch für `fdo-3d-packager`/`fdo-git-packager`-Pakete interessant werden, sobald die manuell aus `fdo-squirrel` erzeugten Bundles veröffentlicht werden sollen.
- **To-Do:** `example/` als Referenz durchgehen und klären, ob `fdo-squirrel-registry` künftig selbst ein Collection-Repo im Sinne dieses Musters wird (eigenes `metadata.yaml` + Action statt der bisherigen S8/S9-Eigenlösung), oder ob beide Wege parallel bestehen bleiben.

---

## Abhängigkeiten

1. **`fdo-squirrel` Patch #2 → `fdo-squirrel-registry`**: Die Registry harvestet die von `fdo-squirrel` erzeugten TTLs/Bundles; das neue Bundle-ZIP-Feature sollte vor dem nächsten Harvest-Lauf angewendet sein.
2. **Prozentkodierungs-Fix gehört in die Registry**, nicht in `fdo-squirrel` — blockiert aktuell nichts, sollte aber vor dem nächsten Bundle-Rebuild in der Registry nachgezogen werden.
3. **Org-Migration ist abgeschlossen** — alle sieben Familien-Repos liegen jetzt unter `FDOx-squirrel`. Dokumente/Configs, die noch die alte Org (`Research-Squirrel-Engineers`) referenzieren (z. B. `registry.yaml` in `fdo-architecture`, sobald gepusht), müssen von Hand nachgezogen werden — technisch unkritisch, da GitHub die alten URLs per 301 weiterleitet, aber für Konsistenz zu erledigen.
4. **`n4o-kg-profile` ist nicht mehr leer** — `fdo-squirrel-registry`s S8/S9 (N4O-Andockung) war bisher als Eigenlösung geplant (`dist/fdo-registry-n4o.ttl`, `n4o-collections.json`), jetzt mit echtem Repo-Inhalt neu zu bewerten: ersetzt das Collection-Repo-Muster von `n4o-kg-profile` diesen Weg, ergänzt es ihn, oder bleiben beide parallel bestehen?
5. **`fdo-3d-packager`/`fdo-git-packager` → `fdo-squirrel`-Einbindung**: Beide neuen Packager brauchen für ihren letzten Schritt (Rundlauf-Test) eine Antwort auf dieselbe offene Frage, wie eine lokale `fdo-squirrel`-Instanz technisch eingebunden wird (pip/Submodule/externer Pfad) — einmal klären, gilt für beide.
6. **RSE-Tauglichkeit der ganzen Familie** (CITATION.cff-ORCIDs, Zenodo-Releases pro Repo, einheitliche CONTRIBUTING.md) ist als nächster großer Block angekündigt, aber noch nicht begonnen — sinnvollerweise erst nach den offenen Patches oben.

---

*Hinweis: Dieser Bericht fasst den bisherigen Gesprächsverlauf in diesem Projekt zusammen und wurde zuletzt gegen den Live-Zustand der GitHub-Org `FDOx-squirrel` sowie `n4o-rse/n4o-kg-profile` geprüft (03.09.2026). Bei Unsicherheiten zu einzelnen Schritten (z. B. genauer S7-Stand der Registry) lohnt ein Blick ins jeweilige `PRIMER.md` des Repos. Dieses Dokument kann als gemeinsamer Ausgangspunkt für neue Chats zu einzelnen Repos dienen.*
