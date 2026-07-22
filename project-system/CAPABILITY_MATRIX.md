# Capability Matrix – Core Brain Pilot

| Feld | Wert |
| --- | --- |
| Phase | **Phase 0 COMPLETE** · Phase 1 AUTHORIZED FOR PLANNING |
| Überarbeitet in | **CBP-WP-012** |
| Autoritätsklasse | A2 |
| Stand | 2026-07-21 |

> **Keine der 29 Produkt-Capabilities ist implementiert.** Der Status
> `implemented` kommt in der Matrix nicht vor und darf erst nach Abnahme durch
> den Human Maintainer vergeben werden. **0 von 29 unverändert.**

## Lokale Skeleton-Bausteine (CBP-WP-012)

CBP-WP-012 hat einen lokalen, fail-closed Runtime Skeleton erstellt und
getestet (69 Tests bestanden). Er setzt **keine** der 29 Produkt-Capabilities
um — insbesondere **nicht** Capability 5 (Ingest-Quarantäne), 6 (Secret-/PII-
Prüfung) oder 20 (Berechtigungen). Diese bleiben `planned` beziehungsweise
`discovery`.

Belegt sind ausschließlich drei **eng umrissene lokale** Bausteine, unterhalb
der Capability-Ebene:

| Baustein | Status | Evidenz |
| --- | --- | --- |
| Runtime Skeleton | **implemented locally** | `core/core_brain/`, 69 Tests |
| Strikte lokale Konfigurationsvalidierung | **implemented locally** | `config.py`, `test_config.py` |
| Fail-closed CLI-Startguard (`run` verweigert) | **implemented locally** | `cli.py`, `test_cli.py` |

**Diese Bausteine sind kein Deploymentnachweis.** Sie belegen nicht:
Security Foundation, Authorization, Secret Management, Egress Control oder
Operational Evidence — jede dieser Aussagen wäre breiter als die Evidenz und
ist ausdrücklich **nicht** zutreffend.

## Zuordnung zu geplanten Work Packages

| Capability | Geplant in | Status bleibt |
| --- | --- | --- |
| 1 Kanonischer Markdown-Wissensbestand | CBP-WP-010 | `discovery` |
| 2 Source Manifest | CBP-WP-014 | `planned` |
| 3 Stabile Source-ID und Content Hash | CBP-WP-014 | `discovery` |
| 5 Ingest-Quarantäne | CBP-WP-013 | `planned` |
| 6 Secret- und PII-Prüfung | CBP-WP-013 | `planned` |
| 7 Deterministischer Quellenindex | CBP-WP-014 | `planned` |
| 20 Quellen- und Collection-Berechtigungen | CBP-WP-012 (Modell), spätere Umsetzung | `planned` |

**Ein zugeordnetes Work Package ist kein Fortschritt, sondern eine Absicht.**

## Zuordnung zu geplanten Work Packages

| Capability | Geplant in | Status bleibt |
| --- | --- | --- |
| 1 Kanonischer Markdown-Wissensbestand | CBP-WP-009, CBP-WP-010 | `discovery` |
| 2 Source Manifest | CBP-WP-014 | `planned` |
| 3 Stabile Source-ID und Content Hash | CBP-WP-014 | `discovery` |
| 5 Ingest-Quarantäne | CBP-WP-013 | `planned` |
| 6 Secret- und PII-Prüfung | CBP-WP-012, CBP-WP-013 | `planned` |
| 7 Deterministischer Quellenindex | CBP-WP-014 | `planned` |

**Alle sechs geplanten Work Packages stehen auf `proposed`.** Keines ist
freigegeben.

## Statuswerte

| Status | Bedeutung |
| --- | --- |
| `planned` | Als Ziel festgehalten, Umsetzung nicht begonnen |
| `discovery` | In Klärung; Anforderung oder Verfahren noch offen |
| `not-started` | Bewusst nicht begonnen, meist durch Sperrliste blockiert |

## Prioritäten

