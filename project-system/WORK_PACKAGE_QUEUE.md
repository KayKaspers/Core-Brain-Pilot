# Work Package Queue – Core Brain Pilot

| Feld | Wert |
| --- | --- |
| Phase | **Phase 0 COMPLETE** · Phase 1 AUTHORIZED FOR PLANNING |
| Aktuelles Work Package | **CBP-WP-022** (`in-review`, **Phase B2A – Contract Model and Read-only Validator**) — **D-057** Registrierung, **D-058** ADR-Gate (**`ADR_REQUIRED`**), **D-059** Architekturannahme und **D-060** Enforcement Contract (alle `accepted`, **A0**, 2026-08-03); **ADR-0014 `accepted`, Autoritätsklasse A1** — **Host-authoritative Enforcement mit deklarativem Zielmodell und read-only Runtime-Validierung**; Vertrag [KB_04_STAGE_1_ENFORCEMENT_CONTRACT.md](../docs/security/KB_04_STAGE_1_ENFORCEMENT_CONTRACT.md) **`accepted contract`** (**`ADR_NOT_REQUIRED`** innerhalb ADR-0014); B0 `committed` (`e4caa14`), B1A `committed` (`1a7696d`), B1B `committed` (`b86a35f`), B1C `committed` (`24de07e`), **B2A uncommitted**; **B2A implementiert das interne, read-only Enforcement-Paket** `core/core_brain/enforcement/` (sechs Module, 21 additive `KB04-*`-ReasonCodes, **206 neue Tests**, Gesamtsuite **930 grün**) — **keine CLI, keine Config, kein Deployment, keine Mutation, keine operative Evidenz**; **KB-04 Enforcement Stage 1** bleibt `DOCUMENTED ONLY`; **B2B, B2C und B2D nicht autorisiert**. Zuletzt abgeschlossen **CBP-WP-021** (`committed`, `complete`, 2026-08-03; **D-056**, `ADR_NOT_REQUIRED`; kanonisch **32 Negativtests / 1 Positivtest / 33 Testfälle**, **0 von 32** und **0 von 1** ausgeführt; B0 `0cb4ea9`, B1/B2 `271acc7`). Zuvor abgeschlossen **CBP-WP-020** (`committed`, `complete`; B0 `17057e2`, B1/B2 `9c6c0fb`, C `d6a1a3c`). **CBP-WP-023 nicht registriert, nicht autorisiert.** |
| Gate G0 | **PASSED WITH NOTES** — 2026-07-21 |
| Überarbeitet in | **CBP-WP-016** |
| Autoritätsklasse | A2 |
| Stand | 2026-08-03 — CBP-WP-022 Phase B2A |

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
| CBP-WP-019 | **Deployment Readiness Intake and Profile-A Target Specification** | P1 | **`committed`** | [work-packages/CBP-WP-019.md](../work-packages/CBP-WP-019.md) |
| CBP-WP-020 | **Controlled Profile-A Deployment Foundation** | P1 | **`committed`** (B0 `17057e2`, B1/B2 `9c6c0fb`) | [work-packages/CBP-WP-020.md](../work-packages/CBP-WP-020.md) |
| CBP-WP-021 | **Canonical Security Test Inventory Reconciliation** | P1 | **`committed`** (B0 `0cb4ea9`, B1/B2 `271acc7`, C `0344774`) | [work-packages/CBP-WP-021.md](../work-packages/CBP-WP-021.md) |
| CBP-WP-022 | **KB-04 Enforcement Stage 1** | P1 | **`in-review`** (Phase B2A; B0 `committed` `e4caa14`, B1A `committed` `1a7696d`, B1B `committed` `b86a35f`, B1C `committed` `24de07e`; **ADR-0014 `accepted`/A1**, **Contract `accepted`**, **Validatorpaket implementiert**) | [work-packages/CBP-WP-022.md](../work-packages/CBP-WP-022.md) |

**Kein Work Package ist als `proposed` geführt.** **CBP-WP-019** (Deployment
Readiness Intake and Profile-A Target Specification) steht auf **`in-review`** in
**`committed`** (`3c437f2`, A0-Freigabe **D-054**; **ADR_NOT_REQUIRED**) und mit
`origin/main` synchron. Es war ein **docs-only, interaktives** Paket: die
Deploymentangaben des Human Maintainers wurden dokumentiert, der DRC von 18 auf
**19** Prüfpunkte erweitert und für **Profil A** vollständig erhoben — **19
`ready`, 0 `blocked`**; der Human Maintainer hat am **2026-07-29** den
**DRC-Gesamtstatus** auf **APPROVED BY HUMAN MAINTAINER** gesetzt — **rein
dokumentarisch**, ohne Installations-, Betriebs-, Security- oder
Capability-Freigabe. CBP-WP-018 ist `committed` (Phase B0
`4dec921`, Phase B1 `5ee2e83`, D-052/D-053, ADR-0013); CBP-WP-017 ist `committed`
(`d3168c4`, D-051); CBP-WP-016 ist `committed` (`04c427c`, D-050). **CBP-WP-020** (Controlled Profile-A Deployment Foundation) ist unter **D-055**
(`ADR_NOT_REQUIRED`) **`committed` und `complete`**: Zielzustand **Z1 erreicht**,
Scope **S2 abgeschlossen**, RT-2-Grenze **P1 eingehalten**; Phase B0 `17057e2`,
Phase B1/B2 `9c6c0fb`. Das Bundle unter **`deployments/profile-a/`** liegt mit
**genau sieben Dateien** vor und ist **offline validiert**
(`PROFILE-A-BUNDLE VALID`, Exit 0). **Nichts wurde bereitgestellt oder
gestartet.** **Phase B3 (reale Bereitstellung) ist ausdrücklich nicht
Bestandteil** von CBP-WP-020.

