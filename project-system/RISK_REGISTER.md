# Risk Register – Core Brain Pilot

| Feld | Wert |
| --- | --- |
| Phase | Phase 0 – Discovery und Scope Lock |
| Überarbeitet in | CBP-WP-002 |
| Autoritätsklasse | A2 |
| Stand | 2026-07-20 |

> **Ablageabweichung.** NDF v1.0.0 sieht `project-brain/RISKS.md` vor.
> Es existiert bewusst nur **eine** von beiden — siehe AB-04 in
> [../docs/ndf/ADOPTION_NOTES.md](../docs/ndf/ADOPTION_NOTES.md).

## Bewertung

Schweregrad **hoch / mittel / niedrig** nach Schadenshöhe und Umkehrbarkeit.
Ein irreversibler Schaden ist mindestens **hoch**, auch bei geringer
Eintrittswahrscheinlichkeit.

## Sicherheit und Datenschutz

| ID | Risiko | Schwere | Gegenmaßnahme | Status |
| --- | --- | --- | --- | --- |
| R-01 | Secret gelangt in die Git-Historie und ist praktisch nicht mehr entfernbar | **hoch** | `.gitignore`, keine Beispiel-Secrets, Secret-Prüfung beim Ingest, Verfahren OD-10 | teilweise gemindert |
| R-02 | `confidential` oder `excluded-from-ai` gelangt in den Modellkontext | **hoch** | Datenschutzfilter TB-4, fail-closed bei unbekannter Klasse | offen |
| R-03 | Datenklassen werden nie konsequent vergeben; Filter laufen ins Leere | **hoch** | Klassenvergabe verpflichtend an TB-1, Vault Doctor | offen |
| R-04 | Prompt Injection aus ingestiertem Material steuert einen Agenten | **hoch** | Ingest ist Daten, nie Anweisung; Quarantäne TB-1 | offen |
| R-05 | Inhalte werden an das Claude-Modell übertragen, obwohl ihre Klasse das nicht erlaubt | **hoch** | Datenschutzmatrix mit Spalte „darf an Claude übertragen werden"; Übergabe §11 | offen |
| **R-25** | **Berechtigungen bestehen nur als Promptregel und nicht technisch** | **hoch** | Übergabe §10 verlangt technische Umsetzung; fünf Berechtigungsstufen in TRUST_BOUNDARIES | **offen** |
| **R-26** | **Betrieb als Root oder direkt auf dem Proxmox-Host** | **hoch** | Ausdrückliches Verbot in TRUST_BOUNDARIES; Übergabe §10 | offen |
| **R-27** | **Pauschale GitHub-Schreibrechte oder allgemeiner Repository-Schreibzugriff** | **hoch** | Verbot in TRUST_BOUNDARIES; Erhebung über E-2 bis E-4 | offen |

## Wissensintegrität

| ID | Risiko | Schwere | Gegenmaßnahme | Status |
| --- | --- | --- | --- | --- |
| R-06 | Abgeleitete Inhalte (A6) überschreiben kuratierte (A0–A5) | **hoch** | Autoritätsmodell, Einbahnregel TB-3 | offen |
| R-07 | Indexverlust bedeutet Wissensverlust, weil Kanonisches nur im Index lag | **hoch** | Trennung kanonisch/abgeleitet, Rebuild-Fähigkeit | offen |
| R-08 | Widersprüche werden automatisch aufgelöst statt vorgelegt | mittel | Konflikt-Queue, menschliche Auflösung | offen |
| R-09 | Veraltetes Wissen wird als aktuell ausgeliefert | mittel | Aktualitätsfilter, Supersession | offen |
| R-10 | Nichtdeterministische Indexierung macht Ergebnisse unreproduzierbar | mittel | Determinismus als Akzeptanzkriterium | offen |
| R-11 | Paralleler Schreibzugriff von mehreren Geräten beschädigt den Bestand | mittel | Atomare Änderungen, Mehrschreiberschutz | offen |
| **R-22** | **Source Drift — die A6-Textfassung weicht von der A4-PDF ab, ohne dass es auffällt** | **mittel** | PDF bleibt Original; Textfassung ausdrücklich als A6 geführt; visuelle Prüfung nicht behauptet; bei Abweichung gilt die PDF | **dokumentiert** |
| **R-23** | **Unvollständiger Quellenabgleich — Aussagen der PDF, die in der Textfassung fehlen, bleiben unbemerkt** | **mittel** | Abgleich in SOURCE_RECONCILIATION nachvollziehbar; Nachprüfung bei verfügbarem PDF-Rendering möglich | **offen** |

