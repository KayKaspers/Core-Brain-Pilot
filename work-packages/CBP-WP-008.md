# CBP-WP-008 — Phase 1 Foundation Implementation Plan

| Feld | Wert |
| --- | --- |
| ID | CBP-WP-008 |
| Titel | Phase 1 Foundation Implementation Plan |
| Typ | `docs-only` |
| Prompt Mode | **Full** (NDF v1.0.0) |
| Context Budget | **B2 – Standard** (Core Brain Pilot) |
| Phase | Phase 1 – Planung |
| Ausgeführt am | 2026-07-21 |
| Status | `in-review` |
| Autoritätsklasse | A2 |

---

## Ziel

Die Phase-1-Backlogpunkte **P1 bis P5** in einen ausführbaren,
nachweisorientierten Implementierungsplan überführen: Abhängigkeiten und
Reihenfolge festlegen, kleine Work Packages schneiden, technische Nachweise
benennen, Abbruch- und Rücksetzbedingungen definieren und Implementierungs- von
Reviewgrenzen trennen.

**Keine technische Umsetzung.** Die G0-Freigabe autorisiert Planung.

## Scope

- Drei veraltete Gate-Angaben korrigieren
- Fünf Foundation-Streams F1–F5 definieren
- Repository- und Workspace-Schnitt entscheidungsreif vorbereiten
- Mappingschema für PS-02, PS-03, PS-04 definieren
- Zwölf Kontrollbereiche der technischen Sicherheitsgrundlage planen
- Fail-closed Ingest-Quarantäne planen
- Deterministisches Registry-Modell planen
- Sechs Folge-Work-Packages schneiden
- Nachweis- und Abnahmeplan erstellen
- Abbruch- und Rücksetzbedingungen definieren
- Status und Register nachführen

## Out of Scope

- Jede technische Implementierung
- Reale Source Mappings, private Pfade, private Repository-URLs, Secrets
- Repository-Reorganisation, Dateiverschiebung
- OD-26, OD-05, OD-06 eigenmächtig schließen
- Spätere Work Packages aktivieren
- Suchprovider-Auswahl, Scannerinstallation, Retrieval, Benchmarklauf
- DRC ausführen
- Commit, Push, Branch, Remote-Änderung, Issue, Release

## Inputs

NDF v1.0.0 · Repository-Stand auf `main` (Commit `5e9c687`) ·
`PHASE_1_BACKLOG.md` · `G0_SCOPE_LOCK_REVIEW.md` · `G0_EVIDENCE_MATRIX.md` ·
`G0_SCOPE_LOCK_CRITERIA.md` · `PILOT_SOURCE_CONTRACT.md` ·
`SOURCE_SLOT_MODEL.md` · `ADR-0006` · `SYSTEM_ARCHITECTURE.md` ·
`COMPONENT_MODEL.md` · `DEPLOYMENT_PROFILES.md` ·
`REPOSITORY_LAYOUT_OPTIONS.md` · `PERMISSION_MODEL.md` ·
`SECRET_INCIDENT_RESPONSE.md` · `DATA_CLASSIFICATION.md` ·
`DEPLOYMENT_READINESS_CHECK.md` · `BENCHMARK_PLAN.md` ·
`EVALUATION_RUBRIC.md` · `PROJECT_MANIFEST.md` · `DECISION_REGISTER.md` ·
`RISK_REGISTER.md` · `WORK_PACKAGE_QUEUE.md` · `CAPABILITY_MATRIX.md` ·
`COMPLIANCE_CHECK.md` · `PROJECT_BRAIN.md` · `CBP-WP-007.md` · `README.md` ·
`CLAUDE.md`

## Aufgaben

