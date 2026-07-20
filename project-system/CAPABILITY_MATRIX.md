# Capability Matrix – Core Brain Pilot

| Feld | Wert |
| --- | --- |
| Phase | Phase 0 – Discovery und Scope Lock |
| Autoritaetsklasse | A2 |
| Stand | 2026-07-20 |

> **Keine Capability ist implementiert.** Der Status `implemented` kommt in
> diesem Dokument nicht vor und darf erst nach Abnahme durch den Human
> Maintainer vergeben werden.

## Statuswerte

| Status | Bedeutung |
| --- | --- |
| `planned` | Als Ziel festgehalten, Umsetzung noch nicht begonnen |
| `discovery` | In Klaerung; Anforderung oder Verfahren noch offen |
| `not-started` | Bewusst nicht begonnen, haeufig durch Sperrliste blockiert |

`planned` ist der Basiswert aus `CAPABILITY_MATRIX_TEMPLATE.md` (NDF v1.0.0).

## Matrix

| # | Capability | Status | Notes |
| --- | --- | --- | --- |
| 1 | Kanonischer Markdown-Wissensbestand | `discovery` | Ablageort und Schnitt einer Wissenseinheit offen (Q-05, Q-07) |
| 2 | Source Manifest | `planned` | Pflichtfelder noch nicht definiert (Q-09) |
| 3 | Stabile Source-ID und Content Hash | `discovery` | ID muss Umbenennung ueberleben; Bildungsvorschrift offen (Q-08) |
| 4 | Owner- und Verifikationsmodell | `planned` | Rollenmodell fuer Einzelnutzer zu klaeren |
| 5 | Ingest-Quarantaene | `planned` | Vertrauensgrenze TB-1; kein automatischer Pfad in den kanonischen Bestand |
| 6 | Secret- und PII-Pruefung | `planned` | Sicherheitskritisch; automatisch oder manuell offen (Q-17) |
| 7 | Deterministischer Quellenindex | `planned` | Determinismus ist Akzeptanzkriterium, nicht Nebeneffekt |
| 8 | Inkrementelle Indexierung mit Tombstones | `planned` | Loeschungen muessen im Index nachvollziehbar bleiben |
| 9 | Volltext-, semantische und hybride Suche | `planned` | Lokal; Engine und Embedding-Modell offen |
| 10 | Brain-First-Retrieval | `discovery` | Reihenfolge und Ebenen noch nicht definiert (Q-19) |
| 11 | Autoritaetsfilter | `planned` | Setzt A0–A6-Vergabeverfahren voraus (Q-10) |
| 12 | Datenschutzfilter | `planned` | Fail-closed; `secret` und `excluded-from-ai` passieren nie |
| 13 | Aktualitaetsfilter | `discovery` | "Veraltet" noch nicht definiert (Q-12) |
| 14 | Zeitliche Gueltigkeit und Supersession | `discovery` | Ausdrucksform offen (Q-13) |
| 15 | Erklaerbarer Retrieval-Trace | `planned` | Umfang und Format offen (Q-21) |
| 16 | Context Budgets B0–B4 | `discovery` | Masseinheit und Schwellen undefiniert (OI-03, Q-18) |
| 17 | Reproduzierbare Context Packs | `planned` | Reproduzierbarkeit bei gleicher Eingabe ist Akzeptanzkriterium |
| 18 | Konflikt- und Review-Queues | `planned` | Aufloesung bleibt menschlich; keine Automatik |
| 19 | Verifikations-Queues | `planned` | Haengt an Capability 4 |
| 20 | Quellen- und Collection-Berechtigungen | `planned` | Vertrauensgrenze TB-5 |
| 21 | Vault Doctor | `planned` | Periodische Bestandspruefung; Pruefkatalog offen |
| 22 | Retrieval-Benchmarks und Regressionstests | `planned` | Ohne Benchmark keine Qualitaetsaussage (Q-22) |
| 23 | Atomare Aenderungen und Mehrschreiberschutz | `planned` | Verfahren offen (Q-27) |
| 24 | Private Mehrgeraete- und Mobile-Nutzung | `planned` | Zugriffsweg offen (Q-23) |
| 25 | Docker-Compose-Betrieb | `not-started` | **Gesperrt** in Phase 0 |
| 26 | Austauschbare Web-UI | `not-started` | **Gesperrt** in Phase 0 |
| 27 | Read-only MCP/API | `not-started` | **Gesperrt** in Phase 0 |
| 28 | Backup, Restore und Rebuild | `planned` | Drei unterscheidbare Faehigkeiten (Q-25, Q-26) |
| 29 | Deployment-neutrale Architektur | `planned` | Querschnitt; wirkt als Randbedingung auf alle uebrigen |

## Zusammenfassung

| Status | Anzahl |
| --- | --- |
| `planned` | 20 |
| `discovery` | 6 |
| `not-started` | 3 |
| **implemented** | **0** |
| **Summe** | **29** |

## NDF-Basisdimensionen

Die Vorlage `CAPABILITY_MATRIX_TEMPLATE.md` (NDF v1.0.0) fuehrt acht
Projektdimensionen. Zustand in diesem Projekt:

| Capability | Status | Notes |
| --- | --- | --- |
| Documentation | `planned` | Fundament durch CBP-WP-001 angelegt, Discovery offen |
| Tests | `not-started` | Kein Code vorhanden |
| CI/CD | `not-started` | CI-Workflows in Phase 0 verboten |
| Docker | `not-started` | Gesperrt; identisch mit Capability 25 |
| Security | `discovery` | Datenklassen und Vertrauensgrenzen dokumentiert, nicht durchgesetzt |
| Project Brain | `planned` | `project-brain/PROJECT_BRAIN.md` angelegt |
| Prompt Workflow | `planned` | NDF-Lifecycle uebernommen, WP-Queue angelegt |
| Release Process | `not-started` | Ohne Implementierung und Lizenzentscheidung nicht definierbar (AB-07) |

## Pflege

Ein Statuswechsel erfolgt ausschliesslich im Rahmen eines freigegebenen Work
Packages. Ein Implementation Agent hebt keinen Status eigenmaechtig an; der
Wechsel nach `implemented` setzt eine Abnahme durch den Human Maintainer
voraus.