| Prio | Bedeutung |
| --- | --- |
| **P0** | Voraussetzung für den Retrieval-Pilot |
| **P1** | Nach dem Fundament sinnvoll |
| **P2** | Spätere Erweiterung |
| **Deferred** | Ausdrücklich zurückgestellt |

Grundlage der Reihenfolge ist die Kernreihenfolge aus Bauanleitung, Seite 2
und 3: Datenbasis ordnen → Katalog → Suche → Brain-First-Regeln → Baseline-Test
→ danach Wiki → Oberfläche und Graph zuletzt.

## Matrix

| # | Capability | Prio | Status | Notes |
| --- | --- | --- | --- | --- |
| 1 | Kanonischer Markdown-Wissensbestand | **P0** | `discovery` | Ablageort und Schnitt einer Wissenseinheit offen (OD-05, OD-15) |
| 2 | Source Manifest | **P0** | `planned` | Pflichtfelder aus Übergabe §6 abzuleiten (OD-17) |
| 3 | Stabile Source-ID und Content Hash | **P0** | `discovery` | ID muss Umbenennung überleben (OD-16) |
| 4 | Owner- und Verifikationsmodell | P1 | `planned` | Rollenmodell für Einzelnutzer zu klären |
| 5 | Ingest-Quarantäne | P1 | `planned` | Vertrauensgrenze TB-1; kein automatischer Pfad ins Kanonische |
| 6 | Secret- und PII-Prüfung | **P0** | `planned` | Sicherheitskritisch; **Schadensverfahren definiert** (SECRET_INCIDENT_RESPONSE); Erkennung offen |
| 7 | Deterministischer Quellenindex | **P0** | `planned` | Determinismus ist Akzeptanzkriterium |
| 8 | Inkrementelle Indexierung mit Tombstones | **P0** | `planned` | Löschungen müssen im Index nachvollziehbar bleiben |
| 9 | Volltext-, semantische und hybride Suche | **P0** | `planned` | Lokal; **kein Provider gewählt**. qmd bleibt Evaluationskandidat mit Prüfvorbehalt (OD-25) |
| 10 | Brain-First-Retrieval | **P0** | `planned` | Suchleiter aus Übergabe §7 in ARCHITECTURE_PRINCIPLES |
| 11 | Autoritätsfilter | **P0** | `planned` | Setzt Vergabeverfahren A0–A6 voraus (OD-07) |
| 12 | Datenschutzfilter | **P0** | `planned` | Fail-closed; `secret` und `excluded-from-ai` passieren nie |
| 13 | Aktualitätsfilter | P1 | `discovery` | „Veraltet" noch nicht definiert (Fragebogen 4.12) |
| 14 | Zeitliche Gültigkeit und Supersession | P1 | `discovery` | Ausdrucksform offen |
| 15 | Erklärbarer Retrieval-Trace | **P0** | `planned` | Umfang und Format offen (OD-19) |
| 16 | Context Budgets B0–B4 | **P0** | `planned` | **Definiert** in CONTEXT_BUDGETS.md; Richtwerte noch zu kalibrieren (OD-02b) |
| 17 | Reproduzierbare Context Packs | **P0** | `planned` | Reproduzierbarkeit bei gleicher Eingabe ist Akzeptanzkriterium |
| 18 | Konflikt- und Review-Queues | **P0** | `planned` | Auflösung bleibt menschlich; Workflow aus Bauanleitung, Seite 4 |
| 19 | Verifikations-Queues | P1 | `planned` | Hängt an Capability 4 |
| 20 | Quellen- und Collection-Berechtigungen | **P0** | `planned` | **Modell vollständig** (PERMISSION_MODEL, ADR-0004); technische Durchsetzung offen (R-25) |
| 21 | Vault Doctor | **P0** | `planned` | Periodische Bestandsprüfung; Prüfkatalog offen |
| 22 | Retrieval-Benchmarks und Regressionstests | **P0** | `planned` | **Design vollständig**: Dataset 1.0.0, 36 Fragen, Metriken, Governance. **Nicht ausgeführt** — kein Lauf, keine Messung |
| 23 | Atomare Änderungen und Mehrschreiberschutz | P1 | `planned` | Verfahren offen (Fragebogen 6.8) |
| 24 | Private Mehrgeräte- und Mobile-Nutzung | P1 | `planned` | Zugriffsweg offen (OD-21) |
| 25 | Docker-Compose-Betrieb | P2 | `not-started` | Referenzprofil D; kein Pflichtziel der ersten Phase |
| 26 | Austauschbare Web-UI | P2 | `not-started` | Erst nach Retrieval-Pilot-Gate (D-014) |
| 27 | Read-only MCP/API | P2 | `not-started` | **Provenienz: CBP-WP-001 (A2).** In keiner Originalquelle belegt; Übergabe §10 fordert lediglich „keine unkontrollierten MCP-Server". Siehe Ü-05 |
| 28 | Backup, Restore und Rebuild | **P0** | `planned` | Rebuild-Vertrag in SYSTEM_ARCHITECTURE; Zielwerte im [DRC](../docs/operations/DEPLOYMENT_READINESS_CHECK.md) |
| 29 | Deployment-neutrale Architektur | **P0** | `planned` | **ADR-0001 angenommen**; fünf Profile in DEPLOYMENT_PROFILES beschrieben |