**CBP-WP-021** (Canonical Security Test Inventory Reconciliation) ist unter
**D-056** (`ADR_NOT_REQUIRED`) **`committed`** und **`complete`** — abgeschlossen
am **2026-08-03**, Phase B0 `0cb4ea9`, Phase B1/B2 `271acc7`. D-056 stellt das
kanonische Security-Foundation-Testinventar verbindlich fest: **32 Negativtests**
(NT-01…NT-24 und NT-26…NT-33), **1 Positivtest** (PT-01), **33 Testfälle**;
**NT-25 bleibt nach Regel TT-5 bewusst frei**, **NT-32 und NT-33 sind gültig**.
Die Zahl **31** ist ein **überholter, falsch etikettierter Ableitungswert**.
**Ausgeführt sind weiterhin 0 von 32 Negativtests und 0 von 1 Positivtest** —
weder die Feststellung eines Inventarwerts noch dessen Reconciliation ist eine
Testausführung oder Gateauswertung. Die Reconciliation umfasste auch die
**ausführbaren** Artefakte des Profil-A-Bundles.

**CBP-WP-022** (KB-04 Enforcement Stage 1) ist unter **D-057** (`accepted`, **A0**,
2026-08-03) **registriert** und steht auf **`in-review`** in **Phase B0 –
Registration and Authority Baseline**. „Enforcement Stage 1“ bezeichnet
**Stufe 1 der neunstufigen technischen Durchsetzungsreihenfolge** (**OS-Dateirechte**);
**KB-04 ist die unterste tragende Ebene**. **KB-04 bleibt `DOCUMENTED ONLY`** — die
Registrierung ist **keine Implementierungsfreigabe**; **B1 und B2 sind nicht
autorisiert**. `ADR_NOT_REQUIRED` gilt **ausschließlich** für die
Registration-Decision. Genau **ein** Work Package ist `in-review` (CBP-WP-022);
**zuletzt abgeschlossen ist CBP-WP-021**. **CBP-WP-023 ist nicht registriert,
nicht begonnen und nicht autorisiert.**

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
(damals 18 Prüfpunkte, NOT EVALUATED; seit CBP-WP-019 **19**), Berechtigungsmodell, Secret-Incident-Response,
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

## CBP-WP-019

| Feld | Wert |
| --- | --- |
| Titel | **Deployment Readiness Intake and Profile-A Target Specification** |
| Typ | **docs-only, interaktiv** (Human-Maintainer-Intake) |
| Prompt Mode | **Full** · Context Budget **B2 – Standard** |
| Status | **`committed`** |
| Abgeschlossene Phasen | **B1 – Registration and Human Intake** · **B1.1 – Final Human Evidence Reconciliation** · **B1.2 – Human DRC Approval Reconciliation** · **C – Post-Commit Reconciliation** |
| Git-Beleg | `3c437f2 CBP-WP-019: approve profile A deployment readiness` |
| Abschlussdatum | **2026-07-29** |
| A0-Entscheidung | **D-054** (konsolidiert, A–H) |
| ADR | **not required** (`ADR_NOT_REQUIRED`) |
| DRC | **19 Prüfpunkte** — **19 `ready`**, **0 `blocked`**; Gesamtstatus **APPROVED BY HUMAN MAINTAINER**, erteilt **2026-07-29** |
| Tests | **558 – OK**, compileall Exit 0 (docs-only, unverändert) |
| Commit | **`3c437f2`** — durch den **Human Maintainer** erstellt und nach `origin/main` gepusht |

Phase A und Phase A.1 read-only abgeschlossen. Phase A bestätigte die
18/16-Struktur des DRC und meldete drei Coverage-Lücken; **Phase A.1 löste den
gemeldeten DRC-16-Zyklus auf**: er entsteht nur unter einer nicht
quellengedeckten Lesart. Standardwert 10, **D-027 §16 (getrennte Bedingungen 2
und 4)** und **Readiness-Gate Punkt 19** belegen, dass der CBP-/RT-2-Restore
bereits nachgelagert verortet ist. Gewähltes Lifecycle-Modell: **L0** mit
Klarstellung des DRC-16-Prüfumfangs.

**Phase B1 (dieser Stand, uncommitted):** CBP-WP-019 registriert; **D-054**
dokumentiert (A Profil/Plattform · B Ressourcen · C Netzwerk · D Backup/Restore ·
E DRC-Lifecycle · F DRC-19 · G Secret-/Produktabgrenzung · H Governance);
**DRC-16 präzisiert** auf das Betreiber-Backup-Regime (nicht CBP, nicht RT-2);
**DRC-17 erweitert** um die OD-34-Restpunkte; **DRC-19 – RT-2-Aufbewahrung**
ergänzt (18 → **19** Prüfpunkte, davon 17 G0-abgeleitet und 2 ohne G0-Herkunft);
Profil-A-Zielspezifikation dokumentiert; Phase-1-Roadmap gebündelt nachgeführt.
**OD-22 und OD-30 beantwortet**; OD-20 bleibt außerhalb des DRC.

**Keine Installation, kein Deployment, keine Betriebsfreigabe, keine
Gatefreigabe, keine Aktivierung, kein RT-2, keine Persistenz.** Alle Angaben
sind **Zusagen des Human Maintainers**, keine verifizierten Messwerte; es fand
**kein** Zugriff auf Hypervisor, Speicher, Netz oder Sicherungsziel statt.
Capability-Stand unverändert **0 von 29**; Mapping Activation Gate und Security
Foundation Readiness Gate bleiben `NOT EVALUATED`; die zwölf KB-Kontrollen
bleiben `DOCUMENTED ONLY`. **R-20 bleibt offen.**

---

## CBP-WP-020

