# Phase 1 Backlog

| Feld | Wert |
| --- | --- |
| **Status** | **AUTHORIZED FOR PLANNING** |
| **Nicht** | **AUTHORIZED FOR IMPLEMENTATION** |
| Grundlage | G0 **PASSED WITH NOTES**, 2026-07-21, A0 |
| Erfasst in | CBP-WP-007 |
| Autoritätsklasse | A3 |
| Stand | 2026-07-21 |

---

## Geltungsbereich

Die G0-Entscheidung autorisiert **ausschließlich die Planung** von Phase 1.
Sie ist **keine** Freigabe für produktiven Betrieb, produktiven Ingest,
öffentliche Erreichbarkeit oder die Verarbeitung zusätzlicher sensibler
Datenklassen.

**Jeder Backlogpunkt trägt „Implementierung erlaubt: nein".** Ein Punkt wird
erst durch ein eigenes, freigegebenes Work Package ausführbar.

### Auflagen aus der G0-Entscheidung

Vor einem **produktiven Betrieb** sind mindestens zu erbringen:

| # | Nachweis | Backlogpunkt |
| --- | --- | --- |
| 1 | Technische Durchsetzung des Berechtigungsmodells | **P3** |
| 2 | Erfolgreiche Negativtests für `excluded-from-ai` | **P8** |
| 3 | Durchführung und Auswertung des V0-/V1-Benchmarks | **P7** |
| 4 | Deployment Readiness Check für das gewählte Profil mit Status `ready` | **P10** |
| 5 | Erfolgreicher Backup-, Restore- und Rebuild-Test | **P9** |

Zusätzlich: **Web-UI und mobile Nutzung erst nach einem funktionierenden und
gemessenen Retrieval-Piloten** — abgebildet in **P11**.

---

## P1 — Repository- und Arbeitsbereichsentscheidung

| Feld | Wert |
| --- | --- |
| **Ziel** | OD-26 entscheiden; allgemeines Core-Repository und private Wissensbereiche trennen |
| **Abhängigkeiten** | ADR-0006 (`accepted`); Entscheidungsvorlage in `REPOSITORY_LAYOUT_OPTIONS.md` |
| **Nachweis** | Angenommener ADR oder A0-Beschluss zu OD-26; dokumentierte Bereichsgrenze |
| **Relevante Risiken** | R-01 (Secret in der Historie), R-17 (NDF-Abweichungen AB-03…AB-08) |
| **Status** | geplant |
| **Implementierung erlaubt** | **nein** |

**Keine Reorganisation in diesem Work Package.** Die Entscheidung geht der
Verschiebung voraus.

## P2 — Pilot Source Mapping

| Feld | Wert |
| --- | --- |
| **Ziel** | Konkrete Mappings für PS-02, PS-03 und PS-04 definieren |
| **Abhängigkeiten** | P1; ADR-0006; `SOURCE_SLOT_MODEL.md` |
| **Nachweis** | Mapping je Slot; Repository-Allowlist; `read-only`-Defaults belegt |
| **Relevante Risiken** | R-27 (Repository-Zugriffe), R-01 |
| **Status** | geplant |
| **Implementierung erlaubt** | **nein** |

**Keine produktiven Daten im allgemeinen Repository.** Mappings sind
fail-closed: ohne Mapping bleibt ein Slot `enabled: false`. Schließt OD-05 und
OD-06.

## P3 — Technische Sicherheitsgrundlage

| Feld | Wert |
| --- | --- |
| **Ziel** | Nicht privilegierter Betrieb, Dateirechte, Mount-Modi, technische Approval-Zustände |
| **Abhängigkeiten** | `PERMISSION_MODEL.md`, ADR-0004 |
| **Nachweis** | Nachweis je Durchsetzungsebene; **kein pauschaler GitHub-Schreibzugriff** |
| **Relevante Risiken** | **R-25**, **R-27**, R-26 |
| **Status** | geplant |
| **Implementierung erlaubt** | **nein** |

**Auflage 1 der G0-Entscheidung.** Bis hierhin bleibt das Berechtigungsmodell
Papier.

## P4 — Ingest Quarantine und Security Scanning

| Feld | Wert |
| --- | --- |
| **Ziel** | Quarantäne, Secret-Prüfung, Datenklassifikation, Freigabe vor Indexierung |
| **Abhängigkeiten** | P3; TB-1, TB-2; D-019 |
| **Nachweis** | Kein Weg von Quarantäne nach kanonisch ohne menschliche Freigabe |
| **Relevante Risiken** | **R-32**, R-03, R-04, R-01 |
| **Status** | geplant |
| **Implementierung erlaubt** | **nein** |

**Noch kein PDF-/Office-Produktiv-Ingest.** PS-06 bleibt `deferred`, bis diese
Grundlage steht.

## P5 — Deterministischer Quellenkatalog

| Feld | Wert |
| --- | --- |
| **Ziel** | Source Registry, stabile Source IDs, Revisionen, Tombstones, reproduzierbarer INDEX |
| **Abhängigkeiten** | P2, P4; Rebuild-Vertrag in `SYSTEM_ARCHITECTURE.md` |
| **Nachweis** | Zwei aufeinanderfolgende Läufe bei unverändertem Input ergeben denselben Indexzustand |
| **Relevante Risiken** | R-10 (Nichtdeterminismus), R-07 |
| **Status** | geplant |
| **Implementierung erlaubt** | **nein** |

## P6 — Lexikalischer Brain-First-Retrieval-Pilot

