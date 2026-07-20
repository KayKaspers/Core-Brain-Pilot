# Work Package Queue – Core Brain Pilot

| Feld | Wert |
| --- | --- |
| Phase | Phase 0 – Discovery und Scope Lock |
| Aktuelles Work Package | **CBP-WP-002** |
| Nächstes Gate | G0 – Discovery and Scope Lock (**NOT PASSED**) |
| Überarbeitet in | CBP-WP-002 |
| Autoritätsklasse | A2 |
| Stand | 2026-07-20 |

Spalten nach `WORK_PACKAGE_QUEUE_TEMPLATE.md` (NDF v1.0.0).

## Statuswerte

| Status | Bedeutung |
| --- | --- |
| `proposed` | Vorgeschlagen, **nicht freigegeben** |
| `released` | Vom Human Maintainer freigegeben |
| `active` | In Ausführung durch den Implementation Agent |
| `in-review` | Ausgeführt, wartet auf Review |
| `complete` | Review bestanden, GO erteilt |
| `committed` | Ergebnis committet, durch Git bestätigt |
| `blocked` | Angehalten, Blocker gemeldet |

## Queue

| ID | Title | Priority | Status | Prompt |
| --- | --- | --- | --- | --- |
| CBP-WP-001 | Repository Bootstrap und dokumentarisches Projektfundament | P0 | **`committed`** | [work-packages/CBP-WP-001.md](../work-packages/CBP-WP-001.md) |
| CBP-WP-002 | Source Reconciliation und G0 Scope-Lock-Definition | P0 | **`in-review`** | [work-packages/CBP-WP-002.md](../work-packages/CBP-WP-002.md) |
| CBP-WP-003 | Human Discovery Intake and G0 Evidence Capture | P0 | `proposed` | noch nicht erstellt |

Genau ein Work Package ist als `proposed` geführt. Weitere werden erst nach
Abschluss von G0 geplant.

---

## CBP-WP-001

| Feld | Wert |
| --- | --- |
| Typ | `docs-only` |
| Prompt Mode | **Standard** (ursprünglich als „Lean" deklariert, siehe AB-01) |
| Context Budget | B2 – Standard |
| Ergebnis | Dokumentarisches Fundament, 23 Dateien |
| Status | **`committed`** |

**Git-Bestätigung:** Commit `849794e CBP-WP-001: bootstrap NDF project
foundation`, gepusht nach `origin/main`. Der Status `committed` ist durch Git
belegt, nicht behauptet.

## CBP-WP-002

| Feld | Wert |
| --- | --- |
| Typ | `docs-only` |
| Prompt Mode | **Full** |
| Context Budget | B2 – Standard |
| Ausführungsversuche | 3 (zwei BLOCKED in der Vorprüfung, einer ausgeführt) |
| Status | **`in-review`** |
| Commit | **nicht** ausgeführt |

Ergebnis: Quellenabgleich gegen A4/A5/A6, Context Budgets B0–B4 definiert, 41
G0-Kriterien, konsolidierter Fragebogen, Register bereinigt, Capabilities
priorisiert.

Der Status wechselt erst nach bestandenen Prüfungen und Review auf `complete`.

## CBP-WP-003 — Vorschlag, nicht freigegeben

| Feld | Wert |
| --- | --- |
| Titel | Human Discovery Intake and G0 Evidence Capture |
| Typ | `docs-only` |
| Prompt Mode | **Full** — Scope Lock ist governance-kritisch |
| Context Budget | B1 – Lean |
| Ziel | Die 35 P0-Fragen des Fragebogens mit dem Human Maintainer beantworten und als Nachweis in den 39 blockierenden G0-Kriterien hinterlegen |

**Warum B1:** Die Antworten kommen vom Menschen, nicht aus Quellen. Es ist
kein breiter Quellenkontext nötig — die beiden Discovery-Dokumente genügen.

**Voraussetzung:** Verfügbarkeit des Human Maintainers für eine gebündelte
Beantwortung. Die Fragen sind bewusst in einem Dokument gesammelt, um genau
eine Unterbrechung statt vieler Einzelrückfragen zu erzeugen.

**Nicht enthalten:** Erklärung von G0 als bestanden. Das bleibt ein eigener
A0-Akt des Human Maintainers.

**Nicht ausführen** ohne ausdrückliche Freigabe.

---

## Regeln

Aus `WORK_PACKAGE_QUEUE_TEMPLATE.md` (NDF v1.0.0):

1. Work Packages klein halten.
2. Jedes Work Package braucht eine Rückmeldung an Nova.
3. **Keine autonomen Commits oder Pushes.**

Ergänzend für dieses Projekt:

4. Genau ein Work Package ist gleichzeitig `active`.
5. Der Lifecycle `Classify → Plan → Execute → Report to Nova → Review → Commit`
   wird vollständig durchlaufen.
6. Ein Statuswechsel nach `released` erfolgt ausschließlich durch den Human
   Maintainer.
7. Der Status `committed` wird nur vergeben, wenn Git ihn bestätigt.
8. Bei fehlender Autorisierung: nicht raten, anhalten, Blocker melden.