| Feld | Wert |
| --- | --- |
| Titel | **Controlled Profile-A Deployment Foundation** |
| Typ | **implementation** (Deployment-Artefakte, offline validiert) |
| Prompt Mode | **Full** · Context Budget **B2 – Standard** |
| Status | **`committed`** · **`complete`** |
| Aktuelle Phase | **Phase C – Post-Commit Reconciliation** (abgeschlossen) |
| A0-Entscheidung | **D-055** (konsolidiert, A–J) |
| ADR | **not required** (`ADR_NOT_REQUIRED`) |
| Zielzustand / Scope / RT-2 | **Z1 erreicht** / **S2 abgeschlossen** / **P1 eingehalten** |
| Tests | **724 – OK**, **0 übersprungen**; `compileall .` Exit 0, Validator Exit 0 |
| Git-Beleg | `17057e2 CBP-WP-020: register controlled deployment foundation` (B0) · `9c6c0fb CBP-WP-020: add validated profile A deployment bundle` (B1/B2) |

Phase A read-only abgeschlossen: bewertet wurden vier Zielzustände (Z0–Z3) und
vier Scope-Varianten (S1–S4). Empfohlen und übernommen: **Z1** (Artefakte plus
Offline-Validierung), **S2** (46/50) und **P1** (RT-2 nur als Vertrag).

**Phase B0 (`committed` `17057e2`):** CBP-WP-020 registriert; **D-055**
dokumentiert (A additive Struktur · B Verhältnis zu ADR-0007 · C Verhältnis zu
D-029 · D Zielzustand · E ausgeschlossener Scope · F RT-2-Grenze · G
Security-Status · H Capability-/Gate-Grenze · I `ADR_NOT_REQUIRED` · J Risiko).
Der Pfad **`deployments/profile-a/`** ist als **B1-Ort** autorisiert; die
Autorisierung ist **rein additiv**, **D-029 bleibt vollständig wirksam** und
**ADR-0007 unverändert**.

**Phase B1/B2 (`committed` `9c6c0fb`):** Das **Profil-A-Bundle** ist als
Repository-Artefakt angelegt — **genau sieben Dateien** unter
`deployments/profile-a/` (`README.md`, `bundle.json`, `compose.yaml`,
`operator.env.example`, `validate.py`, zwei TOML-Vorlagen unter `config/`).
Zwei getrennte Service-Identitäten (`svc-control-plane`, `svc-data-worker`),
fail-closed Compose-Vorlage, maschinenlesbare Mount-, Egress-, Secret-, Backup-
und RT-2-Verträge. Der **deterministische Offline-Validator** meldet
`PROFILE-A-BUNDLE VALID`, `issues=0`, **Exit 0**, bei zwei Läufen
**byte-identisch**. Ergänzt um **drei Runbooks**
(`docs/operations/PROFILE_A_{INSTALLATION,VALIDATION,ROLLBACK}_RUNBOOK.md`),
den **Runtime-Vertrag** `docs/runtime/PROFILE_A_DEPLOYMENT_BUNDLE.md` und
**166 neue Tests** in `tests/test_profile_a_deployment_bundle.py`
(Gesamtstand **724 – OK**, **0 übersprungen**). Der Symlink-Negativfall wird
deterministisch über die vollständige `validate_bundle`-Pipeline ausgeführt und
ist **nicht** umgebungsabhängig.

**Statusaussage ausschließlich:** *repository artifact implemented* · *offline
validation implemented* · *offline validation passed*. **Nicht** deployed,
**nicht** operational, **nicht** production-ready.

**Nicht ausgeführt:** kein Containerstart, kein Docker- oder Compose-Kommando,
kein Netzwerkzugriff, keine Port-, Prozess- oder Hostrechteprüfung, keine reale
UID-/GID-Ermittlung, keine Secret-Auflösung, kein Backup, kein Restore; **keine
Datei verschoben, umbenannt oder gelöscht**; **kein Runtime-Code geändert**.

**Die 166 neuen Tests sind Profile-A Bundle Validation Tests** — ausdrücklich
**keine** Security Foundation NT-01 bis NT-33 und **kein** PT-01. **Kanonische
Kennzahl (D-056): ausgeführt 0 von 32 Negativtests und 0 von 1 Positivtest.**

**B3 (reale Bereitstellung) ist ausdrücklich nicht Bestandteil** von CBP-WP-020
und verlangt ein eigenes Folge-Work-Package mit eigenem Human Gate.

**Keine Installation, keine Bereitstellung, keine Infrastrukturberührung.**
Capability-Stand unverändert **0 von 29**; Mapping Activation Gate und Security
Foundation Readiness Gate bleiben `NOT EVALUATED`; die zwölf KB-Kontrollen
bleiben `DOCUMENTED ONLY`; **R-20 bleibt offen**.

**Phase C (`committed` `d6a1a3c`):** Post-Commit-Reconciliation nach
`9c6c0fb` (Parent `17057e2`, `origin/main` synchron). Der
Commit umfasst **22 Pfade**, **3467 Einfügungen**, **87 Löschungen**, **12
neue** und **10 modifizierte** Dateien; **nichts gelöscht, nichts umbenannt**.
**CBP-WP-020 ist `committed` und `complete`**. **R-33 fortgeschrieben von 16/19
auf 17/20** — siehe `RISK_REGISTER.md` und `COMPLIANCE_CHECK.md`. Decisions,
A0-Decisions und ADRs standen zum Abschluss von CBP-WP-020 auf
**55 / 51 / 13**; keine Capability hochgestuft.

---

## CBP-WP-021

