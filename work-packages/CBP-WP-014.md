# CBP-WP-014 — Deterministic Source Registry and Catalog

| Feld | Wert |
| --- | --- |
| ID | CBP-WP-014 |
| Titel | Deterministic Source Registry and Catalog |
| Typ | **implementation**, interactive authorization |
| Prompt Mode | **Full** (NDF v1.0.0) |
| Context Budget | **B2 – Standard** |
| Claude Code Model | **Claude Opus 4.8** (`claude-opus-4-8`) |
| Claude Code Effort | **ultracode** |
| Phase | Phase 1 – dritte technische Umsetzung |
| Ausgeführt am | 2026-07-22 |
| Ablauf | **interaktiv**, zwei Phasen |
| Status | `in-review` |
| Autoritätsklasse | A2 |

> **Drittes Work Package mit technischer Wirkung.** Es entsteht ausführbarer,
> getesteter Code — ein lokaler, synthetisch testbarer, **deaktivierter** und
> fail-closed Registry- und Catalog-Prototyp **ohne** operative Wirkung. Keine
> reale Quelle, kein Mapping, keine Aktivierung, kein Ingest, kein Index.

---

## Human-Autorisierung

| Feld | Wert |
| --- | --- |
| Entscheidung | **APPROVE WP-014 IMPLEMENTATION WITH NOTES** |
| Autorität | **A0** |
| Datum | 2026-07-22 |

**Kern der Notes (eng normalisiert):** Autorisierung ausschließlich für den
lokalen, synthetisch testbaren, deaktivierten, fail-closed Registry- und
Catalog-Prototyp. Nur strikte Validierung synthetischer Definitionen,
deterministische Source IDs, unveränderliche Records, append-only
Retirement-Events, ein deterministisch abgeleiteter minimierter Katalog, lokale
CLI, temporäre Registry außerhalb des Repos, Tests und Evidenz. **Nicht**
autorisiert: reale Quellen, Pfade/URLs, Source-Inhalt, Mapping, Source
Boundary, Aktivierung, Ingest, Quarantäne-Promotion, Collection/Index,
Retrieval/Embeddings, Netzwerk, Secret-Auflösung, RT-2, API/Web UI,
Docker/Deployment, Gate-Ausführung. Jede schreibende Operation setzt die
Synthetic-only-Grenze technisch durch. Jede Registrierung erzeugt nur
`REGISTERED_DISABLED`. Kein Status/Exitcode bedeutet `approved`, `mapped`,
`activated`, `ingestible`, `indexed`, `retrievable` oder produktionsbereit.
`activate` verweigert deterministisch und verändert keine Datei. Records,
Events, Kataloge, CLI-Ausgaben und Reports enthalten keine Pfade, URLs,
Inhalte, Mapping-Locators, Secrets oder personenbezogenen Daten.

## Vier Teilentscheidungen (A0)

| Teil | Entscheidung | Decision-ID |
| --- | --- | --- |
| A – Registry-Identität | Namespace + Source Key → deterministische Source ID | **D-042** |
| B – Registry-Speicher | unveränderliche JSON-Records + atomarer Katalog außerhalb Repo | **D-043** |
| C – Lifecycle | REGISTERED_DISABLED / RETIRED; append-only Retirement; keine Aktivierung | **D-044** |
| D – Katalogumfang | ausschließlich minimierte Metadaten | **D-045** |

Festgehalten in
[ADR-0011](../docs/decisions/ADR-0011-deterministische-source-registry.md)
(`accepted`, A1). **OD-05, OD-06, OD-37, OD-38 bleiben offen.**

## Ziel

Ein synthetisch testbarer, deaktivierter, fail-closed Registry- und
Catalog-Prototyp: strikte Definition-Validierung, deterministische Source IDs,
unveränderliche Records, append-only Retirement, deterministisch abgeleiteter
minimierter Katalog — **ohne** jede Aktivierung, Mapping oder Ingest.

## Scope

- Registry-Paket `core/core_brain/registry/` (6 Module).
- Beispiel-Policy, Beispiele, CLI-Kommandogruppe `source-registry`.
- Sechs neue Testmodule, erweiterter Netzwerk-Guard.
- Drei Runtime-Dokumente, ADR-0011, dieses Work-Package-Dokument.

## Out of Scope

Reale Quellen, Pfade/URLs, Source-Inhalt, Mapping, Source Boundary, Aktivierung,
Ingest, Quarantäne-Promotion, Collection/Index, Retrieval/Embeddings, Netzwerk,
Secret-Auflösung, RT-2, HTTP-API, Web UI, Docker, Deployment, Gate-Ausführung.

## Trust Boundary

Vor jeder Aktivierung und jedem Mapping. Die **Synthetic-only-Grenze** ist
technisch durchgesetzt: Flag `--synthetic-test-only` **und**
`synthetic_test_only = true` **und** `synthetic:`-Präfix **und**
`activation/content/network = false`; fehlt eines, blockiert die Operation ohne
Schreiben.

## Module