| # | Aufgabe | Ergebnis |
| --- | --- | --- |
| 1 | Veraltete Statusangaben korrigieren | CLAUDE.md, DISCOVERY_QUESTIONS.md, G0_EVIDENCE_MATRIX.md |
| 2 | Phase-1-Foundation-Plan | F1–F5 mit je 14 Feldern |
| 3 | Repository- und Workspace-Plan | Drei Bereiche, Modelle W-1/W-2/W-3, Empfehlung `PROPOSED` |
| 4 | Pilot-Source-Mapping-Plan | 19 Felder, 14 Regeln, 7 spätere Nachweise |
| 5 | Technische Sicherheitsgrundlage | KB-01 bis KB-12, Durchsetzungsreihenfolge |
| 6 | Quarantäne- und Scanning-Plan | 12 Schritte, 10 Status, 12 Negativtests |
| 7 | Source-Registry- und Katalogplan | 24 Felder, ID-/Hash-/Tombstoneregeln, Rebuild-Vertrag |
| 8 | Work-Package-Schnitt | CBP-WP-009 bis CBP-WP-014, alle `proposed` |
| 9 | Evidenz- und Abnahmeplan | 8 Nachweisarten, 6 Statusstufen |
| 10 | Abbruch- und Rücksetzbedingungen | SB-01 bis SB-12 |
| 11 | Status und Register | 14 Dokumente nachgeführt |

## Geplante Folge-Work-Packages

Vollständig in
[PHASE_1_WORK_PACKAGE_MAP.md](../docs/roadmap/PHASE_1_WORK_PACKAGE_MAP.md).

| ID | Titel | Typ | Status |
| --- | --- | --- | --- |
| CBP-WP-009 | Repository Boundary Decision | `docs-only`, interaktiv | **`proposed`** |
| CBP-WP-010 | Pilot Source Mapping Specification | `docs-only` | **`proposed`** |
| CBP-WP-011 | Technical Security Foundation Specification | `docs-only` | **`proposed`** |
| CBP-WP-012 | Foundation Runtime Skeleton | spätere Implementierung | **`proposed`** |
| CBP-WP-013 | Ingest Quarantine Minimum Viable Pipeline | spätere Implementierung | **`proposed`** |
| CBP-WP-014 | Deterministic Source Registry and Catalog | spätere Implementierung | **`proposed`** |

```text
CBP-WP-009 ─┬─► CBP-WP-010 ─────────────┐
            │                           ├─► CBP-WP-013 ─► CBP-WP-014
            └─► CBP-WP-011 ─► CBP-WP-012┘
```

**Keines ist freigegeben. Keines steht auf `active`.**

## Prüfungen

31 Prüfungen. Schwerpunkte: sauberer Arbeitsbaum vor Beginn · ausschließlich
Markdown · drei Gate-Angaben korrigiert · G0 bleibt PASSED WITH NOTES ·
Phase 1 bleibt AUTHORIZED FOR PLANNING · ADR-0006 bleibt `accepted` · DRC
bleibt `NOT EVALUATED` · Benchmark bleibt nicht ausgeführt · alle fünf Streams
mit Abhängigkeiten, Nachweisen, Abbruch- und Rücksetzbedingungen · drei
Bereiche getrennt · keine Reorganisation · keine realen Mappings ·
Mappingdefaults `disabled` und `read-only` · zwölf Kontrollbereiche ·
Promptregeln nicht als technische Kontrolle · Quarantäne fail-closed · kein Weg
von `received` direkt nach indexiert · Secret-Fund blockiert · Registry und
Suchindex getrennt · Tombstone und Derived Cleanup geplant · CBP-WP-009…014 nur
`proposed` · keine Capability `implemented` · **R-33 nicht geschlossen** · genau
ein nächstes Work Package vorgeschlagen · kein Commit, kein Push, `origin`
unverändert.

## Akzeptanzkriterien

