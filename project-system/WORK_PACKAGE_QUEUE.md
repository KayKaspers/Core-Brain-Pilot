# Work Package Queue – Core Brain Pilot

| Feld | Wert |
| --- | --- |
| Phase | **Phase 0 COMPLETE** · Phase 1 AUTHORIZED FOR PLANNING |
| Aktuelles Work Package | **keines aktiv** — zuletzt abgeschlossen **CBP-WP-018** (`committed`, `5ee2e83`) |
| Gate G0 | **PASSED WITH NOTES** — 2026-07-21 |
| Überarbeitet in | **CBP-WP-016** |
| Autoritätsklasse | A2 |
| Stand | 2026-07-29 |

Spalten nach `WORK_PACKAGE_QUEUE_TEMPLATE.md` (NDF v1.0.0).

## Statuswerte

| Status | Bedeutung |
| --- | --- |
| `proposed` | Vorgeschlagen, **nicht freigegeben** |
| `released` | Vom Human Maintainer freigegeben |
| `active` | In Ausführung |
| `in-review` | Ausgeführt, wartet auf Review |
| `complete` | Review bestanden, GO erteilt |
| `committed` | Ergebnis committet, **durch Git bestätigt** |
| `blocked` | Angehalten, Blocker gemeldet |

## Queue

| ID | Title | Priority | Status | Prompt |
| --- | --- | --- | --- | --- |
| CBP-WP-001 | Repository Bootstrap und dokumentarisches Projektfundament | P0 | **`committed`** | [work-packages/CBP-WP-001.md](../work-packages/CBP-WP-001.md) |
| CBP-WP-002 | Source Reconciliation und G0 Scope-Lock-Definition | P0 | **`committed`** | [work-packages/CBP-WP-002.md](../work-packages/CBP-WP-002.md) |
| CBP-WP-003 | Human Discovery Intake and G0 Evidence Capture | P0 | **`committed`** | [work-packages/CBP-WP-003.md](../work-packages/CBP-WP-003.md) |
| CBP-WP-004 | Generic Architecture and Deployment Profiles | P0 | **`committed`** | [work-packages/CBP-WP-004.md](../work-packages/CBP-WP-004.md) |
| CBP-WP-005 | Benchmark Dataset and Retrieval Evaluation Design | P0 | **`committed`** | [work-packages/CBP-WP-005.md](../work-packages/CBP-WP-005.md) |
| CBP-WP-006 | G0 Scope-Lock Review and Pilot Source Contract | P0 | **`committed`** | [work-packages/CBP-WP-006.md](../work-packages/CBP-WP-006.md) |
| CBP-WP-007 | G0 Decision Recording and Phase 1 Backlog | P0 | **`committed`** | [work-packages/CBP-WP-007.md](../work-packages/CBP-WP-007.md) |
| CBP-WP-008 | Phase 1 Foundation Implementation Plan | P0 | **`committed`** | [work-packages/CBP-WP-008.md](../work-packages/CBP-WP-008.md) |
| CBP-WP-009 | **Repository Boundary Decision** | P0 | **`committed`** | [work-packages/CBP-WP-009.md](../work-packages/CBP-WP-009.md) |
| CBP-WP-010 | **Pilot Source Mapping Specification** | P0 | **`committed`** | [work-packages/CBP-WP-010.md](../work-packages/CBP-WP-010.md) |
| CBP-WP-011 | **Technical Security Foundation Specification** | P0 | **`committed`** | [work-packages/CBP-WP-011.md](../work-packages/CBP-WP-011.md) |
| CBP-WP-012 | **Foundation Runtime Skeleton** | P1 | **`committed`** | [work-packages/CBP-WP-012.md](../work-packages/CBP-WP-012.md) |
| CBP-WP-013 | **Ingest Quarantine Minimum Viable Pipeline** | P1 | **`committed`** | [work-packages/CBP-WP-013.md](../work-packages/CBP-WP-013.md) |
| CBP-WP-014 | **Deterministic Source Registry and Catalog** | P1 | **`committed`** | [work-packages/CBP-WP-014.md](../work-packages/CBP-WP-014.md) |
| CBP-WP-015 | **Deterministic Source Mapping Draft Validator** | P1 | **`committed`** | [work-packages/CBP-WP-015.md](../work-packages/CBP-WP-015.md) |
| CBP-WP-016 | **Deterministic Mapping Activation Gate Evaluator** | P1 | **`committed`** | [work-packages/CBP-WP-016.md](../work-packages/CBP-WP-016.md) |
| CBP-WP-017 | **Synthetic Evidence Contract & Provenance Foundation** | P1 | **`committed`** | [work-packages/CBP-WP-017.md](../work-packages/CBP-WP-017.md) |
| CBP-WP-018 | **Security Foundation Readiness Contract & Synthetic Form-Validator** | P1 | **`committed`** | [work-packages/CBP-WP-018.md](../work-packages/CBP-WP-018.md) |

