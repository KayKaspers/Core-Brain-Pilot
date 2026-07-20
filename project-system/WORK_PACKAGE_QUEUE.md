# Work Package Queue – Core Brain Pilot

| Feld | Wert |
| --- | --- |
| Phase | Phase 0 – Discovery und Scope Lock |
| Aktuelles Work Package | **CBP-WP-003** |
| Nächstes Gate | G0 – Discovery and Scope Lock (**NOT PASSED**) |
| Überarbeitet in | CBP-WP-003 |
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
| CBP-WP-003 | Human Discovery Intake and G0 Evidence Capture | P0 | **`in-review`** | [work-packages/CBP-WP-003.md](../work-packages/CBP-WP-003.md) |
| CBP-WP-004 | Generic Architecture and Deployment Profiles | P0 | `proposed` | noch nicht erstellt |

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
| Status | **`in-review`** |
| Phasen | A (Fragebogen, einmal überarbeitet nach Nova-REWORK) und B (Auswertung) |
| Commit | **nicht** ausgeführt |

Ergebnis: 6 Antworten erhoben, 12 A0-Entscheidungen (D-015 bis D-026),
G0-Kriterien dreistufig klassifiziert, Blocker von 45 auf 25 reduziert,
fehlerhafte Summen korrigiert.

## CBP-WP-004 — Vorschlag, nicht freigegeben

| Feld | Wert |
| --- | --- |
| Titel | **Generic Architecture and Deployment Profiles** |
| Typ | `docs-only` |
| Prompt Mode | **Full** — Architekturfestlegung ist governance-kritisch |
| Context Budget | **B2 – Standard** |

**Ziel.** Die allgemeine, deploymentneutrale Architektur beschreiben und die
Referenzprofile A bis E sauber von den Core-Anforderungen trennen. Dazu gehören
das Deployment-Readiness-Gate für die 16 vertagten Kriterien (OD-33) und die
Nachführung von D-016 in `PROJECT_DEFINITION.md` (OD-31).

**Warum dieses und kein anderes.** Die sechs Intake-Antworten liegen
vollständig vor und legen den Pilotumfang auf Profilebene fest. Damit ist die
Voraussetzung für eine generische Architekturbeschreibung erfüllt. Ein reines
Lückenschließungs-Work-Package wäre verfrüht: die verbleibenden
Core-Required-Lücken (Berechtigungsmodell, Secret-Verfahren, Benchmark) hängen
teilweise am Architekturbild, das erst entstehen muss.

**Nicht enthalten:** Erklärung von G0 als bestanden, Benchmarkfragen,
Implementierung, Einführung eines neuen Gate-Namens ohne Definition.

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
