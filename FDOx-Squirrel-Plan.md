# FDOx-Squirrel-Plan — Stand & offene To-Dos

Stand: 04.09.2026. Aktualisiert nach Abschluss von `fdo-squirrel-registry`s S8/S9 (Registry als eigenes FDO, N4O-Andockung), dem Hinzukommen eines neuen Repos, `fdox-squirrel-n4o-collection`, und `fdo-squirrel-spec`s S2/S3 (echte Beispielinstanzen, Tag-Pin). `registry.yaml` in diesem Repo ist mit diesem Stand synchron (`python main.py --strict` läuft fehlerfrei, `dist/architecture.mmd`/`docs/index.html` neu gebaut). Dieses Dokument liegt selbst in [`fdo-architecture/FDOx-Squirrel-Plan.md`](https://github.com/FDOx-squirrel/fdo-architecture/blob/main/FDOx-Squirrel-Plan.md) und soll bei jeder größeren Änderung an einem Familienmitglied nachgezogen werden.

## Familie im Überblick

Acht Repos unter `FDOx-squirrel` (sieben plus ein neu hinzugekommenes), dazu ein externes Werkzeug in einer anderen Org, das zwei der Familienmitglieder tatsächlich benutzen.

| Repo | Rolle | Status (S-Schritte laut `PRIMER.md`, falls vorhanden) |
|---|---|---|
| [`fdo-squirrel`](https://github.com/FDOx-squirrel/fdo-squirrel) | Referenzimplementierung: liest ein FDO-Paket (ZIP), schreibt `fdo-metadata.ttl` | Kein `PRIMER.md`. v0.1, publiziert (Zenodo DOI 10.5281/zenodo.18441772). Laufend gepflegt — siehe unten. |
| [`fdo-squirrel-registry`](https://github.com/FDOx-squirrel/fdo-squirrel-registry) | Erntet von Zenodo, DCAT-Bundle + CRM-Bridge, SHACL-Gate, N4O-Export, Facetten- + SPARQL-Seite | **S0–S9 fertig.** S10 (Restarbeiten) läuft — kein Abnahmeschritt, sondern eine Aufgabenliste. |
| [`fdox-squirrel-n4o-collection`](https://github.com/FDOx-squirrel/fdox-squirrel-n4o-collection) | **Neu.** Collection-Repo für den NFDI4Objects Knowledge Graph: eine `metadata.yaml`, der Rest kommt von `n4o-kg-profile` | Live seit 2026-09-04, Build + Pages-Deploy grün. Kein `PRIMER.md`/`main.py` — folgt bewusst nicht dem Familienmuster, siehe unten. |
| [`fdo-squirrel-md-generator`](https://github.com/FDOx-squirrel/fdo-squirrel-md-generator) | Web-Generator für `MD.cff`+`CITATION.cff` | Nur `PRIMER.md` im Repo. **S0 (Entscheidungen) fertig, S1–S7 (aller Code) offen.** Unverändert seit letztem Stand. |
| [`fdo-squirrel-spec`](https://github.com/FDOx-squirrel/fdo-squirrel-spec) | ReSpec-HTML-Doku des Metadatenformats | **S1–S3 fertig.** Zwei echte Beispielinstanzen aus `fdo-squirrel-registry` statt kaputtem Demo-TTL, `fetch` für `fdo-squirrel` auf Tag `v0.3.1` gepinnt. Live: <https://fdox-squirrel.github.io/fdo-squirrel-spec/>. |
| [`fdo-architecture`](https://github.com/FDOx-squirrel/fdo-architecture) | Meta-Repo: `registry.yaml` + Mermaid-Übersicht + dieser Plan | **S0–S1 fertig.** `registry.yaml` mit diesem Patch aktualisiert (siehe unten) — die drei zuvor offenen Punkte sind erledigt. |
| [`fdo-3d-packager`](https://github.com/FDOx-squirrel/fdo-3d-packager) | Sketchfab/lokales 3D-Modell → `fdo:3DDataFDO`-Paket | **S0–S1 fertig** (Skeleton, 7 Schritte, als Initial-Commit-ZIP geliefert). Committen und in der Praxis testen steht noch aus. S2–S7 offen. |
| [`fdo-git-packager`](https://github.com/FDOx-squirrel/fdo-git-packager) | Git-Repo (fester Commit) → `fdo:SoftwareFDO`-Paket | **S0–S1 fertig** (Skeleton, 6 Schritte, als Initial-Commit-ZIP geliefert). Committen und in der Praxis testen steht noch aus. S2–S6 offen. |

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
Unverändert seit letztem Stand.
- ✅ S0 fertig.
- **To-Do:** immer noch kein Code — S1–S7 offen. Von allen Repos das mit dem größten Rückstand zwischen Planung und Umsetzung.

### `fdo-architecture`
- ✅ S0–S1 fertig.
- ✅ **`registry.yaml`-To-Dos aus dem letzten Stand erledigt:** `org`-Feld für `fdo-squirrel`/`fdo-squirrel-registry` von `Research-Squirrel-Engineers` auf `FDOx-squirrel` korrigiert; `fdo-3d-packager` und `fdo-git-packager` als Einträge ergänzt; `status`-Text der Registry auf S0–S9 aktualisiert; `n4o-kg-profile` und `fdox-squirrel-n4o-collection` neu aufgenommen, inkl. der Kante zwischen beiden. `python main.py --strict`: 9 Einträge, 0 Fehler, 0 Warnungen; `dist/architecture.mmd`/`docs/index.html` neu gebaut.
- Weiterhin vorgeschlagen, aber **nicht umgesetzt**: CI-Workflow (`--strict` bei jedem Push), `check-links`-Schritt gegen echte GitHub-URLs, Rücklinks in den READMEs der anderen Repos.

### `fdo-3d-packager` / `fdo-git-packager`
Unverändert seit letztem Stand.
- ✅ S0–S1 fertig (Skeleton als Initial-Commit-ZIP geliefert), noch nicht committet oder in der Praxis getestet.
- **Offen, für beide identisch:** Einbindungsmechanismus für `fdo-squirrel` (pip aus GitHub, Git-Submodule oder externer Pfad) — `fdo-squirrel-registry`s S8 hat sich dafür entschieden (`pip`-Abhängigkeit von GitHub, auf Commit gepinnt); dieselbe Lösung dürfte auch hier passen, ist aber noch nicht übernommen.

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
4. **`fdo-3d-packager`/`fdo-git-packager` → `fdo-squirrel`-Einbindung**: gemeinsame offene Design-Frage, einmal klären genügt für beide — `fdo-squirrel-registry`s S8-Lösung (gepinnte `pip`-Abhängigkeit von GitHub) ist der naheliegende Kandidat.
5. **`fdo-squirrel`s Rückfluss-Liste** (siehe `fdo-squirrel-registry/PRIMER.md` S10, Punkt 8) wartet weiterhin auf einen `fdo-squirrel`-Chat.
6. **RSE-Tauglichkeit der ganzen Familie** (CITATION.cff-ORCIDs, Zenodo-Releases pro Repo, einheitliche CONTRIBUTING.md) weiterhin angekündigt, noch nicht begonnen.

---

*Hinweis: Dieser Stand basiert auf `fdo-squirrel-registry`s, `fdox-squirrel-n4o-collection`s und `fdo-squirrel-spec`s live stehenden `PRIMER.md`/Repo-Inhalten am 04.09.2026, plus einem frischen Klon von `n4o-rse/n4o-kg-profile` zur Verifikation der drei Bugfixes. `fdo-squirrel`, `fdo-squirrel-md-generator`, `fdo-3d-packager` und `fdo-git-packager` wurden in diesem Durchgang nicht erneut geprüft — deren Abschnitte sind unverändert aus dem Stand vom 03.09.2026 übernommen und entsprechend markiert. Bei Widersprüchen zwischen diesem Dokument und einem `PRIMER.md` gilt das jeweilige `PRIMER.md` des Repos als genauer — dieses Dokument ist die Zusammenfassung, nicht die Quelle der Wahrheit.*
