# Work Package Queue – Core Brain Pilot

| Feld | Wert |
| --- | --- |
| Phase | **Phase 0 COMPLETE** · Phase 1 AUTHORIZED FOR PLANNING |
| Aktuelles Work Package | **CBP-WP-010** (`in-review`) |
| Gate G0 | **PASSED WITH NOTES** — 2026-07-21 |
| Überarbeitet in | **CBP-WP-010** |
| Autoritätsklasse | A2 |
| Stand | 2026-07-21 |

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
| CBP-WP-010 | **Pilot Source Mapping Specification** | P0 | **`in-review`** | [work-packages/CBP-WP-010.md](../work-packages/CBP-WP-010.md) |
| CBP-WP-011 | Technical Security Foundation Specification | P0 | `proposed` | noch nicht erstellt |
| CBP-WP-012 | Foundation Runtime Skeleton | P1 | `proposed` | noch nicht erstellt |
| CBP-WP-013 | Ingest Quarantine Minimum Viable Pipeline | P1 | `proposed` | noch nicht erstellt |
| CBP-WP-014 | Deterministic Source Registry and Catalog | P1 | `proposed` | noch nicht erstellt |

**Vier Work Packages sind als `proposed` geführt** — CBP-WP-011 bis
CBP-WP-014, geschnitten in
[PHASE_1_WORK_PACKAGE_MAP.md](../docs/roadmap/PHASE_1_WORK_PACKAGE_MAP.md).
**Keines ist freigegeben. Implementierung autorisiert: nein.**

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
| Status | **`in-review`** |
| Commit | **nicht** ausgeführt |

Ergebnis: **drei A0-Entscheidungen** — D-031 (YAML-1.2-Strict-Subset mit
JSON-Schema-Vertragsgrenze), D-032 (hybride Collection-Strategie), D-033 (eine
Source Boundary je Mapping). **ADR-0008** `accepted`. Mapping-Spezifikation,
Feldschema mit **31 Feldern**, **24 Validierungsregeln**, Zustandsmodell mit
**10 Zuständen**, slotspezifische Regeln für PS-02/PS-03/PS-04, **10
synthetische Beispiele**, private Operator-Vorlage und das
**Aktivierungsgate** mit 20 Punkten (`NOT EVALUATED`). Klarstellungsnachtrag
zum Veröffentlichungsbegriff in ADR-0006.

**Kein Mapping erstellt, keine Quelle angebunden, nichts aktiviert.**

## CBP-WP-011 — einziges vorgeschlagenes nächstes Work Package

| Feld | Wert |
| --- | --- |
| Titel | **Technical Security Foundation Specification** |
| Typ | `docs-only` |
| Prompt Mode | **Full** |
| Context Budget | **B2 – Standard** |
| Status | **`proposed`** |

**Ziel.** Die zwölf Kontrollbereiche KB-01 bis KB-12 in prüfbare technische
Kontrollen und Abnahmetests überführen.

**Verboten:** Bereitstellung, Installation, Port-, UID- oder Hostpfadwahl.

**Nicht ausführen** ohne ausdrückliche Freigabe.

## CBP-WP-012 bis CBP-WP-014 — vorgeschlagen, nicht freigegeben

Vollständig geschnitten in
[PHASE_1_WORK_PACKAGE_MAP.md](../docs/roadmap/PHASE_1_WORK_PACKAGE_MAP.md).

| ID | Titel | Typ |
| --- | --- | --- |
| CBP-WP-012 | Foundation Runtime Skeleton | spätere Implementierung |
| CBP-WP-013 | Ingest Quarantine Minimum Viable Pipeline | spätere Implementierung |
| CBP-WP-014 | Deterministic Source Registry and Catalog | spätere Implementierung |

**Alle `proposed`. Implementierung autorisiert: nein.**

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