## Zurückgestellt

Ausdrücklich **Deferred**, überwiegend aus Projektübergabe §17:

| Capability | Grund |
| --- | --- |
| Graph-Web-App | Oberfläche und Graph zuletzt (Bauanleitung, Seite 5) |
| Vollständiger Wiki-Ingest | Nur begrenzter Wiki-Pilot vorgesehen (Übergabe §15 Phase 5) |
| Multi-Tenant-SaaS | Nicht verpflichtend in der ersten Phase (Übergabe §4) |
| Kubernetes | Nicht verpflichtend in der ersten Phase (Übergabe §4) |
| Proxmox-API-Integration | Ausdrücklich untersagt (Übergabe §10, §17) |
| Autonome Konfliktentscheidung | Widerspricht dem Kernprinzip menschlicher Kuration |
| Autonome Commits und Pushes | Untersagt (Übergabe §10, §17) |

## Zusammenfassung

| Priorität | Anzahl |
| --- | --- |
| **P0** | **17** |
| P1 | 8 |
| P2 | 4 |
| Deferred | 7 (nicht Teil der 29) |

| Status | Anzahl |
| --- | --- |
| `planned` | 22 |
| `discovery` | 4 |
| `not-started` | 3 |
| **implemented** | **0** |
| **Summe** | **29** |

Alle 29 Capabilities tragen eine Priorität.

## NDF-Basisdimensionen

Aus `CAPABILITY_MATRIX_TEMPLATE.md` (NDF v1.0.0):

| Capability | Prio | Status | Notes |
| --- | --- | --- | --- |
| Documentation | **P0** | `planned` | Fundament angelegt und gegen die Quellen abgeglichen |
| Tests | P1 | `not-started` | Kein Code vorhanden |
| CI/CD | P2 | `not-started` | In Phase 0 verboten |
| Docker | P2 | `not-started` | Identisch mit Capability 25 |
| Security | **P0** | `discovery` | Berechtigungs- und Incident-Modell dokumentiert (ADR-0004); **technisch nicht durchgesetzt** (R-25, R-27, R-30) |
| Project Brain | **P0** | `planned` | `project-brain/PROJECT_BRAIN.md` angelegt |
| Prompt Workflow | **P0** | `planned` | NDF-Lifecycle übernommen, WP-Queue geführt |
| Release Process | P2 | `not-started` | Ohne Implementierung und Lizenz nicht definierbar (AB-07) |

## Pflege

Ein Statuswechsel erfolgt ausschließlich im Rahmen eines freigegebenen Work
Packages. Der Wechsel nach `implemented` setzt eine Abnahme durch den Human
Maintainer voraus. Ein Implementation Agent hebt keinen Status eigenmächtig an.