| Feld | Wert |
| --- | --- |
| Titel | **Canonical Security Test Inventory Reconciliation** |
| Typ | **governance-and-validation reconciliation** |
| Prompt Mode | **Full** · Context Budget **B2 – Standard** |
| Status | **`in-review`** |
| Aktuelle Phase | **Phase C – Post-Commit Reconciliation** (vorbereitet) |
| Abschlussdatum | **2026-08-03** |
| A0-Entscheidung | **D-056** (konsolidiert, A–U) |
| ADR | **not required** (`ADR_NOT_REQUIRED`) |
| Kanonische Authority | **32** Negativtests · **1** Positivtest · **33** Testfälle |
| Ausgeführt | **0 von 32** Negativtests · **0 von 1** Positivtest |
| Commit | **nicht** ausgeführt (Commit-Autorität beim Human Maintainer) |

Phase A read-only abgeschlossen: vollständiges NT-ID-Inventar und
Authority-Audit. Ergebnis: authoritativ ist die **A2-Acceptance-Matrix**, die
die IDs **definiert** und explizit auszählt — **NT-01 bis NT-24** (24) und
**NT-26 bis NT-33** (8) = **32** Negativtests, plus **PT-01** = **33**
Testfälle. **NT-25** ist nicht aktiv; der Fall ist als PT-01 klassifiziert und
die Nummer bleibt nach Regel **TT-5** bewusst frei. **NT-32 und NT-33** sind
gültig und lösen die frühere dokumentübergreifende Doppelvergabe von NT-23 und
NT-24 auf; die ursprünglichen Matrix-Fälle NT-23 und NT-24 bleiben unverändert
aktiv.

**Die Zahl 31 ist ein überholter, falsch etikettierter Ableitungswert** — sie
entspricht dem von CBP-WP-011 auf **33** korrigierten **Gesamtwert**
(30 NT + 1 PT), der in einer nicht nachgeführten Zusammenfassungszeile
fälschlich als „Negativtests" geführt und von dort weitergereicht wurde.

**Phase B0 (`committed` `0cb4ea9`):** CBP-WP-021 registriert; **D-056**
dokumentiert (A kanonischer Wert · B Positivtest · C Gesamtinventar · D NT-25 ·
E NT-32/NT-33 · F Zahl 31 · G Authority-Rangfolge · H Zuständigkeit ·
I Reconciliation-Umfang inklusive ausführbarer Artefakte · J keine
Control-Hochstufung · K keine Testausführung · L Gates · M Capabilities ·
N R-20 · O R-33 · P Risiko · Q `ADR_NOT_REQUIRED` · R KB-04 ausgeschlossen ·
S CBP-WP-022 nur vorgemerkt · T Commitzähler-Governance ausgenommen ·
U Commit-Autorität).

**Phase B1/B2 (dieser Stand, uncommitted):** Die **Übergangsabweichung ist
aufgelöst**. Die drei ausführbaren Artefakte wurden **atomar in einem Lauf**
geändert: `bundle.json` führt `"total": 32`, `validate.py` erzwingt **32**, und
der Bundle-Test heißt `test_security_negative_tests_are_zero_of_32` und erwartet
`(0, 32)`. Schema, Issue-Codes, Exitcodes und Ausgabeformat sind
**unverändert**; der Validator meldet weiterhin bei **jedem** anderen Wert
fail-closed. Dokumentarisch korrigiert wurden `CBP-WP-011.md` (die falsch
etikettierte Zusammenfassungszeile, mit Erläuterung), beide Roadmap-Dokumente,
die Profil-A-Runbooks, der Runtime-Vertrag, `CBP-WP-020.md` und die
Statusspiegel.

