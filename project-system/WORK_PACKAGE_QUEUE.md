# Work Package Queue – Core Brain Pilot

| Feld | Wert |
| --- | --- |
| Phase | Phase 0 – Discovery und Scope Lock |
| Aktuelles Work Package | **CBP-WP-001** |
| Naechstes Gate | G0 – Discovery and Scope Lock |
| Autoritaetsklasse | A2 |
| Stand | 2026-07-20 |

Spalten nach `WORK_PACKAGE_QUEUE_TEMPLATE.md` (NDF v1.0.0).

## Statuswerte

| Status | Bedeutung |
| --- | --- |
| `proposed` | Vorgeschlagen, **nicht freigegeben** |
| `released` | Vom Human Maintainer freigegeben |
| `in-progress` | In Ausfuehrung durch den Implementation Agent |
| `in-review` | Ausgefuehrt, wartet auf Review |
| `done` | Review bestanden, GO erteilt |
| `blocked` | Angehalten, Blocker gemeldet |

## Queue

| ID | Title | Priority | Status | Prompt |
| --- | --- | --- | --- | --- |
| CBP-WP-001 | Repository Bootstrap und dokumentarisches Projektfundament | P1 | `in-review` | [work-packages/CBP-WP-001.md](../work-packages/CBP-WP-001.md) |
| CBP-WP-002 | Gate-G0-Kriterien und Beantwortung der P1-Discovery-Fragen | P1 | `proposed` | noch nicht erstellt |

Weitere Work Packages werden erst nach Abschluss von G0 durch Nova geplant.
Eine Planung vor dem Scope Lock waere Spekulation.

## CBP-WP-001

| Feld | Wert |
| --- | --- |
| Typ | `docs-only` |
| Prompt Mode | Standard (deklariert als "Lean", siehe AB-01) |
| Context Budget | B2 – Standard |
| Ergebnis | Dokumentarisches Fundament, 23 Dateien |
| Commit | **nicht** ausgefuehrt |

## CBP-WP-002 (Vorschlag, nicht freigegeben)

| Feld | Wert |
| --- | --- |
| Typ | `docs-only` |
| Prompt Mode | **Full** — Scope Lock ist governance-kritisch |
| Ziel | Kriterien fuer Gate G0 definieren und die 11 P1-Fragen beantworten |
| Voraussetzung | Core-Brain-Uebergabe und Second-Brain-Bauanleitung beilegen (OI-01) |

Betroffen: OD-01 bis OD-11 in
[DECISION_REGISTER.md](DECISION_REGISTER.md).

**Nicht ausfuehren** ohne ausdrueckliche Freigabe.

## Regeln

Aus `WORK_PACKAGE_QUEUE_TEMPLATE.md` (NDF v1.0.0):

1. Work Packages klein halten.
2. Jedes Work Package braucht eine Rueckmeldung an Nova.
3. **Keine autonomen Commits oder Pushes.**

Ergaenzend fuer dieses Projekt:

4. Genau ein Work Package ist gleichzeitig `in-progress`.
5. Der Lifecycle `Classify → Plan → Execute → Report to Nova → Review → Commit`
   wird vollstaendig durchlaufen.
6. Ein Statuswechsel nach `released` erfolgt ausschliesslich durch den Human
   Maintainer.
7. Bei fehlender Autorisierung: nicht raten, anhalten, Blocker melden.
