# NDF-Anwendung in Core Brain Pilot

| Feld | Wert |
| --- | --- |
| Framework | Nova Development Framework **v1.0.0** |
| Quelle | https://github.com/KayKaspers/Nova-Development-Framework/releases/tag/v1.0.0 |
| Verwendung | verbindlich |
| Stand | 2026-07-20 |

> Es wird **ausschliesslich** die freigegebene Version **v1.0.0** verwendet.
> Noch nicht veroeffentlichte v1.1-Planung wird **nicht** uebernommen.

## Rollenmodell

```
Nova (ChatGPT)  →  Implementation Agent  →  Human Maintainer
```

| Rolle | Verantwortung |
| --- | --- |
| **Nova (ChatGPT)** | Planungs- und Architekturagent. Spezifiziert Work Packages: Typ, Scope, Akzeptanzkriterien |
| **Implementation Agent** | Fuehrt genau ein Work Package aus und berichtet strukturiert zurueck |
| **Human Maintainer** | Prueft, entscheidet GO / REWORK / SPLIT / STOP, committet und pusht |

Commit-, Tag- und Release-Autoritaet liegt **ausschliesslich** beim Human
Maintainer.

## Work Package Lifecycle

```
Classify → Plan → Execute → Report to Nova → Review → Commit
```

Sechs Schritte, sequentiell, kein Schritt wird ausgelassen.
Referenz: `framework/standards/WORK_PACKAGE_LIFECYCLE.md` (NDF v1.0.0).

## Work-Package-Typen

Der Typ bestimmt erlaubte Aenderungen, Testerwartung und Reviewtiefe.

| Typ | Kurzcharakter |
| --- | --- |
| `review-only` | Nur Pruefung, keine Aenderung |
| `docs-only` | Nur Dokumentation |
| `code-fix` | Begrenzte Korrektur |
| `feature` | Neue Funktionalitaet |
| `security-baseline` | Sicherheitsgrundlage |
| `destructive-blueprint` | Plan fuer destruktive Aenderung |
| `destructive-implementation` | Ausfuehrung einer destruktiven Aenderung |
| `project-adapter` | Anpassung an ein Zielprojekt |

Referenz: `framework/standards/WORK_PACKAGE_TYPES.md` (NDF v1.0.0).

**CBP-WP-001 ist vom Typ `docs-only`.**

## Prompt Modes

| Modus | Einsatz |
| --- | --- |
| **Full** | Vollstaendiger Kontext fuer governance-kritische Arbeit: Scope Lock, Architekturentscheidungen, Security-Policies, Release-Readiness, destruktive Aktionen |
| **Standard** | Mittlerer Kontext fuer vorhersagbare, begrenzte Aufgaben: normale Work Packages, Dokumentationsreviews. Verweist auf dauerhafte Regeln statt sie zu wiederholen |
| **Short** | Minimaler Kontext fuer standardisierte Folgearbeit mit vorhandenem Context Pack |

Referenz: `docs/agent-workflows/NDF_PROMPT_MODES.md` (NDF v1.0.0).

> Zur Abbildung der in CBP-WP-001 verwendeten Bezeichnung "Lean" siehe
> [ADOPTION_NOTES.md](ADOPTION_NOTES.md).

## Context Economy

Kontext wird bewusst sparsam gehandhabt: geladen wird nur, was fuer Aufgabe,
Sicherheit und Review noetig ist.

Fuenf Kontextschichten:

| # | Schicht | Inhalt |
| --- | --- | --- |
| 1 | Durable Rules | Invariante NDF-Prinzipien: Rollenmodell, QA-Policy |
| 2 | Phase Context | Aktueller Fundamentzustand: Scope Lock, WP-Queue |
| 3 | Work Package Context | Der konkrete Auftrag und seine Grenzen |
| 4 | Evidence Context | Belege: Gate-Ausgaben, Git-Logs |
| 5 | Output Summary | Uebergabe-Schnappschuss (Compact Context Summary) |

Weitere Begriffe: **Compact Context Summary** (Uebergabeblock, 5–10 Zeilen,
keine privaten Daten, keine Denkprotokolle) und **Context Packs**
(wiederverwendbare Phasen-Schnappschuesse).

**Nicht verhandelbar:** Sicherheitsregeln, Quality Gates, WP-Hard-Limits,
erforderliche Evidenz und die Freigabe durch den Human Maintainer werden
niemals zur Token-Ersparnis reduziert.

Referenz: `docs/agent-workflows/NDF_CONTEXT_ECONOMY.md` (NDF v1.0.0).

## Security-Grundhaltung

Nach ADR-0032 und Skill-Security-Policy arbeiten NDF-Skills
**documentation-only** und **fail-closed**: keine Skripte, kein Netzwerkzugriff,
kein Secrets-Management, keine privaten Daten, keine autonomen Git- oder
Release-Aktionen.

Core Brain Pilot uebernimmt diese Haltung fuer Implementation Agents.

## Struktur in diesem Projekt

Die verwendete Verzeichnisstruktur und jede Abweichung von den kanonischen
NDF-Vorlagen sind in [ADOPTION_NOTES.md](ADOPTION_NOTES.md) dokumentiert.