**Historische Darstellungen bleiben erhalten:** die Befundbeschreibung in
CBP-WP-011 („Ursprünglich: 31 Tests, davon 30 Negativtests…"), die dortige
Korrekturtabelle (Vorher 31 → 33) und die R-33-Chronologieeinträge dokumentieren
weiterhin unverändert, dass **31 der frühere fehlerhafte Wert** war.

**Phase B1/B2.1 — Restfundstelle geschlossen:** `deployments/profile-a/README.md`
führte weiterhin „0 von 31 ausgeführt" und wurde in einem eng begrenzten
Nachlauf auf **0 von 32** korrigiert. Die Abhängigkeitsprüfung ergab: die README
ist in `bundle.json` **namentlich** geführt und Teil der
Exakt-sieben-Dateien-Regel, es existiert jedoch **kein** Hash, **keine**
Dateigröße, **kein** Aggregat und **keine** Inhaltsprüfung durch Validator oder
Tests — **abhängige Metadaten waren nicht anzupassen**. **Das Bundle ist damit
intern konsistent.** Die entsprechenden Angaben in `RISK_REGISTER.md` und
`COMPLIANCE_CHECK.md` sind **Chronologieeinträge** und werden sachgerecht in
**Phase C** behandelt.

**Nicht geändert:** keine Acceptance Matrix, kein D-056, keine NT-/PT-Inhalte,
keine neue Test-ID, kein KB-04.

**Keine Control-Hochstufung, keine Testausführung, keine Gateauswertung.**
Capability-Stand unverändert **0 von 29**; beide Runtime-Gates bleiben
`NOT EVALUATED`; die zwölf KB-Kontrollen bleiben `DOCUMENTED ONLY`; **R-20
bleibt offen**; **R-33 fortgeschrieben 17/20 → 18/21** in Phase C.

**Phase C (dieser Stand, uncommitted):** Post-Commit-Reconciliation nach
`271acc7` (Parent `0cb4ea9`, `origin/main` synchron). Der Commit umfasst **19
Pfade**, **156 Einfügungen**, **97 Löschungen**, **ausschließlich modifizierte
Dateien** — nichts neu, nichts gelöscht, nichts umbenannt. **CBP-WP-021 ist
`committed` und `complete`**, Abschlussdatum **2026-08-03**; **kein Work Package
ist aktiv** und **kein Folge-Work-Package autorisiert**. **R-33 fortgeschrieben
von 17/20 auf 18/21** — achtzehnter Konsistenzvorgang, identisch gespiegelt in
`RISK_REGISTER.md` und `COMPLIANCE_CHECK.md`, **genau einmal gezählt**; B0,
B1/B2, die README-Note-Schließung und der Bytecode-Cleanup gehören zusammen zu
**einem** Vorgang. Decisions, A0-Decisions und ADRs bleiben **56 / 52 / 13**;
keine Capability hochgestuft, keine neue Decision, kein ADR, **keine neue
Risiko-ID**.

**Erhaltene technische Evidenz aus B1/B2** — in Phase C **nicht erneut
ausgeführt**: Bundle-Test **166 OK**, Gesamtsuite **724 OK**, je **0
übersprungen**, Exit 0; `compileall` Exit 0; Validator zweimal Exit 0,
`PROFILE-A-BUNDLE VALID`, `issues=0`, byte-identisch; Repository-Bytecode **0**.

**KB-04 ist nicht Bestandteil von CBP-WP-021.** Das spätere KB-04-Paket ist als
**nicht autorisierter späterer Kandidat** vorgemerkt; **CBP-WP-022 ist weder
registriert noch autorisiert**.

---

## CBP-WP-022

| Feld | Wert |
| --- | --- |
| Titel | **KB-04 Enforcement Stage 1** |
| Typ | **security-foundation enforcement** (Stufe 1) |
| Prompt Mode | **Full** · Context Budget **B2 – Standard** |
| Status | **`in-review`** |
| Aktuelle Phase | **Phase B2A – Contract Model and Read-only Validator** |
| Registration Decision | **D-057** (konsolidiert, A–M), `accepted`, **A0**, 2026-08-03 |
| ADR-Gate-Decision | **D-058** (konsolidiert, A–M), `accepted`, **A0**, 2026-08-03 — Ergebnis **`ADR_REQUIRED`** |
| Architektur-Decision | **D-059** (konsolidiert, A–N), `accepted`, **A0**, 2026-08-03 — Ergebnis **`ADR-0014_ACCEPTED`** |
| Contract-Decision | **D-060** (konsolidiert, A–S), `accepted`, **A0**, 2026-08-03 — Ergebnis **`KB-04_STAGE_1_CONTRACT_ACCEPTED`**, **`ADR_NOT_REQUIRED`** |
| ADR | **ADR-0014** — *KB-04 Stage 1 Filesystem Enforcement Architecture*, `accepted`, **Autoritätsklasse A1**, 2026-08-03 |
| Enforcement Contract | [KB_04_STAGE_1_ENFORCEMENT_CONTRACT.md](../docs/security/KB_04_STAGE_1_ENFORCEMENT_CONTRACT.md) — **`accepted contract`**, 2026-08-03 |
| Human-Maintainer-Freigabe | **B1C Contract and Validation Plan authorized** |
| Technische Implementierung | **nicht autorisiert** |
| Commit | **B0 `committed` `e4caa14`** · **B1A `committed` `1a7696d`** · **B1B `committed` `b86a35f`** · **B1C `committed` `24de07e`** · **B2A nicht committed** (Commit-Autorität beim Human Maintainer) |

**KB-04 ist der Kontrollbereich „Dateisystemrechte“.** Ziel: **Deny-by-default
auf Dateiebene**; Bedrohung: **Direktzugriff unter Umgehung der Anwendung**.
Anforderung laut Spezifikation: explizite Owner- und Gruppenregeln, **keine
world-writable Dateien**, **kein Schreibrecht auf Canonical durch Retrieval oder
Ingest**, **Symlink-Escapes blockieren**, sichere Dateierstellung und **atomare
Writes**. Negativtests **NT-04** und **NT-05**, Stop-Bedingung **SB-S04**,
Nachweisstufe **4**, Durchsetzungsstufe **1**.

**„Enforcement Stage 1“** bezeichnet **Stufe 1 der neunstufigen technischen
Durchsetzungsreihenfolge** (Spezifikation §11) — **OS-Dateirechte**, *„gilt
noch, wenn die Anwendung kompromittiert ist“*. Der englische Begriff ist eine
**Benennung** dieser bestehenden Stufe, **keine neue Definition**.

**Phase B0 (dieser Stand, uncommitted):** CBP-WP-022 registriert; **D-057**
dokumentiert (A Gegenstand · B kanonische KB-04-Bedeutung · C
Stage-1-Zuordnung · D bestehende Registrierung als Control · E
Voraussetzungen · F OD-37 · G Registrierungsgrenze · H Stage-1-Grenze
· I ADR-Status · J unveränderte Grenzen · K Human-Authority ·
L Folge-WP · M Commit-Autorität). Der repository-weite
KB-04-Authority-Audit ergab **keinen Widerspruch**.

**Ausdrücklich nicht autorisiert:** technische Implementierung ·
Runtime-Code · Tests · Bundle- oder Validatoränderung ·
Control-Hochstufung · Gateauswertung · Capability-Änderung ·
Security-Testausführung · Stage 2 · Infrastruktur · RT-2 ·
Persistenz · Folge-Work-Package.

**Unverändert:** KB-04 und die übrigen elf Controls bleiben
`DOCUMENTED ONLY`; beide Runtime-Gates `NOT EVALUATED`; Capabilities **0 von 29**;
Security-Foundation-Tests **0 von 32** und **0 von 1**; **R-20 offen**; **R-33
unverändert 18/21**; **keine neue Risiko-ID**.

**Offene Voraussetzung:** **OD-37** (P1, Deployment Required) betrifft die
produktive Isolation auf der Ziel-VM für KB-03 und KB-04 und bleibt
**offen**. Die Nachweisstufe 4 verlangt eine **reale Profil-A-Instanz**, die
**nicht existiert**.

**Phase B1A (dieser Stand, uncommitted):** Vollständiger technischer
KB-04-Authority- und Design-Grenzen-Audit durchgeführt — **kein Konflikt**.
Die **Contract Boundary** ist implementierungsneutral festgehalten: sieben
verbindliche Sicherheitsinvarianten (I-1 bis I-7), die noch offenen
Designparameter, fünf implementierungsneutrale Verantwortlichkeiten, die
Fail-closed-Grenze und der Nicht-Stage-1-Scope.

**ADR-Gate — Ergebnis `ADR_REQUIRED` (D-058).** Sechs der zehn Designachsen
enthalten eine offene, architekturweit wirkende Wahl: **Owner- und
Gruppenmodell** (das Identity Model führt bewusst keine Benutzer, Gruppen,
UID- oder GID-Werte), **UID-/GID-Abbildung und Host-/Container-Grenze**
(Deployment Required), **konkrete Datei- und Verzeichnismodi** (im Foundation
Plan ausdrücklich *offen — Deployment*), **Durchsetzungsakteur**,
**Verifikations- gegen Korrektursemantik** sowie **Migrations- und
Reparaturverhalten**. **ADR-0009 ist nicht konkret genug**, und **keine
bestehende ADR** deckt die Lösungswahl ab. Die Entscheidung ist **schwer
reversibel** und **sicherheitskritisch**, weil KB-04 die unterste tragende
Ebene ist.

**Voraussichtlich ADR-0014 — in diesem Lauf nicht angelegt.** Nächste
mögliche Phase: **B1B – ADR-0014 Authoring and Design Decision**.
*Phase B1A ist seit `1a7696d` committed; B1B wurde anschließend freigegeben.*

**Bereits entschieden und daher keine offene Achse:** die Schreib- und
Erstellungssemantik — exklusive Temp-Datei, `fsync`, `os.replace`, kein
Schreiben außerhalb des Roots, keine Hard- oder Symlinks (ADR-0010/ADR-0011,
in `quarantine/store.py` und `registry/storage.py` bereits implementiert).

**Unverändert:** KB-04 und alle zwölf Controls `DOCUMENTED ONLY`; beide
Runtime-Gates `NOT EVALUATED`; Capabilities **0 von 29**; **NT-04 und NT-05
nicht ausgeführt**; **R-20 offen**; **OD-37 offen**; **R-33 18/21**; keine neue
Risiko-ID; keine reale Bereitstellung; kein RT-2; **CBP-WP-023 nicht
registriert**.

**Phase B1B (dieser Stand, uncommitted):** **ADR-0014** — *KB-04 Stage 1
Filesystem Enforcement Architecture* — wurde erstellt und ist **`accepted`**
mit **Autoritätsklasse A1**; angenommen durch **D-059** (`accepted`, **A0**,
2026-08-03, Teile A–N). Das bestehende Autoritätsmodell bleibt
unverändert: **die Decision trägt A0, der angenommene ADR trägt A1**.

**Gewählte Architektur:** **Host-authoritative Enforcement mit deklarativem Zielmodell und read-only Runtime-Validierung** (Option A). Drei Schichten mit
disjunkten Befugnissen — das **Repository** hält ausschließlich das
**abstrakte** Zielmodell ohne reale Identitäten, UIDs, GIDs, Modi, Benutzer,
Gruppen oder Hostpfade; der **Deployment- und Setup-Akteur** bindet Rollen an
konkrete Identitäten und setzt Besitz und Rechte **vor** dem Runtime-Start;
die **Runtime** besitzt **ausschließlich Lese- und Ablehnungsrecht**.
**Keine lang laufende Runtime-Komponente verändert jemals Besitz, Gruppe,
Modus oder Identität** — unabhängig davon, ob die Umgebung die
nötigen Privilegien böte.

**Entschieden** sind Authority-Modell, Identitätsmodell mit explizit
erklärter und beim Start gegen die **effektive** Identität geprüfter
Host-/Container-Bindung, das **Rechteprofil-Modell PP-1 bis PP-4**,
Initialisierung, Validierung an vier Zeitpunkten, Migration und Reparatur nach
dem Prinzip **Plan vor Wirkung**, Link- und Pfadsicherheit einschließlich
ausdrücklich anerkannter **TOCTOU**-Grenze, Plattformgrenze und
Nachweisgrenze. Die Invarianten **I-1 bis I-7** bleiben unverändert bindend.

**Verworfen:** Option C (Runtime Self-Repair) als **repository-widersprüchlich**
— V-1, V-3 und `cap_drop: ALL` entziehen die nötigen Privilegien, I-7 wird
verletzt, NT-04/NT-05 verlieren ihre Aussagekraft; Option D (ACL-centric) als
Hauptmechanismus; Option E (Zielmodell ohne Validierung). Option B ist
**nicht verworfen, sondern verortet** — die Initialisierung liegt auf der
**Deployment-Seite** der Grenze.

**Bewusst offen — vierzehn Implementierungsparameter**, darunter die
vollständige Pfad-zu-Rolle-zu-Modus-Matrix, exakte Modusprofile, `umask`,
Konfigurationsschema, Initialisierungs-, Validierungs-, Migrations- und
Reparaturvertrag, Fehlerklassen, Issue- und Exitcodebedarf, Testmatrix,
NT-04-/NT-05-Abbildung, B2-Scope sowie **sämtliche realen UID-, GID-,
Benutzer- und Gruppenwerte** (Deployment Required).

**Phase B1C ist seit diesem Stand abgeschlossen** — siehe unten. **B2 bleibt
gesperrt.**

**Unverändert nach B1B:** **KB-04 bleibt `DOCUMENTED ONLY`**, alle zwölf
Controls `DOCUMENTED ONLY` — **keine Control-Hochstufung**; beide
Runtime-Gates `NOT EVALUATED` — **keine Gateauswertung**; Capabilities
**0 von 29**; **NT-04 und NT-05 nicht ausgeführt** (0 von 32 Negativtests,
0 von 1 Positivtest); **R-20 offen**; **OD-37 offen** — **strukturiert, nicht
geschlossen**; **R-33 18/21**; keine neue Risiko-ID; keine reale Bereitstellung;
kein RT-2; **CBP-WP-023 nicht registriert**.

**Eine entschiedene Architektur ist keine Sicherheitswirkung.**

**Phase B1C (dieser Stand, uncommitted):** **D-060** (`accepted`, **A0**,
2026-08-03, Teile A–S) nimmt den implementierungsfähigen Vertrag
[KB_04_STAGE_1_ENFORCEMENT_CONTRACT.md](../docs/security/KB_04_STAGE_1_ENFORCEMENT_CONTRACT.md)
an — Status **`accepted contract`**, Ergebnis
**`KB-04_STAGE_1_CONTRACT_ACCEPTED`**, ADR-Status **`ADR_NOT_REQUIRED`**.
**D-060 konkretisiert ADR-0014, ändert es nicht und führt keine neue
Architektur ein.** **ADR-0014 bleibt die bindende A1-Authority.**

**Gebunden sind die vierzehn offenen Parameter aus ADR-0014:**

- **elf Pfadklassen PC-01 bis PC-11**, verankert an den bereits committeten
  `container_paths` und `tmpfs_targets` des Profil-A-Bundles — **kein
  erfundener Rootpfad, kein Hostpfad**; **PC-11 ist die Klasse der unbekannten
  Pfade und endet fail-closed**;
- **zehn Akteure** mit zwölf Befugnisspalten; nur der Setup-Akteur setzt
  initial Besitz und Rechte, **keine normale Runtime-Komponente ändert
  jemals Besitz, Gruppe, Modus oder Bindung**;
- **Rechteprofile** — **PP-1** `0600`/`0700`, **PP-2** `0640`/`0750`
  (setgid `2750` nur bei zwingender Gruppenvererbung), **PP-3a** `0640`/`0750`,
  **PP-3b** `0444`/`0555` — **eng begrenztes Kompatibilitätsprofil, nur PC-07,
  secretfrei** — und **PP-4** *not-present*; `umask` **`0077`**
  beziehungsweise **`0027`**; acht kategorische Klassenregeln. **PP-3b ist eine
  ausdrückliche, vollständig begründete Ausnahme** (Regeln 3b-1 bis
  3b-16), weil das committete Bundle den Config-Bindmount mit `mode: 292`
  (`0444`) führt — **der Vertrag ändert das Bundle nicht, er
  übernimmt und validiert den Wert**. **PP-3b gilt ausschließlich für
  PC-07**, ist **nicht übertragbar**, **kein allgemeines read-only Profil**
  und **kein sicherer Default**; **Secrets, Credentials, lokale UID-/GID-Werte,
  Benutzer- und Gruppennamen, Identitätsbindungen sowie sensible Operator-
  und Deploymentwerte sind darunter unzulässig** und enden fail-closed;
  **`world-writable` bleibt ausnahmslos verboten**;
- **vier getrennte Prüfdimensionen** **D-I** Host-Quellobjekt, **D-II**
  Mountvertrag, **D-III** Runtime-sichtbares Objekt und **D-IV**
  Runtimeidentität (MT-9 bis MT-14): **der Bundlemodus ist kein Nachweis der
  Host-Quellrechte**, keine Dimension belegt eine andere, **eine nicht
  prüfbare Dimension gilt als nicht erfüllt**;
- **Mount- und POSIX-Trennung MT-1 bis MT-8** — Runtime-Schreibzugriff
  verlangt **gleichzeitig** Mountmodus, Rolle, PP-Profil und **positive**
  Identitätsbindung; **unbekannter Mountstatus = fail-closed**;
- **Identitätsbindungsvertrag** mit elf Feldern, davon zehn Pflichtfeldern;
  **keine Konfigurationsdatei angelegt, kein realer Wert eingetragen**; **kein
  Default, keine Ableitung, kein Fallback**;
- **Initialisierung strikt getrennt von Bestandsmigration** — Apply nur auf
  nachweislich neuer, leerer Struktur; Transaktionsgrenze **Preflight → Plan
  → begrenztes Apply → Post-Validation**; **keine Rollback-Zusage**,
  weil kein Mechanismus existiert;
- **vier read-only Validierungszeitpunkte** — Installation, **Start vor
  Dienstaufnahme**, Schreibzeit, Gate; **kein periodischer Self-Repair**;
  Grundregel **nicht feststellbar = nicht erfüllt**;
- **zehn Link- und Pfadregeln LP-1 bis LP-10** einschließlich abgelehnter
  interner Symlinks, verbotener Hardlinks und ausdrücklich anerkannter
  **TOCTOU**-Grenze;
- **24 Fehlerklassen** mit Präfix **`KB04-`**, alle fail-closed;
- **Issue- und Exitcodes** — Wiederverwendung von
  `RUNTIME_START_BLOCKED` (4), `CONFIG_INVALID` (2) und `USAGE_ERROR` (64)
  **ohne semantische Überladung**, dazu zwei **reservierte, nicht
  implementierte** Namen `FILESYSTEM_ENFORCEMENT_BLOCKED` (**15**) und
  `FILESYSTEM_MIGRATION_REQUIRED` (**16**). **Keine bestehende Kennung
  überschrieben, keine neue Security-Test-ID, NT-25 bleibt frei.**
  **Reservierung heißt nicht Implementierung** (RC-1 bis RC-10): die Codes
  sind **nicht implementiert**, **kein Pfad emittiert sie**, **das heutige
  öffentliche Verhalten bleibt unverändert**, und vor einer Umsetzung
  sind Nummer, Name, Semantik und öffentliche Kompatibilität erneut zu
  prüfen — bei Kollision **keine stille Neunummerierung, B2 stoppen**;
- **Test- und Evidenzplan** mit **zwölf positiven** und **dreiunddreißig
  negativen** Fällen — einschließlich der vollständigen
  PP-3b-Prüffolge und acht negativer PP-3b-Fälle — unter den vorläufigen internen Kennungen
  `KB04-T-P*` und `KB04-T-N*` — **ausdrücklich keine Security-Test-IDs**;
  synthetische und reale Evidenz getrennt, **nur real** sind die Fälle zu
  **NT-04** und **NT-05**. **Kein Testfall wurde ausgeführt.**

**Reparatur bleibt an RT-2 gebunden.** RT-2 ist **nicht implementiert**, damit
ist der **ausführende Reparaturmodus gesperrt**; zulässig ist
ausschließlich **plan-only**.

**B2-Kandidat beschrieben, nicht autorisiert:** **B2A** Contract Model and
Read-only Validator · **B2B** New-target Initialization Boundary ·
**B2C** Synthetic Tests and Evidence · **B2D** Profile-A Deployment
Integration. Gesperrt bleiben produktive Reparatur, Migration bestehender
Daten, RT-2, reale Gatefreigabe, Control-Uplift und **Stage 2**.

**Unverändert nach B1C:** **KB-04 bleibt `DOCUMENTED ONLY`**, alle zwölf
Controls `DOCUMENTED ONLY` — **keine Control-Hochstufung**; beide
Runtime-Gates `NOT EVALUATED` — **keine Gateauswertung**; Capabilities
**0 von 29**; **NT-04 und NT-05 nicht ausgeführt** (0 von 32 Negativtests,
0 von 1 Positivtest); **SB-S04 nicht wirksam**; **R-20 offen**; **OD-37 offen**
— **strukturiert, nicht geschlossen**; **R-33 18/21**; keine neue
Risiko-ID; **RT-2 nicht implementiert**; keine reale Bereitstellung;
**CBP-WP-023 nicht registriert**.

**Ein implementierungsfähiger Vertrag ist keine Implementierung, und eine
geplante Prüfung ist kein Nachweis.**

**Phase B2A (dieser Stand, uncommitted):** Das interne, **read-only**
Enforcement-Paket `core/core_brain/enforcement/` ist implementiert — sechs Module:

| Modul | Verantwortung |
| --- | --- |
| `contract.py` | Teilmodell: **elf Pfadklassen**, **fünf Profilausprägungen**, zehn Akteure, vier Dimensionen, Selbstkonsistenzprüfung, **Dokument- und Modellhash** gegen Drift |
| `binding.py` | Identitätsbindung mit **zehn Pflichtfeldern**; keine Auflösung realer Identitäten, **kein Default, kein Fallback** |
| `paths.py` | Root-Boundary, Symlink- und Hardlinkablehnung, Objektartklassifikation, dokumentierte **TOCTOU**-Grenze |
| `validator.py` | injizierbare Beobachtungsmodelle **D-I bis D-IV**, read-only Prüfungen, **PP-3b-Inhaltsklassifikation** |
| `aggregate.py` | Befunde, **fail-closed Faltung**, deterministische Serialisierung |
| `__init__.py` | explizite Re-Exporte; **nicht** in `core/core_brain/__init__.py` aufgenommen |

Dazu **21 additive `KB04-*`-ReasonCodes** und `FilesystemEnforcementError` in
`errors.py`. **206 neue Tests**, Gesamtsuite **930 grün, 0 übersprungen**,
**ohne einen einzigen Plattformskip**.

**Herkunft ist Pflicht.** Jede Beobachtung trägt `SYNTHETIC`, `DECLARED`
oder `OBSERVED`. `operationally_verified` wird **nur** wahr, wenn alle vier
Dimensionen konform **und** durchgängig `OBSERVED` sind — eine
synthetische oder deklarierte Konformität erzeugt sie **nie**.

**PP-3b bleibt eng begrenzt:** nur PC-07; `SENSITIVE_OR_SECRET` ist eine
Verletzung, `UNCLASSIFIED` und eine fehlende Klassifikation sind
**`INDETERMINATE`** — **kein Default auf secret-free**, **keine
Inhaltsanalyse**, **kein Secret-Scanning**.

**Nicht implementiert und nicht autorisiert:** CLI · Config-Datei ·
Deploymentänderung · neuer Exitcode (15 und 16 bleiben **reine
Reservierung**) · Initialisierung · Migration · Reparatur ·
`chmod` · `chown` · jede Dateisystemmutation · RT-2 ·
Gateauswertung · Control-Hochstufung · Ausführung von NT-04 oder
NT-05.

**Unverändert nach B2A:** Decisions/A0/ADRs **60/56/14** · **KB-04 und
alle zwölf Controls `DOCUMENTED ONLY`** · beide Gates
**`NOT EVALUATED`** · Capabilities **0 von 29** · **NT-04 und NT-05
nicht ausgeführt** · **SB-S04 nicht wirksam** · **R-20 offen**
· **OD-37 offen** · **R-33 18/21** · keine neue Risiko-ID ·
**RT-2 nicht implementiert** · keine reale Bereitstellung ·
**CBP-WP-023 nicht registriert**.

**Nächste mögliche Phasen: B2B, B2C und B2D — sämtlich nicht
autorisiert.**

**Eine synthetisch festgestellte Konformität ist keine KB-04-Evidenz.**

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