Veraltete Gate-Angaben korrigiert · P1 bis P5 vollständig geplant ·
Repository- und Workspace-Schnitt entscheidungsreif · Source-Mapping-Plan
vorhanden · technische Sicherheitsgrundlage planbar · Quarantäne und Scanning
planbar · Registry und Katalog planbar · kleine Folge-Work-Packages definiert ·
Nachweise und Stop-Bedingungen vollständig · **keine Implementierung begonnen**
· Phase 1 weiterhin nur zur Planung autorisiert · alle Prüfungen bestanden.

---

## Ergebnis

| Gegenstand | Wert |
| --- | --- |
| Neue Dokumente | **10** (9 Roadmap-Dokumente + dieses) |
| Geänderte Dokumente | **14** |
| Streams | **F1 bis F5** |
| Kontrollbereiche | **KB-01 bis KB-12** |
| Quarantäneschritte / Status | **12 / 10** |
| Registry-Felder | **24** |
| Mapping-Felder | **19** |
| Folge-Work-Packages | **6**, alle `proposed` |
| Nachweisstufen | **6** |
| Stop-Bedingungen | **12** |
| Neue offene Entscheidung | **OD-34** (Secret-Store-Technologie) |
| Neue fehlende Information | **OI-11** |
| **Geschlossene Risiken** | **0** |
| **Capabilities `implemented`** | **0 von 29**, unverändert |
| **Commit / Push** | **nein / nein** |

## Rückmeldung an Nova

**Phase 1 ist vollständig geplant und weiterhin vollständig unautorisiert.**
P1 bis P5 liegen als Streams F1 bis F5 vor, geschnitten in sechs
Folge-Work-Packages. Es wurde nichts gebaut, nichts installiert, nichts
angebunden, nichts verschoben und nichts gemessen.

**Vier Punkte, die ich hervorhebe:**

1. **Der vierte Zählfehler des Projekts ist gefunden.** Die Summenzeile des
   Decision Registers führte 22 A0-Entscheidungen und 8 offene P0-Punkte; die
   Auszählung ergibt **24** und **6**. Der Fehler entstand in CBP-WP-007 —
   **nachdem** die Zählregel eingeführt worden war — und wurde erst jetzt
   sichtbar. **R-33 bleibt offen**: die Regel wirkt nachlaufend, nicht
   vorbeugend.

2. **Zwei Dokumente hätten dieselben Bezeichner verschieden belegt.**
   `REPOSITORY_LAYOUT_OPTIONS.md` verwendet A/B/C für Verzeichnislayouts. Der
   Arbeitsbereichsschnitt ist eine **unabhängige** Frage; seine Modelle heißen
   deshalb **W-1/W-2/W-3**. **OD-26 braucht beide Antworten** — das war vorher
   nicht sichtbar.

3. **OD-34 ist neu und war eine echte Lücke.** Kontrollbereich KB-08 und das
   Mappingschema setzen einen Secret Store voraus, auf den nur **verwiesen**
   wird. Weder Technologie noch Verweisformat waren irgendwo als offene
   Entscheidung geführt. Blockiert CBP-WP-012.

4. **Kein Risiko wurde geschlossen oder gemindert.** Der Evidenzplan ordnet
   jedem Risiko einen Schließungsweg und eine erforderliche Nachweisstufe zu —
   beschritten ist keiner. **Alle Artefakte des Projekts stehen auf Stufe 1
   `dokumentiert`.** Stufe 1 schließt definitionsgemäß kein Risiko.

**Ein Hinweis zur Reihenfolge:** Der F3-Strang (CBP-WP-011 → CBP-WP-012) ist
der breiteste Enabler. CBP-WP-013 und CBP-WP-014 sind ohne ihn nicht
durchsetzbar — sie wären Konventionen statt Kontrollen. Gleichzeitig geht
**CBP-WP-009 allen voraus**, weil ohne Bereichsgrenze jedes Mapping ortlos ist.

**Nächstes vorgeschlagenes Work Package: CBP-WP-009 — Repository Boundary
Decision** (`docs-only`, Full, B1 – Lean, interaktiv). **Nicht ausführen** ohne
ausdrückliche Freigabe.