| Modul | Inhalt |
| --- | --- |
| `registry/models.py` | Enums, Policy-/Definition-/Record-/Event-/Catalog-Modelle |
| `registry/policy.py` | fail-closed Policy-Validierung (14 Felder) |
| `registry/storage.py` | unveränderlicher Speicher, atomar, idempotent, Konflikt |
| `registry/catalog.py` | deterministische Katalogableitung, Integritätsschutz |
| `registry/service.py` | Definition-Validierung, Identität, register/retire/inspect |
| `registry/__init__.py` | nebenwirkungsfreie Exporte |

## Identität

Source ID = `src-` + 24 Hex des SHA-256 aus Identitätsschema-Version,
`namespace`, `source_key`. Deterministisch; kein Display Name, kein Pfad, keine
URL, kein Inhalt. Abweichende Identität/Definition unter bestehender ID → Konflikt.

## Policy

14 Pflichtfelder, fail-closed. `allow_activation`/`content_access`/`network`/
`updates`/`deletion` = true blockieren; `allow_retirement` = false blockiert.
Leere Allowlists und unzulässige Maximalwerte blockieren.

## Definition

15 Felder, fail-closed. Slugs für `namespace`/`source_key`/`collection_key`/
`domain_key`/`owner_role`; Pfadseparator, `..`, URL-Indikator, Steuerzeichen
blockieren; `source_reference` mit `synthetic:`; `synthetic_test_only = true`;
`activation/content/network = false`.

## Record

17 Felder, unveränderlich, kanonisch, ohne Pfad/URL/Inhalt/Mapping-Locator.
Initialzustand `REGISTERED_DISABLED`, `registered_at` UTC-normalisiert,
injizierbar.

## Retirement

Append-only Event (9 Felder), `event_type = RETIRED`,
`reason_code = HUMAN_REQUESTED_SYNTHETIC_RETIREMENT`, deterministische Event-ID
(schließt `occurred_at` aus). Keine Löschung, keine Reaktivierung, idempotent.

## Storage

`records/<source-id>.json`, `events/<source-id>/<event-id>.json`,
`catalog/catalog.json`. Root außerhalb des Repos, kein Symlink, Pfade nur aus
IDs, atomare Schreibweise, kein Schreiben außerhalb des Roots.

## Catalog

Deterministisch nach `source_id` sortiert, aus Records und Events abgeleitet,
10 minimierte Felder je Eintrag (keine `source_reference`, kein Definition
Hash). Beschädigter Record blockiert den Gesamtkatalog; kein Teilkatalog.

## CLI

| Kommando | Wirkung | Exitcodes |
| --- | --- | --- |
| `source-registry validate-definition` | validiert, schreibt nichts | 0 / 8 |
| `source-registry register` | registriert deaktiviert; aktiviert nichts | 0 / 8 / 9 |
| `source-registry list` | minimierte Katalogeinträge | 0 |
| `source-registry inspect` | minimierte Record-Metadaten | 0 / 10 |
| `source-registry retire` | append-only Retirement; keine Löschung | 0 / 8 / 10 |
| `source-registry activate` | verweigert immer, ändert nichts | 11 |

Neue Exitcodes: **8** `SOURCE_REGISTRY_BLOCKED`, **9** `SOURCE_REGISTRY_CONFLICT`,
**10** `SOURCE_REGISTRY_NOT_FOUND`, **11** `SOURCE_REGISTRY_ACTIVATION_BLOCKED`
(kollisionsfrei mit 0–7, 64, 70). Exit 0 bei `register` bedeutet ausschließlich:
technisch registriert, `REGISTERED_DISABLED` — **nicht** approved/mapped/
activated/ingestible/indexed/retrievable.

## Zustände

`REGISTERED_DISABLED`, `RETIRED`. Kein Zustand erzeugt Mapping Approval,
Activation, Source Boundary, Source-Zugriff, Quarantäne-Promotion,
Collection-/Index-Eintrag, Context Pack oder externen Transfer.

## Tests

| Kennzahl | Wert (aus dem Lauf) |
| --- | --- |
| **Ausgeführte Tests** | **212** |
| Bestanden | **212** · Fehlgeschlagen 0 · Fehler 0 · Übersprungen 0 |
| Befehl | `py -3.13 -m unittest discover -s tests -v` |
| Testbasislinie CBP-WP-013 | **137**, weiterhin grün |
| Neue Testmodule | 6 (policy, definition, storage, catalog, service, cli) |
| Netzwerkzugriff | keiner — durch erweiterten Netzwerk-Guard belegt |
| Dateisystemwirkung | nur temporäre Testverzeichnisse |

**Ein Testdefekt im ersten Lauf gefunden und behoben** (im Test, nicht im Code)
— URL-Indikator-Test mit Schrägstrich; siehe Evidenz.

## Technische Evidenz

Vollständig in
[SOURCE_REGISTRY_EVIDENCE.md](../docs/runtime/SOURCE_REGISTRY_EVIDENCE.md).

