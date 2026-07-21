# Work Package Queue – Core Brain Pilot

| Feld | Wert |
| --- | --- |
| Phase | Phase 0 – Discovery und Scope Lock |
| Aktuelles Work Package | **CBP-WP-007** |
| Gate G0 | **PASSED WITH NOTES** — 2026-07-21 |
| Phase | **Phase 0 COMPLETE** · Phase 1 AUTHORIZED FOR PLANNING |
| Überarbeitet in | CBP-WP-007 |
| Autoritätsklasse | A2 |
| Stand | 2026-07-20 |

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
| CBP-WP-007 | G0 Decision Recording and Phase 1 Backlog | P0 | **`in-review`** | [work-packages/CBP-WP-007.md](../work-packages/CBP-WP-007.md) |
| CBP-WP-008 | Phase 1 Foundation Implementation Plan | P0 | `proposed` | noch nicht erstellt |

Genau ein Work Package ist als `proposed` geführt.

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
| Status | **`in-review`** |
| Ablauf | interaktiv — Phase A Entscheidungsfragebogen, Phase B Aufzeichnung |
| Commit | **nicht** ausgeführt |

Ergebnis: **G0 PASSED WITH NOTES** und **ADR-0006 accepted**, beide am
2026-07-21 durch den Human Maintainer (A0). Phase-1-Backlog mit 11 Punkten,
Status **AUTHORIZED FOR PLANNING**. Zähl- und Statusregel ergänzt.

## CBP-WP-008 — Vorschlag, nicht freigegeben

| Feld | Wert |
| --- | --- |
| Titel | **Phase 1 Foundation Implementation Plan** |
| Typ | `docs-only` |
| Prompt Mode | **Full** |
| Context Budget | **B2 – Standard** |

**Ziel.** Aus dem Phase-1-Backlog einen ausführbaren Plan machen: die Punkte
P1 bis P5 in konkrete Work Packages schneiden, mit Reihenfolge, Nachweisen und
Abbruchbedingungen. Schwerpunkt auf **P3 (technische Sicherheitsgrundlage)** —
dem breitesten Enabler.

**Weiterhin `docs-only`.** Der Plan beschreibt die Umsetzung, er beginnt sie
nicht. Die G0-Freigabe autorisiert Planung, nicht Implementierung.

**Nicht ausführen** ohne ausdrückliche Freigabe.
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