**Kein Work Package ist als `proposed` geführt.** CBP-WP-018 (Security Foundation
Readiness Contract & Synthetic Form-Validator) ist **`committed`** — Phase B0
(Governance Foundation) mit `4dec921` und Phase B1 (Technical Implementation)
mit `5ee2e83` (A0-Freigaben **D-052**, **D-053**; **ADR-0013** angenommen) — und
mit `origin/main` synchron. Der Runtime-Stand ist **Evidence Schema 3.0** mit
statischem **Security Contract 1.0**. CBP-WP-017 ist `committed` (`d3168c4`,
D-051); CBP-WP-016 ist `committed` (`04c427c`, D-050). **Kein** Work Package ist
`active` oder `in-review`; **zuletzt abgeschlossen ist CBP-WP-018**. Ein
**nächstes autorisiertes Work Package existiert nicht**. **CBP-WP-019 ist nicht
Bestandteil, nicht registriert, nicht begonnen und nicht autorisiert.**

> **Titelkorrektur in CBP-WP-009.** Diese Übersichtstabelle trug bis dahin die
> Titel eines verworfenen Entwurfs der Work-Package-Karte (009 „Repository and
> Workspace Decision", 011 „Technical Security Foundation", 012 „Ingest
> Quarantine…", 013 „Deterministic Source Registry", 014 „Phase 1 Evidence
> Consolidation"). Verbindlich sind die Titel aus
> `PHASE_1_WORK_PACKAGE_MAP.md`; der Detailblock weiter unten war bereits
> korrekt. Der Fehler stammt aus CBP-WP-008.

> Die frühere Regel „genau ein Work Package ist `proposed`" gilt nicht mehr:
> CBP-WP-008 hat den gesamten Phase-1-Einstieg auf einmal geschnitten. Regel 4
> (**genau ein `active`**) bleibt unberührt.

---

## CBP-WP-001

| Feld | Wert |
| --- | --- |
| Typ | `docs-only` · Prompt Mode Standard · Budget B2 |
| Status | **`committed`** |
| Git-Beleg | `849794e CBP-WP-001: bootstrap NDF project foundation` |

## CBP-WP-002

| Feld | Wert |
| --- | --- |
| Typ | `docs-only` · Prompt Mode Full · Budget B2 |
| Status | **`committed`** |
| Git-Beleg | `18fda97 CBP-WP-002: reconcile sources and define G0 criteria` |

Der Status wurde in CBP-WP-003 von `in-review` auf `committed` nachgeführt —
die Queue war gegenüber dem Git-Stand veraltet.

**Nachträglicher Befund:** Die in CBP-WP-002 berichteten Kennzahlen waren
fehlerhaft addiert (41/39/35/55 statt 47/45/38/56). Korrigiert in CBP-WP-003,
erfasst als R-33. Die Dokumente selbst waren vollständig.

## CBP-WP-003

| Feld | Wert |
| --- | --- |
| Typ | `docs-only` · Prompt Mode **Full** · Budget **B1 – Lean** |
| Status | **`committed`** |
| Git-Beleg | `b1a6c2f CBP-WP-003: capture human discovery evidence` |

Ergebnis: 6 Antworten erhoben, 12 A0-Entscheidungen (D-015 bis D-026),
G0-Kriterien dreistufig klassifiziert, Blocker von 45 auf 25 reduziert,
fehlerhafte Summen korrigiert.

## CBP-WP-004

| Feld | Wert |
| --- | --- |
| Typ | `docs-only` · Prompt Mode **Full** · Budget **B2 – Standard** |
| Status | **`committed`** |
| Git-Beleg | `4cddc28 CBP-WP-004: define generic architecture and deployment profiles` |

Ergebnis: deployment-neutrale Systemarchitektur in 9 Schichten, 14 logische
Komponenten mit Schreibrechten, 5 Deploymentprofile, Deployment Readiness Check
(18 Prüfpunkte, NOT EVALUATED), Berechtigungsmodell, Secret-Incident-Response,
5 ADRs. G0-`accepted` von 8 auf **18** gestiegen; verbleibende Blocker von 17
auf **7**.

## CBP-WP-005

| Feld | Wert |
| --- | --- |
| Typ | `docs-only` · Prompt Mode **Full** · Budget **B2 – Standard** |
| Status | **`committed`** |
| Git-Beleg | `70132b3 CBP-WP-005: design benchmark dataset and retrieval evaluation` |

Ergebnis: synthetischer Benchmark-Korpus mit 24 Quellen und 3 fiktiven
Projekten, **A0 bis A6** belegt, 36 Fragen in 6 Kategorien, Evaluationsplan
V0/V1/V2, Metrikrubrik mit 9 kritischen Fehlern, Dataset 2.0.0.
**G-1 bis G-6 auf `accepted`**; verbleibende Blocker von 7 auf **1**.

Enthält einen **Korrekturlauf nach Nova-REWORK**: das A0-Fixture fehlte in der
Erstausführung.

**Nicht durchgeführt:** kein Lauf, keine Messung, kein Index, keine
Suchsoftware.

## CBP-WP-006

| Feld | Wert |
| --- | --- |
| Typ | `docs-only` · Prompt Mode **Full** · Budget **B1 – Lean** |
| Status | **`committed`** |
| Git-Beleg | `f93f257 CBP-WP-006: prepare G0 scope-lock review and source contract` |

Ergebnis: Pilot Source Contract mit 7 logischen Source Slots,
Source-Slot-Modell mit 10 Validierungsregeln, ADR-0006 (`proposed`),
G0-Evidenzmatrix über alle 25 Core-Kriterien, entscheidungsreife
G0-Review-Unterlage.

**D-1 von `answered` auf `accepted`** — alle 25 Core-Kriterien sind belegt.

**Gate-Status zum Abschluss von CBP-WP-006: NOT PASSED**, Entscheidungsblock leer. Die Entscheidung erfolgte anschließend in CBP-WP-007.

## CBP-WP-007

| Feld | Wert |
| --- | --- |
| Typ | `docs-only` · Prompt Mode **Standard** · Budget **B0 – Micro** |
| Status | **`committed`** |
| Ablauf | interaktiv — Phase A Entscheidungsfragebogen, Phase B Aufzeichnung |
| Git-Beleg | `5e9c687 CBP-WP-007: record G0 approval and phase 1 planning backlog` |

Ergebnis: **G0 PASSED WITH NOTES** und **ADR-0006 accepted**, beide am
2026-07-21 durch den Human Maintainer (A0). Phase-1-Backlog mit 11 Punkten,
Status **AUTHORIZED FOR PLANNING**. Zähl- und Statusregel ergänzt.

## CBP-WP-008

| Feld | Wert |
| --- | --- |
| Titel | **Phase 1 Foundation Implementation Plan** |
| Typ | `docs-only` · Prompt Mode **Full** · Budget **B2 – Standard** |
| Status | **`committed`** |
| Git-Beleg | `47a336d CBP-WP-008: plan phase 1 foundation work` |

Ergebnis: drei veraltete Gate-Angaben korrigiert · P1–P5 als Streams **F1–F5**
geplant · Repository- und Workspace-Schnitt entscheidungsreif (W-1/W-2/W-3) ·
Mappingschema mit 19 Feldern · **zwölf Kontrollbereiche** KB-01…KB-12 ·
fail-closed Quarantäne mit 12 Schritten und 10 Status · Registry mit 24 Feldern
· **sechs Folge-Work-Packages geschnitten** · sechs Nachweisstufen · zwölf
Stop-Bedingungen · **vierter Zählfehler gefunden und korrigiert**.

> **Historische Planungsannahme (nicht umgeschrieben).** Das oben genannte
> „Mappingschema mit 19 Feldern" war die **Planungsannahme aus CBP-WP-008**. Sie
> wurde durch den angenommenen A1/A2-Vertrag (ADR-0008, CBP-WP-010) mit **31
> Felddefinitionen** (29 Pflicht + 2 optional) und **24 Validierungsregeln**
> **abgelöst**. Diese historische Aussage bleibt als Beleg des damaligen Stands
> erhalten; die 19/31-Korrektur der **aktuellen** Planungsdokumente ist in
> CBP-WP-015 (R-33, neunter Konsistenzvorgang) dokumentiert.

**Nichts gebaut, nichts installiert, nichts verschoben, nichts gemessen.**

## CBP-WP-009

| Feld | Wert |
| --- | --- |
| Titel | **Repository Boundary Decision** |
| Typ | `docs-only`, **interaktiv** |
| Prompt Mode | **Full** · Context Budget **B1 – Lean** |
| Claude Code | Opus 4.8 (`claude-opus-4-8`), Effort **xhigh** |
| Status | **`committed`** |
| Git-Beleg | `1227aa5 CBP-WP-009: decide repository and workspace boundaries` |

Ergebnis: **OD-26 geschlossen** durch zwei getrennte A0-Entscheidungen —
**D-029** (Teil A, Ziel-Monorepo nach Layout-Option B) und **D-030** (Teil B,
Modell W-3, privater Operator-Workspace außerhalb des Core-Repositorys).
**ADR-0007** `accepted`. Titelkorrektur in der Übersichtstabelle.

**Keine Reorganisation, kein Verzeichnis angelegt, kein Workspace erzeugt.**
Die Migration in die Zielstruktur bleibt einem separaten, ausdrücklich
freigegebenen Work Package vorbehalten.

## CBP-WP-010

| Feld | Wert |
| --- | --- |
| Titel | **Pilot Source Mapping Specification** |
| Typ | `docs-only`, **interaktiv** |
| Prompt Mode | **Full** · Context Budget **B1 – Lean** |
| Claude Code | Opus 4.8 (`claude-opus-4-8`), Effort **xhigh** |
| Status | **`committed`** |
| Git-Beleg | `43bb4e3 CBP-WP-010: specify pilot source mapping contract` |

Ergebnis: **drei A0-Entscheidungen** — D-031 (YAML-1.2-Strict-Subset mit
JSON-Schema-Vertragsgrenze), D-032 (hybride Collection-Strategie), D-033 (eine
Source Boundary je Mapping). **ADR-0008** `accepted`. Mapping-Spezifikation,
Feldschema mit **31 Feldern**, **24 Validierungsregeln**, Zustandsmodell mit
**10 Zuständen**, slotspezifische Regeln für PS-02/PS-03/PS-04, **10
synthetische Beispiele**, private Operator-Vorlage und das
**Aktivierungsgate** mit 20 Punkten (`NOT EVALUATED`). Klarstellungsnachtrag
zum Veröffentlichungsbegriff in ADR-0006.

**Kein Mapping erstellt, keine Quelle angebunden, nichts aktiviert.**

## CBP-WP-011

| Feld | Wert |
| --- | --- |
| Titel | **Technical Security Foundation Specification** |
| Typ | `docs-only`, **interaktiv** |
| Prompt Mode | **Full** · Context Budget **B2 – Standard** |
| Claude Code | Opus 4.8 (`claude-opus-4-8`), Effort **ultracode** (deklariert) |
| Status | **`committed`** |
| Git-Beleg | `8a7c455 CBP-WP-011: specify technical security foundation` |

Ergebnis: **vier A0-Entscheidungen** — D-034 (getrennte Service-Identitäten),
D-035 (versionierter Secret-Reference-Vertrag plus OS-geschützter Datei-Provider),
D-036 (Egress deny-by-default), D-037 (RT-2 append-only und verkettet).
**ADR-0009** `accepted`. Sicherheitsspezifikation mit **18 Abschnitten**, zwölf
Kontrollbereichen, **neunstufiger Durchsetzungsreihenfolge**, Identitäts- und
Privilegienmodell, Secret-Vertrag, Egress-Policy, Operational-Evidence-Policy
mit 18 Feldern und 17 Ereignisarten, **32 Negativtests plus 1 Positivtest** und einem Readiness
Gate mit 24 Punkten (`NOT EVALUATED`). **OD-34 und OD-35 geschlossen.**

**Keine Kontrolle umgesetzt, kein Test ausgeführt.** Alle zwölf stehen auf
**DOCUMENTED ONLY**.

## CBP-WP-012

| Feld | Wert |
| --- | --- |
| Titel | **Foundation Runtime Skeleton** |
| Typ | **implementation**, interactive authorization |
| Prompt Mode | **Full** · Context Budget **B2 – Standard** |
| Claude Code | Opus 4.8 (`claude-opus-4-8`), Effort **ultracode** (deklariert) |
| Status | **`committed`** |
| Git-Beleg | `1f55234 CBP-WP-012: implement fail-closed runtime skeleton` |

Ergebnis: **erstes Artefakt mit technischer Wirkung.** Human-Autorisierung
APPROVE WITH NOTES (A0); A1, B1, C1. Additive Struktur `core/`, `config/`,
`examples/`, `tests/`, `docs/runtime/`; **9 Runtime-Module**, lokale CLI
(`version`, `validate-config`, `doctor`, `run`), strikte fail-closed
Konfigurationsvalidierung, vier verweigernde Ports. **Python 3.13.14**, keine
Abhängigkeiten. **69 Tests bestanden**, alle Smoke-Tests mit erwarteten
Exitcodes; `run` verweigert (Exit 4).

**Keine KB-Kontrolle durchgesetzt** — alle bleiben `DOCUMENTED ONLY`. **Kein
Gate bestanden, kein Risiko geschlossen.**

## CBP-WP-013

| Feld | Wert |
| --- | --- |
| Titel | **Ingest Quarantine Minimum Viable Pipeline** |
| Typ | **implementation**, interactive authorization |
| Prompt Mode | **Full** · Context Budget **B2 – Standard** |
| Claude Code | Opus 4.8 (`claude-opus-4-8`), Effort **ultracode**; **A0-Modellsubstitution** (Fable 5 nicht verfügbar) |
| Status | **`committed`** |
| Git-Beleg | `4a35245 CBP-WP-013: implement synthetic ingest quarantine MVP` |

Ergebnis: **zweites Artefakt mit technischer Wirkung.** Human-Autorisierung
APPROVE WITH NOTES (A0); A1, B1, C1, D1. Lokaler, synthetisch testbarer,
fail-closed Quarantäneprototyp: **6 Quarantäne-Module**, Beispiel-Policy,
CLI-Kommandogruppe `quarantine` (`scan`, `stage`, `inspect`, `release`),
content-addressed Store außerhalb des Repos, minimierte Records. **Python
3.13.14**, keine Abhängigkeiten. **137 Tests bestanden** (Basislinie WP-012: 69,
weiterhin grün), CLI-Smoke mit Exitcodes 0/5/6/7. **ADR-0010** `accepted`
(D-038 bis D-041); **OD-37, OD-38** neu offen.

**Keine KB-Kontrolle durchgesetzt** — alle bleiben `DOCUMENTED ONLY`. **Kein
Gate bewertet, kein Risiko geschlossen, nichts freigegeben oder promotet.**
Capability 5 bleibt **nicht** vollständig `implemented`.

## CBP-WP-014

| Feld | Wert |
| --- | --- |
| Titel | **Deterministic Source Registry and Catalog** |
| Typ | **implementation**, interactive authorization |
| Prompt Mode | **Full** · Context Budget **B2 – Standard** |
| Claude Code | Opus 4.8 (`claude-opus-4-8`), Effort **ultracode** |
| Status | **`committed`** |
| Git-Beleg | `d0c0531 CBP-WP-014: implement deterministic source registry MVP` |

Ergebnis: **drittes Artefakt mit technischer Wirkung.** Human-Autorisierung
APPROVE WITH NOTES (A0); A1, B1, C1, D1. Lokaler, synthetisch testbarer,
**deaktivierter** Registry- und Catalog-Prototyp: **6 Registry-Module**,
Beispiel-Policy, CLI-Kommandogruppe `source-registry` (`validate-definition`,
`register`, `list`, `inspect`, `retire`, `activate`), unveränderliche Records
und append-only Retirement außerhalb des Repos, deterministisch abgeleiteter
minimierter Katalog. **Python 3.13.14**, keine Abhängigkeiten. **212 Tests
bestanden** (Basislinie WP-013: 137, weiterhin grün), CLI-Smoke mit neuen
Exitcodes 8/9/10/11. **ADR-0011** `accepted` (D-042 bis D-045); keine neue
offene Entscheidung.

**Keine KB-Kontrolle durchgesetzt** — alle bleiben `DOCUMENTED ONLY`. **Kein
Gate bewertet, kein Risiko geschlossen, nichts aktiviert oder gemappt.**
Capability 2/3/7 (Source Registry / Katalog) bleiben **nicht** vollständig
`implemented`.

## CBP-WP-015

| Feld | Wert |
| --- | --- |
| Titel | **Deterministic Source Mapping Draft Validator** |
| Typ | **implementation**, interactive authorization |
| Prompt Mode | **Full** · Context Budget **B2 – Standard** |
| Claude Code | Opus 4.8 (`claude-opus-4-8`), Effort **ultracode** |
| Status | **`committed`** |
| Git-Beleg | `645ccb1 CBP-WP-015: implement source mapping draft validator` |
| Status-Reconciliation | `8d715e7 CBP-WP-015: reconcile post-commit status` |

Ergebnis: **viertes Artefakt mit technischer Wirkung.** Human-Autorisierung
APPROVE WITH NOTES (A0); A1/B1/C1/D1. Lokaler, synthetischer, **read-only**,
nicht persistenter und fail-closed Mapping-Draft-Validator gegen den
angenommenen **31-Feld-Vertrag** (29 Pflicht + 2 optional); externe read-only
Registry-Bindung (`collection`/`data_class` exakt); `mapping_id` nur validiert,
nie berechnet; nicht persistierter Report; `activation-check` verweigert immer.
**6 Mapping-Module**, CLI-Gruppe `source-mapping` (`validate-draft`,
`activation-check`), neue Exitcodes 12/13. **Python 3.13.14**, keine
Abhängigkeiten, **315 Tests bestanden** (Basislinie WP-014: 212, weiterhin grün).
**ADR-0012** `accepted` (D-046 bis D-049); keine neue offene Entscheidung.

**Keine KB-Kontrolle durchgesetzt, kein Gate bewertet, kein Mapping gespeichert,
keine Aktivierung, keine reale Source, keine Produktionsreife.** Capability 2/7
bleiben **nicht** vollständig `implemented`.

> **Historischer Vorbereitungsstand (vor der A0-Implementierungsfreigabe):**
> Dieser Detailblock führte CBP-WP-015 zuvor als „**`proposed`. Implementierung
> autorisiert: nein.**". Das war der **Planungsstand vor** der späteren
> A0-Implementierungsfreigabe und ist durch den belegten `committed`-Zustand
> (`645ccb1`, Status-Reconciliation `8d715e7`) **abgelöst**.

## CBP-WP-016

| Feld | Wert |
| --- | --- |
| Titel | **Deterministic Mapping Activation Gate Evaluator** |
| Typ | **implementation**, interactive authorization |
| Prompt Mode | **Full** · Context Budget **B2 – Standard** |
| Claude Code | Opus 4.8 (`claude-opus-4-8`), Effort **ultracode** |
| Status | **`committed`** |
| Git-Beleg | `04c427c CBP-WP-016: implement mapping activation gate evaluator` |
| A0-Entscheidung | **D-050** (APPROVE WITH NOTES; A1/B1-eng/C1/D1) |

Ergebnis: **fünftes Artefakt mit technischer Wirkung.** Phase A/A.1 read-only
abgeschlossen (Feasibility PASS WITH NOTES); Human-Autorisierung **D-050**:
APPROVE WITH NOTES (A0), A1/B1-eng/C1/D1. Lokaler, synthetischer, **read-only**,
nicht persistenter, fail-closed Evaluator der Review-Bereitschaft anhand der
**20 kanonischen Gate-Kriterien**: **5 Gate-Module** (`core/core_brain/gate/`),
CLI `source-mapping activation-evaluate`, neuer Exitcode **14**. Ausgabestatus
ausschließlich `NOT_EVALUATED`/`BLOCKED`; `READY FOR ACTIVATION DECISION`,
`APPROVED FOR ACTIVATION` und `REVOKED` sind **nicht** emittierbar. Security
Foundation/DRC sind **keine** Kriterien 21/22. **Python 3.13.14**, keine
Abhängigkeiten, **398 Tests bestanden** (Basislinie WP-015: 315, weiterhin grün),
**compileall OK**. **Kein neues ADR**; keine neue offene Entscheidung.

**Kein Gate ausgeführt, kein Gate freigegeben, kein Gate-Status geändert, keine
Aktivierung, kein gespeichertes Ergebnis, keine reale Source, keine
Produktionsreife.** Capability-Stand unverändert **0 von 29**.

> **Historischer Vorbereitungsstand (vor dem Commit):** Dieser Detailblock
> führte CBP-WP-016 zuvor als „**`in-review`. Commit nicht ausgeführt.**" — der
> korrekte **Vor-Commit-Reviewstatus**. Er ist durch den belegten
> `committed`-Zustand (`04c427c`, mit `origin/main` synchron) **abgelöst**.

## CBP-WP-017

| Feld | Wert |
| --- | --- |
| Titel | **Synthetic Evidence Contract & Provenance Foundation** |
| Typ | **implementation** |
| Prompt Mode | **Full** · Context Budget **B2 – Standard** |
| Claude Code | Opus 4.8 (`claude-opus-4-8`), Effort **ultracode** |
| Status | **`committed`** |
| Git-Beleg | `d3168c4 CBP-WP-017: implement synthetic evidence contract` |
| A0-Entscheidung | **D-051** (APPROVE WITH NOTES; A2/B1/C2/D1/E2) |

Ergebnis: **sechstes Artefakt mit technischer Wirkung.** Human-Autorisierung
**D-051**. Geschlossener, deterministischer, **synthetic-only** Evidence-Vertrag
**2.0** mit eingebetteten strukturierten Artefakten: **neues Modul**
`core/core_brain/gate/provenance.py`, erweiterte `evidence.py`/`evaluator.py`/
`service.py`/`models.py`; Provenance-/Binding-Hashes, deterministische
**Invalid-/Stale-/Conflict-Erkennung** (ohne Uhr), **negative-evidence-only**
(keine positive Gate-Erfüllung), minimal erweiterter A6-Report (6 Felder).
Schema **1.0 fail-closed**. Bestehender CLI-Pfad `activation-evaluate --evidence`
unverändert (Exit 14); `activation-check` bleibt 13. **Python 3.13.14**, keine
Abhängigkeiten, **451 Tests bestanden** (Basislinie WP-016: 398, weiterhin grün),
**compileall OK**. **Kein neues ADR**; keine neue offene Entscheidung.

**Keine reale/operative Evidenz, keine Evidence-Promotion, kein Gate ausgeführt/
freigegeben, keine Aktivierung, kein RT-2, keine Persistenz, keine
Produktionsreife.** Capability-Stand unverändert **0 von 29**.

> **Historischer Vorbereitungsstand (vor dem Commit):** Dieser Detailblock
> führte CBP-WP-017 zuvor als „**`in-review`. Commit nicht ausgeführt.**" — der
> korrekte **Vor-Commit-Reviewstatus**. Er ist durch den belegten
> `committed`-Zustand (`d3168c4`, mit `origin/main` synchron) **abgelöst**.

## CBP-WP-018

| Feld | Wert |
| --- | --- |
| Titel | **Security Foundation Readiness Contract & Synthetic Form-Validator** |
| Typ | **implementation** (Governance-Phase vorangestellt) |
| Prompt Mode | **Full** · Context Budget **B2 – Standard** |
| Claude Code | Opus 4.8 (`claude-opus-4-8`), Effort **ultracode** |
| Status | **`committed`** |
| Abgeschlossene Phasen | **Phase B0 – Governance Foundation** · **Phase B1 – Technical Implementation** |
| A0-Entscheidungen | **D-052** (Governance Foundation; `committed` `4dec921`) · **D-053** (APPROVE TECHNICAL IMPLEMENTATION WITH NOTES; A1/B1/C1/D1/E1) |
| ADR | **ADR-0013** `accepted` (Evidence Schema 3.0) |
| Tests | **558 – OK** (Basislinie 451), compileall Exit 0 |
| Git-Beleg (Governance) | `4dec921 CBP-WP-018: establish evidence schema 3 governance` |
| Git-Beleg (Implementation) | `5ee2e83 CBP-WP-018: implement evidence schema 3 security contract` |

Phase A/A.1 read-only abgeschlossen (Phase A REWORK, A.1 angenommen); Blocker A
(fehlendes `control_id`) und Blocker B (fehlende Security-Contract-Bindung)
bestätigt. **Phase B0** (`committed` `4dec921`): **ADR-0013** angenommen,
**D-052** dokumentiert (partielle Ablösung von D-051: C2/D1). **Phase B0.1**:
R-33-Konsistenzkorrektur (ADR-Indexzahl 11 → 13), R-33 = **14/18**.

**Phase B1 (`committed` `5ee2e83`):** Evidence Schema **2.0 → 3.0**
vollständig migriert (1.0 und 2.0 fail-closed); Producer-Klasse
`security-control-form` mit Pflichtfeld `control_id`; neues reines Modul
`core/core_brain/gate/security_contract.py` (Revision 1.0, **12** dokumentierte
/ **7** runtime-scoped Controls / **11** `(criterion, control_id)`-Bindungen);
per-Bindungs-Verdikte mit Priorität `INVALID > CONFLICTING > STALE`; A6-Report
um Contract-Revision/-Hash und fünf Binding-Zähler (Summeninvariante = 11)
erweitert; **D-053** dokumentiert. Der Commit umfasst **32 Pfade** (29
modifiziert, 3 neu, 0 gelöscht, 0 umbenannt).

> **Historischer Vorbereitungsstand (vor dem Commit):** Dieser Detailblock
> führte CBP-WP-018 zuvor als „**`in-review`**, Phase B1, Commit nicht
> ausgeführt" — der korrekte **Vor-Commit-Reviewstatus**. Er ist durch den
> belegten `committed`-Zustand (`5ee2e83`, mit `origin/main` synchron)
> **abgelöst**.

**Keine Security-Evaluation, kein Enforcement, keine Gatefreigabe, keine
Aktivierung, kein RT-2, keine Persistenz, keine Produktionsreife.**
Capability-Stand unverändert **0 von 29**; alle drei Gates `NOT EVALUATED`; die
zwölf KB-Kontrollen bleiben `DOCUMENTED ONLY`. Kriterium 5 Human-only,
Kriterium 9 non-security-structural, Gate-Kriterien 4/6/7/8/10/11 bleiben
`DEPENDENCY_BLOCKED` — auch bei elf gültigen Formbindungen.

---

## Regeln

Aus `WORK_PACKAGE_QUEUE_TEMPLATE.md` (NDF v1.0.0):

1. Work Packages klein halten.
2. Jedes Work Package braucht eine Rückmeldung an Nova.
3. **Keine autonomen Commits oder Pushes.**

Ergänzend:

4. Genau ein Work Package ist gleichzeitig `active`.
5. Der Lifecycle wird vollständig durchlaufen.
6. Statuswechsel nach `released` nur durch den Human Maintainer.
7. Der Status `committed` wird nur vergeben, wenn Git ihn bestätigt.
8. Bei fehlender Autorisierung: nicht raten, anhalten, Blocker melden.
9. Kennzahlen werden **ausgezählt**, nicht aus dem Vorbericht fortgeschrieben
   (R-33).