| # | Kommando | Exitcode |
| --- | --- | ---: |
| P01–P03 | compileall · unittest · policy-check | 0 · 0 · 0 |
| S04–S10 | version · validate-definition · register · list · inspect · retire · list | 0 (alle) |
| S11 | `source-registry activate` | 11 |
| S12 | `run` | 4 |

Registry-Inventar: genau 1 Record + 1 Event + 1 Katalog; Cleanup vollständig
(`temp_remains=False`). Katalog minimiert (keine Ref, kein Pfad, keine URL).
Netzwerk-Guard über alle sechs neuen CLI-Pfade.

## Risiken

Geprüft: R-01, R-20, R-21, R-25, R-26, R-27, R-30, R-31, R-32, R-33, R-34.
**Kein Risiko geschlossen.** Präzisiert: die Registry-Identitäts- und
Katalogkonsistenz ist lokal getestet; Aktivierung bleibt technisch blockiert.
Getrennt geführt: **A – Weiterhin kritisch (kuratiert, 6):** R-21, R-25, R-27,
R-31, R-32, R-34 · **B – Zusätzliche offene Beobachtungsrisiken (5):** R-01,
R-20, R-26, R-30, R-33 · **C – Gesamte beobachtete Risikomenge (11).** C ist
keine kritische Liste. **R-33 bleibt `gemindert, nicht geschlossen`.**

## Stop-Bedingungen

Erfüllt: keine externe Abhängigkeit, kein Download, keine reale Quelle, kein
realer Pfad/URL, kein Source-Inhaltszugriff, kein Mapping, keine Aktivierung,
kein Netzwerkversuch, keine Speicherung im Repository, kein Symlink-Escape, kein
Schreiben außerhalb des Roots, kein Pfad-/URL-/Inhaltsleak, keine unzulässige
Record-Überschreibung, kein Teilkatalog bei Integritätsfehler, keine Collection/
Index, kein fehlgeschlagener Test, keine unerwartete Datei, keine Änderung
außerhalb der Erlaubnisliste, keine Gate-Ausführung, kein Versuch CBP-WP-015.

## Akzeptanzkriterien

Alle erfüllt: Implementierung autorisiert; A1/B1/C1/D1 gewählt; ADR-0011
erstellt; ausführbarer synthetischer Registry-Prototyp; Policy/Definition
strikt fail-closed; Source IDs deterministisch; Records unveränderlich und
idempotent; Retirement append-only; Katalog deterministisch und
rekonstruierbar; keine Pfade/URLs/Inhalte gespeichert oder ausgegeben;
Aktivierung immer verweigert; keine reale Quelle/Mapping; Testsuite grün; keine
Gate- oder Produktionsreife vorgetäuscht.

## Ergebnis

| Gegenstand | Wert |
| --- | --- |
| Neue Registry-Module | **6** |
| Neue Testmodule / Gesamttests | **6 / 212** |
| **Testergebnis** | **212 bestanden, 0 fehlgeschlagen** |
| Neue CLI-Kommandos | **6** |
| Neue Exitcodes | **4** (8, 9, 10, 11) |
| Externe Abhängigkeiten | **0** |
| **Durchgesetzte KB-Kontrollen** | **0** — alle bleiben `DOCUMENTED ONLY` |
| Geschlossene Risiken | **0** |
| Geschlossene Gates | **0** — alle bleiben `NOT EVALUATED` |
| Commit / Push | **nein / nein** |

## Rückmeldung an Nova

Der Source-Registry-MVP ist **lokal implementiert und getestet** — 212 Tests
bestanden, alle CLI-Smoke-Tests mit den erwarteten Exitcodes. **Keine reale
Quelle berührt, kein Mapping erzeugt, nichts aktiviert.**

**Vier Punkte, die ich hervorhebe:**

1. **Eine Registrierung ist keine Aktivierung.** Jeder Record ist
   `REGISTERED_DISABLED`; `activate` verweigert strukturell (Exit 11) und
   erzeugt kein Mapping und keine Source Boundary.

2. **Identität ist deterministisch und minimiert.** Die Source ID leitet sich
   ausschließlich aus Namespace und Source Key ab; Records und Katalog
   enthalten keinen Pfad, keine URL, keinen Inhalt und keinen Mapping-Locator.

3. **Der Katalog ist fail-closed rekonstruierbar.** Er wird deterministisch aus
   Records und Events abgeleitet; ein beschädigter Record blockiert den
   Gesamtkatalog — es entsteht kein Teilkatalog.

4. **Ein Testdefekt, kein Codedefekt.** Der URL-Indikator-Test verwendete eine
   URL mit Schrägstrich (zuerst als Pfadseparator blockiert); korrigiert und
   um einen Pfadseparator-Fall ergänzt. Die Testzahl 212 stammt aus dem grünen
   Lauf.

**Kein Risiko geschlossen. Kein Gate bewertet. Keine Capability vollständig
`implemented`.**

**Nächstes vorgeschlagenes Work Package: CBP-WP-015 — Deterministic Source
Mapping Draft Validator** (implementation, interactive authorization, Full, B2 –
Standard), Status **`proposed`, implementation not yet authorized**. **Nicht
ausführen** ohne ausdrückliche Freigabe.