| Feld | Wert |
| --- | --- |
| **Ziel** | V1 aufbauen: Index als Einstieg, Metadatenfilter, Context Budgets, Retrieval Trace |
| **Abhängigkeiten** | P5; `CONTEXT_BUDGETS.md`; Suchleiter aus `ARCHITECTURE_PRINCIPLES.md` |
| **Nachweis** | Nachvollziehbarer Trace je Anfrage; Quellenbegrenzung eingehalten |
| **Relevante Risiken** | R-21, R-24 |
| **Status** | geplant |
| **Implementierung erlaubt** | **nein** |

**V1 vor V2.** **Keine feste qmd-Entscheidung ohne Evaluation** — OD-25 bleibt
offen.

## P7 — Benchmarkausführung V0 und V1

| Feld | Wert |
| --- | --- |
| **Ziel** | Ersten vollständigen V0-/V1-Vergleich durchführen und auswerten |
| **Abhängigkeiten** | P6; Dataset 2.0.0; `BASELINE_PROTOCOL.md` |
| **Nachweis** | Rohdaten je Lauf, Metriken der vier Gruppen, Liste kritischer Fehler |
| **Relevante Risiken** | **R-21**, OD-02b |
| **Status** | geplant |
| **Implementierung erlaubt** | **nein** |

**Auflage 3 der G0-Entscheidung.** Development-Set zuerst, **Holdout erst zur
formalen Prüfung**. **R-21 bleibt bis zur Messung offen.**

## P8 — `excluded-from-ai`-Sperrwirkung

| Feld | Wert |
| --- | --- |
| **Ziel** | Technische Negativtests der Sperrwirkung |
| **Abhängigkeiten** | P3, P6; Fixtures aus Dataset 2.0.0 |
| **Nachweis** | Sammelanfragen, Context-Pack-Filter, externe Modellgrenze — **Zielwert null Leaks** |
| **Relevante Risiken** | **R-31**, R-02, R-05, R-30 |
| **Status** | geplant |
| **Implementierung erlaubt** | **nein** |

**Auflage 2 der G0-Entscheidung.** Besonders zu prüfen ist der Weg über weit
gefasste Sammelanfragen (Benchmarkfrage D-06).

## P9 — Backup-, Restore- und Rebuild-Test

| Feld | Wert |
| --- | --- |
| **Ziel** | Wiederherstellbarkeit nachweisen — kanonische Daten, Derived Data, Rebuild |
| **Abhängigkeiten** | P5; Rebuild-Vertrag; DRC-Kriterium DRC-16 |
| **Nachweis** | Durchgeführter Restore; Rebuild nach Vertrag verifiziert |
| **Relevante Risiken** | **R-20**, R-07 |
| **Status** | geplant |
| **Implementierung erlaubt** | **nein** |

**Auflage 5 der G0-Entscheidung.** Eine ungeprüfte Sicherung ist keine
Sicherung.

## P10 — Deployment Readiness Profil A

| Feld | Wert |
| --- | --- |
| **Ziel** | DRC für Profil A auf `ready` bringen |
| **Abhängigkeiten** | P3, P9; `DEPLOYMENT_READINESS_CHECK.md` |
| **Nachweis** | Konkrete Proxmox-VM, Ressourcen, Netzwerk, Backup, RPO/RTO, Betriebsverantwortung — 18 Prüfpunkte |
| **Relevante Risiken** | **R-34**, R-20, R-19 |
| **Status** | geplant |
| **Implementierung erlaubt** | **nein** |

**Auflage 4 der G0-Entscheidung.** **Der DRC bleibt fail-closed:** fehlt eine
erforderliche Angabe, wird nicht installiert.

## P11 — Web-UI und Mobile Read/Review

| Feld | Wert |
| --- | --- |
| **Ziel** | Austauschbare Web-UI und mobiler Lese-/Review-Zugang |
| **Abhängigkeiten** | **P6 und P7 abgeschlossen** — funktionierendes und gemessenes Retrieval |
| **Nachweis** | Retrieval-Pilot belegt; keine administrativen Hostrechte; mobile Suche, Lesen, Status, Freigaben |
| **Relevante Risiken** | R-25 (UI-Berechtigungen) |
| **Status** | geplant |
| **Implementierung erlaubt** | **nein** |

**Ausdrückliche Auflage der G0-Entscheidung:** erst nach einem funktionierenden
und **gemessenen** Retrieval-Piloten.

---

## Reihenfolge und Abhängigkeiten

```text
P1 Repository-Entscheidung
 └─ P2 Source Mapping
     └─ P4 Quarantäne & Scanning ──┐
P3 Sicherheitsgrundlage ───────────┼─ P8 excluded-from-ai-Tests
                                   │
     P5 Quellenkatalog ────────────┘
      └─ P6 Retrieval-Pilot V1
          └─ P7 Benchmark V0/V1
              └─ P11 Web-UI & Mobile
     P9 Restore-Test
      └─ P10 Deployment Readiness Profil A
```

**P3 ist der breiteste Enabler** — ohne technische Sicherheitsgrundlage bleiben
P4, P8 und P10 blockiert.

## Nicht in Phase 1

| Ausgeschlossen | Grund |
| --- | --- |
| Knowledge Graph | D-025; nicht Pilotumfang |
| Vollständiger Wiki-Ingest | D-025; Sperrliste |
| Breite externe Connectoren | D-025; PS-07 `deferred` |
| Produktive Obsidian-Synchronisation | D-025; erst nach Test-Vault (R-29) |
| Kubernetes | Sperrliste; Übergabe §4 |
| Multi-Tenant-SaaS | Sperrliste; D-018 |
| Öffentliche Cloudinstanz | Sperrliste |

## Status

**AUTHORIZED FOR PLANNING.**

Elf Backlogpunkte, **alle mit „Implementierung erlaubt: nein"**. Es wurde nichts
gebaut, nichts installiert, nichts angebunden und nichts gemessen.

Der nächste Schritt ist ein **Planungs-Work-Package**, kein Implementierungs-Work-Package.