## Projekt und Prozess

| ID | Risiko | Schwere | Gegenmaßnahme | Status |
| --- | --- | --- | --- | --- |
| R-12 | Vorgezogene Implementierung präjudiziert offene Architekturentscheidungen | **hoch** | Sperrliste `DO_NOT_START.md`, Aufhebung nur per A0 | gemindert |
| R-13 | **Scope Creep** — 29 Capabilities ohne Priorisierung führen zu Scope-Überdehnung | **hoch** | Priorisierung P0/P1/P2/Deferred in der Capability Matrix; Scope Lock an G0 | **gemindert** |
| R-14 | **G0 ohne objektive Kriterien** ist nicht abschließbar | mittel | 41 Kriterien mit Nachweis, Owner und Abschlussregel | **geschlossen** |
| R-15 | Verbindliche Eingangsquellen liegen nicht vor | mittel | Beide Quellen abgeglichen; OI-01 geschlossen | **geschlossen** |
| R-16 | Dokumentationsfundament driftet vom tatsächlichen Stand ab | mittel | Pflege in jedem Work Package, `project-brain` als Einstiegspunkt | offen |
| R-17 | Abweichungen vom NDF wachsen unkontrolliert | niedrig | `ADOPTION_NOTES.md`; AB-03 bis AB-08 nur vorläufig akzeptiert, Entscheidung vor G0 | gemindert |
| R-18 | Fehlende Lizenz blockiert spätere Nutzung oder Veröffentlichung | niedrig | OD-23 | offen |
| **R-24** | **Verwechslung von NDF Prompt Mode und Core-Brain Context Budget** | **mittel** | Ausdrückliche Abgrenzung in CONTEXT_BUDGETS und CLAUDE.md; D-009 | **gemindert** |
| **R-28** | **Ein zweites Governance-System wird neben NDF eingeführt** | mittel | Übergabe §14: Superpowers nur als Referenz; Aufnahme in DO_NOT_START | gemindert |

## Betrieb

| ID | Risiko | Schwere | Gegenmaßnahme | Status |
| --- | --- | --- | --- | --- |
| R-19 | Bindung an Proxmox oder Compose sickert in die Architektur ein | mittel | Prinzip Deployment-Neutralität; fünf Referenzprofile A–E | offen |
| R-20 | **Fehlende Restore-Evidenz** — Sicherung existiert, Wiederherstellung wurde nie geprobt | **hoch** | Übergabe §12: geprüfter Wiederherstellungspunkt vor Reorganisation, Ingest, Sync-Änderung und Wiki-Migration; Zielwerte OD-30 | **offen** |
| R-21 | Retrieval-Qualität verschlechtert sich unbemerkt | mittel | Benchmarks und Regressionstests; mindestens 30 Fragen (G-1) | offen |
| **R-29** | **Produktive Synchronisation ohne Test-Vault führt zu Datenverlust** | **hoch** | Übergabe §9 und §17: keine produktive Sync-Lösung vor Prüfung auf Konflikte, Datenverlust und Backupfähigkeit | offen |
| **R-30** | **Datenschutzklassifikation ohne technische Durchsetzung** — die Klassen existieren dokumentarisch, greifen aber nirgends | **hoch** | Fünf Durchsetzungsebenen in DATA_CLASSIFICATION; nur Ebene 1 wirksam | **offen** |

## Zusammenfassung

| Schwere | Anzahl |
| --- | --- |
| hoch | 14 |
| mittel | 13 |
| niedrig | 2 |
| **Summe** | **29** |

| Status | Anzahl |
| --- | --- |
| geschlossen | 2 |
| gemindert | 5 |
| dokumentiert | 1 |
| teilweise gemindert | 1 |
| offen | 20 |

**In CBP-WP-002 geschlossen:** R-14 (G0-Kriterien liegen vor), R-15
(Quellenabgleich durchgeführt).

**In CBP-WP-002 neu:** R-22 bis R-30.

**In CBP-WP-002 verändert:** R-13 von `offen` auf `gemindert` (Priorisierung),
R-17 auf `gemindert` (AB-Status), R-05 präzisiert um die Claude-Übertragung,
R-20 von `mittel` auf **`hoch`** angehoben — ungetestetes Restore ist bei
Eintritt irreversibel.

## Pflege

Ein Risiko wird nicht gelöscht, sondern auf `geschlossen` gesetzt und mit der
wirksamen Kontrolle verknüpft.
